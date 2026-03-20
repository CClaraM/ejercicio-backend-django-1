from django.conf import settings
from django.db import models


class Libro(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
    ]

    codigo_libro = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    area = models.CharField(max_length=100, blank=True, null=True)
    anio_publicacion = models.PositiveIntegerField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='disponible'
    )
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)

    class Meta:
        db_table = 'libros'

    def __str__(self):
        return self.titulo


class EjemplarLibro(models.Model):
    CONDICIONES = [
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
    ]

    DISPONIBILIDADES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='ejemplares',
        db_column='id_libro'
    )
    codigo_inventario = models.CharField(max_length=80, unique=True)
    condicion = models.CharField(
        max_length=20,
        choices=CONDICIONES,
        default='bueno'
    )
    disponibilidad = models.CharField(
        max_length=20,
        choices=DISPONIBILIDADES,
        default='disponible'
    )

    class Meta:
        db_table = 'ejemplares_libro'

    def __str__(self):
        return f'{self.codigo_inventario} - {self.libro.titulo}'


class SolicitudPrestamo(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes',
        db_column='id_usuario'
    )
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='solicitudes',
        db_column='id_libro'
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )
    observacion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'solicitudes_prestamo'

    def __str__(self):
        return f'Solicitud {self.id} - {self.usuario}'


class Prestamo(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prestamos',
        db_column='id_usuario'
    )
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='prestamos',
        db_column='id_libro'
    )
    ejemplar = models.ForeignKey(
        EjemplarLibro,
        on_delete=models.CASCADE,
        related_name='prestamos',
        db_column='id_ejemplar'
    )
    fecha_prestamo = models.DateField()
    fecha_vencimiento = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='activo'
    )

    class Meta:
        db_table = 'prestamos'

    def __str__(self):
        return f'Préstamo {self.id} - {self.usuario}'


class Devolucion(models.Model):
    prestamo = models.OneToOneField(
        Prestamo,
        on_delete=models.CASCADE,
        related_name='devolucion',
        db_column='id_prestamo'
    )
    fecha_devolucion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'devoluciones'

    def __str__(self):
        return f'Devolución {self.id} - préstamo {self.prestamo_id}'