from django.shortcuts import render


def welcome(request):
    return render(request, template_name="api/welcome.htm")
