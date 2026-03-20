from django.urls import path
from .views import MisPrestamosView, LibrosListView, AdminLibroCreateView, AdminImportLibrosView, AdminLibroUpdateView, AdminLibroPortadaUploadView

urlpatterns = [
    path('me/prestamos/', MisPrestamosView.as_view(), name='mis_prestamos'),
    path('libros/', LibrosListView.as_view(), name='libros_list'),
    path('admin/libros/', AdminLibroCreateView.as_view(), name='admin_libros_create'),
    path('admin/import/libros/', AdminImportLibrosView.as_view(), name='admin_import_libros'),
    path('admin/libros/<int:id>/', AdminLibroUpdateView.as_view(), name='admin_libros_update'),
    path('admin/libros/<int:id>/portada/', AdminLibroPortadaUploadView.as_view(), name='admin_libros_portada'),
]