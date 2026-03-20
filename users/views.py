from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        documento = serializer.validated_data['documento']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(documento=documento)
        except User.DoesNotExist:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            return Response(
                {'detail': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'detail': 'Usuario inactivo'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'documento': user.documento,
                'username': user.username,
                'nombre': user.first_name,
                'apellido': user.last_name,
                'email': user.email,
                'rol': user.rol,
            }
        }, status=status.HTTP_200_OK)
    
class MiPerfilView(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'documento': getattr(user, 'documento',''),
            'username': user.username,
            'nombre': user.first_name,
            'apellido': user.last_name,
            'email': user.email,
            'rol': getattr(user, 'rol', 'estudiante'),
        })

    def put(self, request):
        user = request.user

        user.first_name =  request.data.get('nombre', user.first_name)
        user.last_name = request.data.get('apellido', user.last_name)
        user.email = request.data.get('correo', user.email)

        if hasattr(user, 'telefono'):
            user.telefono = request.data.get('telefono',user.telefono)
        
        user.save()

        return Response({
            'message': 'Perfil actualizado correctamente',
            'user': {
                'id': user.id,
                'documento': getattr(user, 'documento', ''),
                'username': user.username,
                'nombre': user.first_name,
                'apellido': user.last_name,
                'correo': user.email,
                'telefono': getattr(user, 'telefono', ''),
                'rol': getattr(user, 'rol', 'estudiante'),
            }
        })