from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    # return HttpResponse("Hello WElcome to Pinaks 1st backend in django .......")
    return render(request, 'website/index.html')

def about(request):
    return HttpResponse("Pinak Seth cha Bhari Kaam aahe ")