from django.shortcuts import render

def homePageLogic(request):
    return render(request, 'index.html')
