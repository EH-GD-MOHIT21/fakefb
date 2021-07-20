"""myfbb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.hlo),
    path('login',views.login),
    path('signup',views.signup),
    path('cm',views.cmm),
    path('sgn',views.hlo),
    path('lgn',views.shlgn),
    path('cpost',views.createpost),
    path('logout',views.logout),
    path('addpost',views.addpost),
    path('addcom',views.addcomment),
    path('mposts',views.uposts),
    path('dpost',views.delepost),
    path('dcomme',views.delecomm),
    path('verify/<slug:pid>',views.verify),
    path('verify/verifyacc/<slug:pid>',views.updateuser),
    path('likein',views.likechange),
    path('showprofile',views.yourprofile),
    path('saveupdate',views.saveupdate)
]
