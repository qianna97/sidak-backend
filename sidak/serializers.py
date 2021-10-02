from rest_framework import serializers
from sidak.models import *


class SiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siswa
        fields = [
            'no_induk',
            'no_induk_nasional',
            'nama',
            'tempat_lahir',
            'tanggal_lahir',
            'kelas',
            'jenis_kelamin',
            'telepon',
            'email',
            'foto'
        ]


class SiswaPresensiSerializer(serializers.ModelSerializer):
    kelas = serializers.CharField(source="kelas.nama_kelas")

    class Meta:
        model = Siswa
        fields = [
            'no_induk',
            'nama',
            'kelas'
        ]


class KelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = '__all__'


class PresensiSerializer(serializers.ModelSerializer):
    data_siswa = SiswaPresensiSerializer(source="no_induk")

    class Meta:
        model = Presensi
        fields = [
            'id',
            'data_siswa',
            'status',
            'tanggal',
            'waktu'
        ]


class LiburSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libur
        fields = (
            'tanggal'
        )


class SuratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surat
        fields = '__all__'