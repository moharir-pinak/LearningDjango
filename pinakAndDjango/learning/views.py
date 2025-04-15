from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def learning(request):
    return render(request, 'learning/index.html')
    
