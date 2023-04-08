from django.urls import path

from .import views

urlpatterns=[ 
    path('',views.login,name='login'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('home', views.index,name='index'),
    path('register', views.register,name='register'),
    path('inputform', views.inputform,name='inputform'),
    path('loanpredict',views.predictLoan,name='predictloan'),
]