from .settings import PORTAL_URL


def student_proc(request):
    return {'PORTAL_URL': PORTAL_URL}
