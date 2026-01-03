from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categoria/<int:id>/', views.productos_categoria, name='productos_categoria'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('catalogo/', views.catalogo, name='catalogo'),

    # PDF
    path('catalogo/pdf/', views.preview_pdf, name='preview_pdf'),
]
