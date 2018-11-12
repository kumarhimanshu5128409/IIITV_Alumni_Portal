from django.shortcuts import render

# Create your views here.


def AboutUs(request):
    return render(request, 'pages/about_us.html')

def ContactUs(request):
    return render(request, 'pages/contact_us.html')

def NotAllowed(request):
    return render(request, 'pages/not_allowed.html')

def RegistrationEmailError(request):
    return render(request, 'pages/registration_email_error.html')
