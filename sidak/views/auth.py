from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from sidak.models import Siswa
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions


class IsPetugasKelas(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        data_siswa = Siswa.objects.get(no_induk = request.user.username)
        if data_siswa.petugas_kelas:
            return True
        return False

class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data_siswa = Siswa.objects.get(no_induk=user.username)
        return Response({
            'token': token.key,
            'user_id': data_siswa.pk,
            'no_induk': data_siswa.no_induk
        })


@api_view(['GET',])
def logout(request):
    try:
        request.user.auth_token.delete()
        message = "Logout Success"
        status = status.HTTP_200_OK
    except:
        message = "Failed"
        status = status.HTTP_400_BAD_REQUEST
    return Response(
        data={
            'message': message
        },
        status=status
    )