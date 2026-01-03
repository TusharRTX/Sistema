from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto
from .forms import ProductoForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Categoria


def preview_pdf(request):
    categorias_ids = request.GET.getlist('categorias')

    categorias = Categoria.objects.filter(
        id__in=categorias_ids,
        activa=True
    ).prefetch_related('producto_set')

    # 🔥 Construir URLs absolutas de imágenes
    for categoria in categorias:
        for producto in categoria.producto_set.all():
            if producto.imagen:
                producto.imagen_url = request.build_absolute_uri(producto.imagen.url)
            else:
                producto.imagen_url = ''

    template = get_template('catalogo_pdf.html')
    html = template.render({
        'categorias': categorias
    })

    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)

    response = HttpResponse(
        result.getvalue(),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = 'inline; filename="catalogo.pdf"'
    return response



def menu(request):
    return render(request, 'menu.html')

def crear_producto(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        producto = form.save()
        return redirect('productos_categoria', producto.categoria.id)

    return render(request, 'crear_producto.html', {'form': form})


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)

    if form.is_valid():
        form.save()
        return redirect('productos_categoria', producto.categoria.id)

    return render(request, 'crear_producto.html', {
        'form': form,
        'editar': True
    })


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categoria_id = producto.categoria.id
    producto.delete()
    return redirect('productos_categoria', categoria_id)


def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})


def productos_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    productos = Producto.objects.filter(categoria=categoria)

    return render(request, 'productos_categoria.html', {
        'categoria': categoria,
        'productos': productos
    })


def catalogo(request):
    categorias = Categoria.objects.filter(activa=True)
    return render(request, 'catalogo.html', {'categorias': categorias})

