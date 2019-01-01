from django.shortcuts import render


def index(request):
    return render(request, 'pages/index.html')


def data(request):
    return render(request, 'pages/data.html')


def analysis(request):
    return render(request, 'pages/analysis.html')
