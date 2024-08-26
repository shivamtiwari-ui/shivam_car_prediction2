from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
   path(' ' , views.home , name='home'),
   path('signin/' , views.signin , name='signin'),
   path('signup/' , views.signup , name='signup'),
   path('signout/' , views.signout , name='signout'),
   path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
   path('send-test-email/', views.send_test_email, name='send_test_email'),
   path('logout/', views.LogoutPage,name='logout'),
  

 
   

]