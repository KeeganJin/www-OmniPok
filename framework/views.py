from django.shortcuts import render


def index(request):
    """首页视图"""
    return render(request, 'framework/index.html')


def features(request):
    """特性页面视图"""
    return render(request, 'framework/features.html')


def documentation(request):
    """文档页面视图"""
    return render(request, 'framework/documentation.html')

