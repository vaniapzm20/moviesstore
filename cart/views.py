from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())

    if (movie_ids == []):
        return redirect('cart.index')
    
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['google_maps_api_key'] = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    template_data['cart_total'] = cart_total
    template_data['cart'] = cart

    if request.method == "POST": 
        city = (request.POST.get('city') or '').strip()
        country= (request.POST.get('country') or '').strip()
        place_id = (request.POST.get('place_id') or '').strip()
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
    
        if not city or not country or not place_id:
            messages.error(request, 
                        'Please select your location using the search box. '
                        'Location is required to complete your purchase.')
            return render(request, 'cart/checkout.html', {'template_data': template_data})
        
        order = Order()
        order.user = request.user
        order.total = cart_total
        order.city = city
        order.country = country
        order.place_id = place_id

        if lat and lng:
            try: 
                order.latitude = float(lat)
                order.longitude = float(lng)
            except (TypeError, ValueError):
                pass
        order.save()

        for movie in movies_in_cart:
            item = Item()
            item.movie = movie
            item.price = movie.price
            item.order = order
            item.quantity = cart[str(movie.id)]
            item.save()

        request.session['cart'] = {}

        template_data = {
            'title': 'Purchase confirmation',
            'order_id': order.id,
        }
        return render(request, 'cart/purchase.html', {'template_data': template_data})

    return render(request, 'cart/checkout.html', {'template_data': template_data})


