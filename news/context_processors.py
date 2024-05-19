def custom_alerts(request):
    return {'alerts': request.session.pop('custom_alerts', [])}
