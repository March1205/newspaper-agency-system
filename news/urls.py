from django.urls import path

from .views import (
    index,
    RedactorListView,
    RedactorDetailView,
    TopicListView,
    NewspaperListView,
    NewspaperDetailView, RedactorUpdateView, RedactorDeleteView,
    RedactorCreateView, NewspaperUpdateView,
    NewspaperDeleteView, NewspaperCreateView, TopicUpdateView,
    TopicDeleteView, TopicCreateView, RemoveRedactorView,
    AssignRedactorView, SignupView, UserLoginView, logout_view,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "redactor/",
        RedactorListView.as_view(),
        name="redactor-list",
    ),
    path(
        "redactor/<int:pk>/",
        RedactorDetailView.as_view(),
        name="redactor-detail",
    ),
    path(
        "redactor/<int:pk>/update/",
        RedactorUpdateView.as_view(),
        name="redactor-update",
    ),
    path(
        "redactor/<int:pk>/delete/",
        RedactorDeleteView.as_view(),
        name="redactor-delete",
    ),
    path(
        "redactor/create",
        RedactorCreateView.as_view(),
        name="redactor-create",
    ),
    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list",
    ),
    path(
        "newspaper/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail",
    ),
    path(
        "newspaper/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update",
    ),
    path(
        "newspaper/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="newspaper-delete",
    ),
    path(
        "newspapers/create/",
        NewspaperCreateView.as_view(),
        name="newspaper-create",
    ),
    path(
        "topic/",
        TopicListView.as_view(),
        name="topic-list",
    ),
    path(
        "topic/<int:pk>/update/",
        TopicUpdateView.as_view(),
        name="topic-update",
    ),
    path(
        "topic/<int:pk>/delete/",
        TopicDeleteView.as_view(),
        name="topic-delete"
    ),
    path(
        "topic/create/",
        TopicCreateView.as_view(),
        name="topic-create"
    ),
    path(
        "newspapers/remove_redactor/",
        RemoveRedactorView.as_view(),
        name="remove-redactor"
    ),
    path(
        "newspaper/assign_redactor",
        AssignRedactorView.as_view(),
        name="assign-redactor"
    ),
    path(
        "signup/",
        SignupView.as_view(),
        name="signup"
    ),
    path(
        "accounts/login/",
        UserLoginView.as_view(),
        name="login"
    ),
    path(
        "accounts/logout/",
        logout_view,
        name="logout"
    ),

]

app_name = "news"
