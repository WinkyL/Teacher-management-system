"""NewSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from teacher import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^dean/$',views.dean, name = 'dean'),
    url(r'^teachertables/$',views.teachertables, name = 'teachertables'),
    url(r'^teacherform/$',views.teacherform, name = 'teacherform'),
    url(r'^faculty/$',views.faculty, name = 'faculty'),
    url(r'^BasicInf/$',views.BasinInf, name = 'basicinf'),
    url(r'^teacheredit/$',views.teacheredit, name = 'teacheredit'),
    url(r'^teachertables/(?P<teacher>\d{8})/$',views.edit, name='teacher_id'),
    url(r'^teachertables/delete=(?P<teacher>\d{8})/$', views.delete, name='teacher_id'),
    url(r'^teachertables/check=(?P<teacher>\d{8})/$', views.check, name='teacher_id'),
    url(r'^teachertables/rate=(?P<teacher>\d{8})/$', views.rate, name='teacher_id'),
    url(r'^ChangePwd/$',views.ChangePwd,name='ChangePwd'),
    url(r'^addclasshour/$',views.Addclasshour, name='AddHour'),
]
