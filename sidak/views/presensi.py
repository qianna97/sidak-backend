from sidak.models import Presensi, PresensiSetting, Libur, Siswa
from sidak.serializers import LiburSerializer, PresensiSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import datetime


class PresensiSiswa(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Presensi.objects.all()
    serializer_class = PresensiSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'status',
        'no_induk',
        'no_induk__kelas__nama_kelas',
        'tanggal'
    ]

    def get_queryset(self):
        queryset = self.queryset
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')

        if from_date and to_date is not None:
            queryset = queryset.filter(tanggal__range=[from_date, to_date])
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        today = datetime.datetime.now()
        libur = Libur.objects.filter(tanggal=today.strftime("%Y-%m-%d")).count()
        presensi_setting = PresensiSetting.objects.get(pk=1)
        hari = 6
        if presensi_setting.sabtu_libur:
            hari = 5

        if today.weekday() < hari and libur == 0:
            data_siswa = Siswa.objects.get(no_induk=request.user.username)

            presensi_query = Presensi.objects \
                .filter(tanggal=today.strftime("%Y-%m-%d")) \
                .filter(no_induk=data_siswa.no_induk).count()

            if presensi_query > 0:
                return Response({
                    'messsage': 'Sudah mengisi presensi'
                }, status=status.HTTP_208_ALREADY_REPORTED)

            if today.strftime("%H:%M") > presensi_setting.waktu_tutup.strftime("%H:%M"):
                return Response({
                    'message': "Waktu pengisin presensi sudah selesai"
                }, status=status.HTTP_401_UNAUTHORIZED)
            if today.strftime("%H:%M") < presensi_setting.waktu_buka.strftime("%H:%M"):
                return Response({
                    'message': "Waktu pengisin presensi belum dibuka"
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            
            data = {
                'no_induk': data_siswa,
                'status': request.data['status'],
                'tanggal': today.strftime("%Y-%m-%d"),
                'waktu': today.strftime("%H:%M")
            }

            presensi = Presensi.objects.create(**data)
            presensi.save()
            return Response({
                'message': "Sukses mengisi kehadiran"
            })
            
            return Response({
                    'message': presensi.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
                'message': "Libur"
            }, status=status.HTTP_400_BAD_REQUEST)