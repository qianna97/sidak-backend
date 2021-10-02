from __future__ import absolute_import
import os
import datetime
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('sidak')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(name="close_presensi")
def closing():
    from .models import Siswa, Presensi
    from .serializers import SiswaSerializer

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    siswa_query = Siswa.objects.all()
    
    for siswa in siswa_query:
        if siswa.presensi.filter(tanggal=today).count() == 0:
            data = {
                'no_induk': siswa,
                'status': 'ABSEN',
                'tanggal': today,
                'waktu': today
            }
            presensi = Presensi.objects.create(**data)
            presensi.save()
    