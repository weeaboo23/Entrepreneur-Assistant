from django.urls import path

from . import views 

urlpatterns = [
    path("",views.login_view , name = "login"),
    path( "homepage/", views.index , name= "index"),
    path("register/", views.createAccount , name="register"),
    path("logout/" , views.logout_view , name= "logout"),
    path("license/", views.licenseSearch , name = "license")
    
]
