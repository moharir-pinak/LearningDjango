from django.shortcuts import render
from django.http import HttpResponse
from .models import CharVarity
from django.shortcuts import get_object_or_404


# Create your views here.


def learning(request):
    learnings = CharVarity.objects.all() 
    return render(request, 'learning/index.html',{'learnings': learnings})

def learning_detail(request, pk):
    learning = get_object_or_404(CharVarity, pk=pk)
    return render(request, 'learning/learning_detail.html', {'learning': learning})
    
