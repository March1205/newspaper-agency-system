from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import (
    RedactorSearchForm,
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorCreationForm,
    NewspaperForm
)
from .models import Redactor, Topic, Newspaper
from .utils import add_alert


@login_required
def index(request):
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()
    num_newspapers = Newspaper.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_topics": num_topics,
        "num_newspapers": num_newspapers,
        "num_visits": num_visits + 1,
    }

    return render(request, "news/index.html", context=context)


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    template_name = "news/redactor_list.html"
    paginate_by = 5
    ordering = ["username"]

    def get_context_data(self, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers__topic")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("news:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    fields = ("username", "first_name", "last_name", "years_of_experience")
    success_url = reverse_lazy("news:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("news:redactor-list")

    def form_valid(self, form):
        self.object = self.get_object()
        newspapers = list(self.object.newspapers.all())
        success_url = self.get_success_url()
        self.object.delete()

        for newspaper in newspapers:
            if newspaper.publishers.count() == 0:
                newspaper.delete()
        return HttpResponseRedirect(success_url)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    template_name = "news/topic_list.html"
    paginate_by = 5

    def get_context_data(self, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("news:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("news:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("news:topic-list")

    def form_valid(self, form):
        self.object = self.get_object()
        associated_newspapers = Newspaper.objects.filter(topic=self.object)
        if associated_newspapers.exists():
            add_alert(self.request,
                      "Cannot delete topic because it is "
                      "associated with existing newspapers. "
                      "Please delete those newspapers first.",
                      alert_type="danger")
            return redirect("news:topic-list")
        return super().form_valid(form)


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    template_name = "news/newspaper_list.html"
    paginate_by = 5

    def get_context_data(self, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = (super().get_queryset().select_related("topic").
                    order_by("published_date"))
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            if title:
                queryset = queryset.filter(title__icontains=title)
        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("news:newspaper-list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.published_date > timezone.now().date():
            add_alert(
                self.request,
                "The published date can't be in the future. "
                "Please try again.",
                "danger"
            )
            return self.render_to_response(self.get_context_data(form=form))
        self.object.save()
        form.save_m2m()
        return redirect(self.success_url)


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("news:newspaper-list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.published_date > timezone.now().date():
            add_alert(
                self.request,
                "The published date can't be in the future. "
                "Please try again.",
                "danger"
            )
            return self.render_to_response(self.get_context_data(form=form))
        self.object.save()
        form.save_m2m()
        return redirect(self.success_url)


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("news:newspaper-list")


class AssignRedactorView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        newspaper_id = request.POST.get("newspaper_id")
        newspaper = get_object_or_404(Newspaper, pk=newspaper_id)
        newspaper.publishers.add(request.user)
        return redirect("news:newspaper-detail", pk=newspaper_id)


class RemoveRedactorView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        newspaper_id = request.POST.get("newspaper_id")
        newspaper = get_object_or_404(Newspaper, pk=newspaper_id)
        newspaper.publishers.remove(request.user)
        return redirect("news:newspaper-detail", pk=newspaper_id)
