from sidak.models import Siswa, Surat
from sidak.serializers import SuratSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .auth import IsPetugasKelas


class SuratView(APIView):
    permission_classes = [IsAuthenticated, IsPetugasKelas]

    def post(self, request):
        data_petugas = Siswa.objects.get(no_induk=request.user.username)
        data_subjek = Siswa.objects.get(no_induk=request.data['no_induk'])

        if data_petugas.kelas != data_subjek.kelas:
            return Response({
                'message': 'Anda bukan petugas kelas siswa yang dituju'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        datas = {
            'foto': request.data['foto'],
            'petugas': data_petugas.no_induk,
            'subjek': data_subjek.no_induk,
            'catatan': request.data['no_induk']
        }

        surat_serializer = SuratSerializer(data=datas)
        if surat_serializer.is_valid():
            surat_serializer.save()
            return Response({
                'message': 'Surat Berhasil dikirim',
            })
        
        return Response({
            'message': surat_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
