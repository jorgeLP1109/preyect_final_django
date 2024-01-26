# En views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem
from .forms import ProductForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.conf import settings
from django.http import JsonResponse
import requests

@login_required(login_url='/login/')  # Redirects unauthenticated users to the login page
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# En tu views.py
from django.shortcuts import render, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Verifica si el producto ya está en el carrito
    if not user_cart.products.filter(id=product.id).exists():
        # Si no está en el carrito, añádelo
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    else:
        # Si ya está en el carrito, incrementa la cantidad
        cart_item = CartItem.objects.get(cart=user_cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    
    total_price = cart_item.total_price()  # Utiliza el método de la clase CartItem para calcular el total
    
    return render(request, 'cart.html', {'cart': user_cart, 'total_price': total_price})


def update_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user_cart = Cart.objects.get(user=request.user)
    quantity = int(request.POST['quantity'])

    cart_product = user_cart.products.through.objects.get(product=product, cart=user_cart)
    cart_product.quantity = quantity
    cart_product.save()

    return redirect('cart')

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user_cart = Cart.objects.get(user=request.user)

    user_cart.products.remove(product)

    return redirect('cart')

def cart_view(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': user_cart})

def checkout(request):
    if request.method == 'POST':
        # Lógica de procesamiento de pago con Instapago
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        total_amount = user_cart.calculate_total()

        payload = {
            'KeyId': settings.INSTAPAGO_KEY_ID,
            'PublicKeyId': settings.INSTAPAGO_PUBLIC_KEY,
            'Amount': total_amount,
            # Agrega más campos según sea necesario
        }

        # Resto de la lógica para la API de Instapago

        # Después de procesar el pago, puedes redirigir a una página de éxito
        return render(request, 'payment_success.html')
    else:
        # Maneja el caso de solicitud GET (si es necesario)
        return HttpResponse("Método no permitido")

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = [product.image, product.image_2, product.image_3, product.image_4, product.image_5]
    # Filtrar imágenes no nulas
    images = [image for image in images if image]

    return render(request, 'product_detail.html', {'product': product, 'images': images})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'product_create.html', {'form': form})

@login_required
def edit_product(request, id_producto):
    # Obtén el producto específico o redirecciona si no se encuentra
    product = get_object_or_404(Product, id=id_producto)

    # Asegúrate de que solo los administradores puedan editar productos
    if not request.user.is_staff:
        return redirect('product_list')

    if request.method == 'POST':
        # Si se envió el formulario, procesa la información
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        # Si es una solicitud GET, muestra el formulario con los datos actuales del producto
        form = ProductForm(instance=product)

    return render(request, 'product_edit.html', {'form': form, 'product': product})
def custom_login(request):
    # Lógica de la vista login
    return render(request, 'login.html')


class CustomLogoutView(LogoutView):
    # Lógica personalizada si es necesario
    
    
    pass   

def home(request):
    return render(request, 'home.html')

def otra_vista(request):
    # Puedes agregar lógica adicional aquí si es necesario

    # Datos que puedes pasar a la plantilla (puedes personalizar según tus necesidades)
    data = {
        'titulo': 'Bienvenido a Mi Tienda',
        'mensaje': 'Explora nuestra increíble selección de productos.',
    }

    # Renderiza la plantilla 'home.html' con los datos proporcionados
    return render(request, 'home.html', data)


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')
    
def payment_view(request):
    if request.method == 'POST':
        # Recupera la información del formulario o el objeto del carrito
        amount = request.POST.get('amount')
        card_holder = request.POST.get('card_holder')
        card_number = request.POST.get('card_number')
        expiration_date = request.POST.get('expiration_date')
        cvc = request.POST.get('cvc')

        # Construye la solicitud a la API de Instapago
        payload = {
            'KeyID': settings.INSTAPAGO_API_KEY,
            'Amount': amount,
            'Description': 'Descripción de la compra',
            'CardHolder': card_holder,
            'CardNumber': card_number,
            'ExpirationDate': expiration_date,
            'CVC': cvc,
        }

        response = requests.post(settings.INSTAPAGO_API_URL, json=payload)

        # Procesa la respuesta de la API
        if response.status_code == 200:
            # Pago exitoso
            return JsonResponse({'message': 'Pago exitoso'})
        else:
            # Pago fallido
            return JsonResponse({'message': 'Error en el pago'})

    return render(request, 'payment.html')  # Asegúrate de tener un template payment.html    
