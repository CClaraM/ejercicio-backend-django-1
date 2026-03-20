import pandas as pd

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Prestamo, Libro, EjemplarLibro
from .permissions import IsAdminRol
from .serializers import MiPrestamoSerializer, LibroCreateSerializer, LibroListSerializer

class MisPrestamosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        prestamos = (
            Prestamo.objects
            .filter(usuario=request.user)
            .select_related('libro')
            .order_by('-fecha_prestamo')
        )

        serializer = MiPrestamoSerializer(prestamos, many=True)
        return Response(serializer.data)
    

class AdminLibroCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRol]

    def post(self, request):
        serializer = LibroCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        libro = serializer.save()

        return Response({
            'id': libro.id,
            'id_libro': libro.id,
            'codigo_libro': libro.codigo_libro,
            'titulo': libro.titulo,
            'autor': libro.autor,
            'area': libro.area,
            'anio_publicacion': libro.anio_publicacion,
            'estado': libro.estado,
            'portada_url': libro.portada_url,
        }, status=status.HTTP_201_CREATED)
    

class AdminImportLibrosView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRol]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {'detail': 'No se envió archivo'},
                status=status.HTTP_400_BAD_REQUEST
            )

        archivo = request.FILES['file']

        try:
            df = pd.read_excel(archivo)
        except Exception as e:
            return Response(
                {'detail': f'Error leyendo Excel: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        inserted = 0
        ejemplares_creados = 0
        errors = []

        for index, row in df.iterrows():
            try:
                codigo = str(row.get('codigo_libro', '')).strip()
                titulo = str(row.get('titulo', '')).strip()
                autor = str(row.get('autor', '')).strip()
                area = str(row.get('area', '')).strip()
                portada = str(row.get('portada_url', '')).strip()

                # Año
                anio_raw = row.get('anio_publicacion')
                anio = int(anio_raw) if pd.notna(anio_raw) else None

                # Cantidad ejemplares
                cant_raw = row.get('cantidad_ejemplares', 0)
                cantidad = int(cant_raw) if pd.notna(cant_raw) else 0

                if not codigo or not titulo or not autor:
                    errors.append(f'Fila {index + 2}: datos incompletos')
                    continue

                libro, created = Libro.objects.get_or_create(
                    codigo_libro=codigo,
                    defaults={
                        'titulo': titulo,
                        'autor': autor,
                        'area': area or None,
                        'anio_publicacion': anio,
                        'portada_url': portada or None,
                    }
                )

                if created:
                    inserted += 1

                #  Crear ejemplares
                for i in range(cantidad):
                    codigo_inv = f"{codigo}-{i+1}"

                    if not EjemplarLibro.objects.filter(codigo_inventario=codigo_inv).exists():
                        EjemplarLibro.objects.create(
                            libro=libro,
                            codigo_inventario=codigo_inv,
                            condicion='bueno',
                            disponibilidad='disponible'
                        )

                        ejemplares_creados += 1

            except Exception as e:
                errors.append(f'Fila {index + 2}: {str(e)}')

        return Response({
            'inserted': inserted,
            'ejemplares_creados': ejemplares_creados,
            'errors': errors,
        })
    
class LibrosListView(APIView):
    def get(self, request):
        search = request.GET.get('search', '').strip()
        libros = Libro.objects.all().order_by('titulo')

        if search:
            libros = libros.filter(titulo__icontains=search)

        serializer = LibroListSerializer(libros, many=True, context={'request': request})
        return Response(serializer.data)
    

class AdminLibroUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRol]

    def put(self, request, id):
        libro = get_object_or_404(Libro, id=id)

        serializer = LibroCreateSerializer(
            libro,
            data=request.data,
            partial=True  # importante para update parcial
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Libro actualizado correctamente',
            'id': libro.id
        }, status=status.HTTP_200_OK)
    
class AdminLibroPortadaUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRol]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, id):
        libro = get_object_or_404(Libro, id=id)

        if 'file' not in request.FILES:
            return Response(
                {'detail': 'No se envió archivo en el campo file'},
                status=status.HTTP_400_BAD_REQUEST
            )

        libro.portada = request.FILES['file']
        libro.save()

        portada_url = request.build_absolute_uri(libro.portada.url) if libro.portada else ''

        return Response({
            'message': 'Portada subida correctamente',
            'portada_url': portada_url,
        }, status=status.HTTP_200_OK)