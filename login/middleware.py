from datetime import datetime, timedelta
from django.shortcuts import redirect

class UserInactivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity_time')
            if last_activity:
                inactive_duration = datetime.now() - last_activity
                max_inactive_duration = timedelta(minutes=30)
                if inactive_duration > max_inactive_duration:
                    # User is inactive, perform logout or other actions
                    # For example, you can clear the session and redirect to the login page
                    request.session.flush()
                    return redirect('login')

        response = self.get_response(request)

        if request.user.is_authenticated:
            request.session['last_activity_time'] = datetime.now()

        return response
