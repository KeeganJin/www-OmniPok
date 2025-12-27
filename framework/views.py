from django.shortcuts import render


def index(request):
    """首页视图"""
    return render(request, 'framework/index.html')


def services(request):
    """服务页面视图"""
    return render(request, 'framework/services.html')


def omnipok_agent(request):
    """OmniPok-Agent 产品页面视图"""
    return render(request, 'framework/omnipok_agent.html')


def about(request):
    """关于我们页面视图"""
    return render(request, 'framework/about.html')


def contact(request):
    """联系我们页面视图"""
    return render(request, 'framework/contact.html')

