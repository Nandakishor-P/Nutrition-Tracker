from django.shortcuts import render

def nutrition(request):
    return render(request, 'nutrition.html')