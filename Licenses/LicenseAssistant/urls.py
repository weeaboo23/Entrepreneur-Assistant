from django.urls import path

from . import views 

urlpatterns = [
    path("",views.login_view , name = "login"),
    path( "homepage/", views.index , name= "index"),
    path("register/", views.createAccount , name="register"),
    path("logout/" , views.logout_view , name= "logout"),
    path("license/", views.licenseSearch , name = "license"),
    path("license_result/" , views.licenseSearchResults , name="license_results"),
    path("license_result/<slug:slug>/", views.license_details , name = "license_detail"),
    path('contact/', views.contact_me, name='contact_me'),
    path('track/', views.track_applications, name='track_applications'),
    path('change-password/', views.change_password, name='change_password')
    
]
