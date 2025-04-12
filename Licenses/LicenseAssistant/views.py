from django.shortcuts import render 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.urls import reverse

from . models import User 
# Create your views here.
def index(request):
    return render(request , "LicenseAssistant/index.html")




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "LicenseAssistant/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "LicenseAssistant/login.html")


def createAccount(request):
     if request.method == "POST":
        username = request.POST["Username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"]
        if password != confirmation:
            return render(request, "LicenseAssistant/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "LicenseAssistant/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
     else:
        return render(request, "LicenseAssistant/register.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def licenseSearch(request):
    return render(request , "LicenseAssistant/license.html")

    