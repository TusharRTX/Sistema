from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50)
    tamaño = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

