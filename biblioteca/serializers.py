from rest_framework import serializers
from .models import Prestamo, Libro

class MiPrestamoSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source='libro.titulo', read_only=True)
    autor = serializers.CharField(source='libro.autor', read_only=True)
    portada_url = serializers.CharField(source='libro.portada_url', read_only=True)

    class Meta:
        model = Prestamo
        fields = [
            'id',
            'titulo',
            'autor',
            'portada_url',
            'fecha_prestamo',
            'fecha_vencimiento',
            'fecha_devolucion',
            'estado',
        ]


class LibroCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = [
            'id',
            'codigo_libro',
            'titulo',
            'autor',
            'area',
            'anio_publicacion',
            'estado',
            'portada_url',
        ]


class LibroListSerializer(serializers.ModelSerializer):
    id_libro = serializers.IntegerField(source='id', read_only=True)
    genero = serializers.CharField(source='area', read_only=True)
    anio = serializers.IntegerField(source='anio_publicacion', read_only=True)
    isbn = serializers.CharField(source='codigo_libro', read_only=True)
    ejemplares = serializers.SerializerMethodField()
    ejemplares_disponibles = serializers.SerializerMethodField()
    portada_url = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = [
            'id',
            'id_libro',
            'codigo_libro',
            'isbn',
            'titulo',
            'autor',
            'area',
            'genero',
            'anio_publicacion',
            'anio',
            'estado',
            'portada_url',
            'ejemplares',
            'ejemplares_disponibles',
        ]

    def get_ejemplares(self, obj):
        return obj.ejemplares.count()

    def get_ejemplares_disponibles(self, obj):
        return obj.ejemplares.filter(disponibilidad='disponible').count()
    
    def get_portada_url(self, obj):
        request = self.context.get('request')
        if obj.portada:
            if request:
                return request.build_absolute_uri(obj.portada.url)
            return obj.portada.url
        return ''