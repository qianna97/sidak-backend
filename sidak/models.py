from django.db import models
from django.contrib.auth.models import User
import datetime

class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nama_kelas

    class Meta:
        verbose_name_plural = 'Kelas'


class Siswa(models.Model):
    KELAMIN = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    no_induk = models.CharField(max_length=20, unique=True, primary_key=True)
    no_induk_nasional = models.CharField(max_length=30, blank=True)
    nama = models.CharField(max_length=50)
    tempat_lahir = models.CharField(max_length=50, blank=True)
    tanggal_lahir = models.DateField(max_length=10, blank=True, null=True)
    kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE)
    jenis_kelamin = models.CharField(max_length=2, choices=KELAMIN, blank=True)
    telepon = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=30, blank=True)
    foto = models.ImageField(upload_to ='uploads/', max_length=50, blank=True)
    petugas_kelas = models.BooleanField(default=True) 

    def __str__(self):
        return self.nama + " - "+ self.no_induk

    class Meta:
        verbose_name_plural = 'Siswa'


class Presensi(models.Model):
    STATUS_PRESENSI = [
        ('HADIR', 'HADIR'),
        ('SAKIT', 'SAKIT'),
        ('IZIN', 'IZIN'),
        ('ABSEN', 'ABSEN'),
    ]
    no_induk = models.ForeignKey(Siswa,on_delete=models.CASCADE, db_constraint=False, related_name="presensi")
    status = models.CharField(max_length=5, choices=STATUS_PRESENSI, blank=True)
    tanggal = models.DateField(max_length=8, blank=False, auto_now_add=True)
    waktu = models.TimeField(auto_now=True)

    def __str__(self):
        return str(self.no_induk) + " - "+ str(self.status)

    class Meta:
        verbose_name_plural = 'Presensi'


class PresensiSetting(models.Model):
    waktu_buka = models.TimeField(default=datetime.time(7,0,0))
    waktu_tutup = models.TimeField(default=datetime.time(11,0,0))
    sabtu_libur = models.BooleanField(default=True)
    kode_preview = models.CharField(max_length=20, blank=False, default='preview123')

    class Meta:
        verbose_name_plural = 'Pengaturan Presensi'


class Libur(models.Model):
    tanggal = models.DateField(max_length=8)

    def __str__(self):
        return str(self.tanggal)

    class Meta:
        verbose_name_plural = 'Hari Libur'


class Surat(models.Model):
    foto = models.ImageField(upload_to='uploads/', blank=True)
    petugas = models.ForeignKey(Siswa,on_delete=models.CASCADE, db_constraint=False, related_name="surat")
    subjek = models.ForeignKey(Siswa,on_delete=models.CASCADE, db_constraint=False, related_name="subjek_surat")
    waktu = models.DateTimeField(auto_now_add=True)
    catatan = models.TextField(blank=False)

    class Meta:
        verbose_name_plural = 'Surat'


class Rekap(models.Model):
    class Meta:
        verbose_name_plural = 'Rekap'