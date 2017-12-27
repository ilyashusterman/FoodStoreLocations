from django.shortcuts import render
from .models import Branches, Chains


# Create your views here.
def home(request):
    home_context = {
        'branches': Branches.objects.all()
    }
    return render(request, 'main.html', context=home_context)
