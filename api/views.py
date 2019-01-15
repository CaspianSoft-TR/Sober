from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Caspiansoft API services...")

def temptest(request):
    user_dict = {'text':'Caspiansoft API services...'}
    return render(request,'web/index.html',context=user_dict)