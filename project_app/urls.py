from django.contrib import admin
from django.urls import path
from project_app import views


urlpatterns = [
    path('register/',views.user_register),
    path('verify_mobile_number/',views.account_otp_varify),
    path('comlete_user_profile/',views.add_username_profile),
    path('user_login/',views.user_login),
    path('varify_login_otp/',views.login_otp_varify),
    path('show_all_images/',views.show_all_images),
    path('user_image_recongnization/',views.user_image_recongnization),
    path('get_user_history/',views.get_user_history),
   
    
]