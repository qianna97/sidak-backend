from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Kelas, Siswa, Presensi, Libur, PresensiSetting, Surat, Rekap
from django.urls import include, path
from django import forms
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Q
import json
import datetime

admin.site.site_header="SIDAK Administrator"
admin.site.site_title="SIDAK Administrator"


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField()


class CustomUser(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'is_active', 'last_login')
    list_filter = ['groups__name', 'is_active', 'last_login', 'is_superuser']


class SiswaAdmin(admin.ModelAdmin):
    list_display = ('no_induk', 'nama', 'kelas')
    list_filter = ['kelas']
    list_per_page = 50
    search_fields = ['nama']

    change_list_template = "siswa_csv_form.html"

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return additional_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra["csv_upload_form"] = CsvUploadForm()
        return super(SiswaAdmin, self).changelist_view(request, extra_context=extra)

    def upload_csv(self, request):
        if request.method == "POST":
            form = CsvUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if request.FILES['csv_file'].name.endswith('csv'):
                    try:
                        import pandas as pd
                        import hashlib

                        data = pd.read_csv(request.FILES['csv_file'])

                        for index, r in data.iterrows():
                            try:
                                no_induk = r['no_induk']
                                nama = r['nama']
                                kelas = r['kelas']
                                password = r['password']
                            except Exception as e:
                                self.message_user(
                                    request,
                                    "Data format invalid:{}".format(e),
                                    level=messages.ERROR
                                )
                                return redirect("..")

                            if Kelas.objects.filter(nama_kelas=kelas).count() == 0:
                                k = Kelas(nama_kelas=kelas)
                                k.save()
                            k = Kelas.objects.get(nama_kelas=kelas)

                            # no passowrd
                            if password == 'nan' or password == 'Nan' or isinstance(password, float):
                                password = '123456'

                            try:
                                obj = Siswa.objects.get(no_induk=no_induk)
                            except Siswa.DoesNotExist:
                                obj = Siswa(
                                    no_induk = no_induk,
                                    nama = nama,
                                    kelas = k
                                )
                                obj.save()
                            
                            try:
                                obj = User.objects.get(username=no_induk)
                            except User.DoesNotExist:
                                name = nama.split(" ")
                                first_name = ""
                                if len(name) > 1:
                                    if len(name[0]) < 3:
                                        first_name = name[1]
                                    else:
                                        first_name = name[0]

                                obj = User.objects.create_user(
                                    username = no_induk,
                                    first_name = first_name,
                                    password = password
                                )
                                group = Group.objects.get(name='Siswa')
                                obj.groups.add(group)
                                obj.save()
                                print("bisa masuk")

                    except Exception as e:
                        self.message_user(
                            request,
                            "There was an error decoding the file:{}".format(e),
                            level=messages.ERROR
                        )
                        return redirect("..")
        else:
            self.message_user(
                request,
                "There was an error in the form {}".format(form.errors),
                level=messages.ERROR
            )

        return redirect("..")


class PresensiAdmin(admin.ModelAdmin):
    model = Presensi
    list_display = ('get_nama', 'status', 'waktu', 'tanggal')
    list_filter = ['tanggal', 'no_induk__kelas', 'status']
    search_fields = ['no_induk__nama']
    list_per_page = 50

    def get_nama(self, obj):
        return obj.no_induk.nama
    get_nama.admin_order_field  = 'siswa'
    get_nama.short_description = 'nama'

    def changelist_view(self, request, extra_context=None):
        hadir = Presensi.objects.values('tanggal').annotate(y=Count('status', filter=Q(status='HADIR')))
        izin = Presensi.objects.values('tanggal').annotate(y=Count('status', filter=Q(status='IZIN')))
        sakit = Presensi.objects.values('tanggal').annotate(y=Count('status', filter=Q(status='SAKIT')))
        absen = Presensi.objects.values('tanggal').annotate(y=Count('status', filter=Q(status='ABSEN')))

        today = datetime.datetime.today().strftime("%Y-%m-%d")

        today_hadir = Presensi.objects.filter(tanggal=today).filter(status="HADIR").count()
        today_izin = Presensi.objects.filter(tanggal=today).filter(status="IZIN").count()
        today_sakit = Presensi.objects.filter(tanggal=today).filter(status="SAKIT").count()
        today_absen = Presensi.objects.filter(tanggal=today).filter(status="ABSEN").count()

        user = User.objects.all().count()

        today_non = user - (today_absen+today_hadir+today_izin+today_sakit)

        hadir_as_json = json.dumps(list(hadir), cls=DjangoJSONEncoder)
        izin_as_json = json.dumps(list(izin), cls=DjangoJSONEncoder)
        sakit_as_json = json.dumps(list(sakit), cls=DjangoJSONEncoder)
        absen_as_json = json.dumps(list(absen), cls=DjangoJSONEncoder)

        extra_context = extra_context or {
            "hadir_data": hadir_as_json,
            "izin_data": izin_as_json,
            "sakit_data": sakit_as_json,
            "absen_data": absen_as_json,
            "today_sakit": today_sakit,
            "today_hadir": today_hadir,
            "today_izin": today_izin,
            "today_absen": today_absen,
            "today_non": today_non
        }

        return super().changelist_view(request, extra_context=extra_context)


class PresensiSettingAdmin(admin.ModelAdmin):
    list_display = ('waktu_buka', 'waktu_tutup', 'sabtu_libur')

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class RekapAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        kelas = Kelas.objects.values_list('nama_kelas', flat=True).distinct()
        tanggal = Presensi.objects.values_list('tanggal', flat=True).distinct()

        tanggal = [x.strftime("%d-%m-%Y") for x in tanggal]

        extra_context = extra_context or {
            'kelas': kelas,
            'tanggal': tanggal
        }

        return super().changelist_view(request, extra_context=extra_context)
    
    def generate_pdf(self):
        return "dsds"



admin.site.unregister(User)
admin.site.register(User, CustomUser)
admin.site.register(Kelas)
admin.site.register(PresensiSetting,PresensiSettingAdmin)
admin.site.register(Libur)
admin.site.register(Siswa, SiswaAdmin)
admin.site.register(Presensi, PresensiAdmin)
admin.site.register(Surat)
admin.site.register(Rekap, RekapAdmin)