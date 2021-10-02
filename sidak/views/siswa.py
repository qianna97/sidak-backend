from sidak.models import Siswa
from sidak.serializers import SiswaSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated



class SiswaList(generics.ListAPIView):
    queryset = Siswa.objects.all()
    serializer_class = SiswaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kelas', ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
       qs = super().get_queryset()
       return qs


class SiswaDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        siswa_query = Siswa.objects.get(no_induk=request.user.username)
        siswa_serializer = SiswaSerializer(siswa_query).data
        
        return Response(
            siswa_serializer
        )

    def patch(self, request):
        pass