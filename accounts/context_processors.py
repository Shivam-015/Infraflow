from .models import Register

def register_data(request):
    users = Register.objects.all()
    return {
        'users': users
    }