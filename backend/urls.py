"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from sidak import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.Login.as_view(), name='api_token_auth'),
    path('logout', views.logout, name='logout'),
    path('siswa', views.SiswaList.as_view()),
    path('siswa/detail', views.SiswaDetail.as_view()),
    path('presensi', views.PresensiSiswa.as_view()),
    path('surat', views.SuratView.as_view()),
    path('rekap/<str:kelas>/<str:tanggal>', views.generate_pdf)
]