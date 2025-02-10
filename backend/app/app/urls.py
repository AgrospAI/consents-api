from django.contrib import admin
from django.urls import path, include
from web3auth import urls as web3auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"^", include(web3auth_urls))
]
