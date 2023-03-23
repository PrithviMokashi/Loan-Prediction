from django.urls import path

from .import views

urlpatterns=[ 
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('login', views.login,name='login'),
    path('register', views.register,name='register'),
    path('inputform', views.inputform,name='inputform'),
    path('loanpredict',views.predictLoan,name='predictloan'),
]