def add_alert(request, message, alert_type="info"):
    if 'custom_alerts' not in request.session:
        request.session['custom_alerts'] = []
    request.session['custom_alerts'].append({
        'message': message,
        'alert_type': alert_type,
    })
    request.session.modified = True
