"""CarRentaller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include,url
# from django.contrib import admin

from rental.views import login
from rental.views import worker
from rental.views import index
from rental.views import showAOrders
from rental.views import complete
from rental.views import showRunning
urlpatterns = [
    url(r'^$',include('rental.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'login.html/',login),
    url(r'login/',login),
    url(r'worker/',worker),
    url(r'show/',showAOrders),
    url(r'generate/',complete),
    url(r'showRunning/',showRunning),
]
