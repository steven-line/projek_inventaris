from django.http import HttpResponseForbidden

def staff_me_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='staff_me').exists():
            return HttpResponseForbidden("Akses terbatas untuk Staff ME.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
