from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Order, Item
from django.http import JsonResponse
from django.db.models import Sum, Avg
from django.conf import settings

def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html',
                  {'template_data': template_data})


def trending_map(request):
    template_data = {
        'title': 'Local popularity map',
        'google_maps_api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
    return render(request, 'home/trending_map.html', {'template_data': template_data})

def api_trending_regions(request):
    region_qs = (
        Order.objects.filter(city__isnull=False)
        .exclude(city='')
        .values('city', 'country')
        .annotate(avg_lat=Avg('latitude'), avg_lng=Avg('longitude'))
    )
    regions = []
    for r in region_qs:
        city, country = r['city'], r['country']
        lat, lng = r['avg_lat'], r['avg_lng']
        if lat is None:
            lat = 0.0
        if lng is None:
            lng = 0.0
        items = (
            Item.objects.filter(order__city=city, order__country=country)
            .values('movie_id', 'movie__name')
            .annotate(total=Sum('quantity'))
            .order_by('-total')[:3]
        )
        top_movies = [{'id': x['movie_id'], 'name': x['movie__name'], 'count': x['total']} for x in items]
        regions.append({
            'city': city,
            'country': country,
            'lat': float(lat),
            'lng': float(lng),
            'top_movies': top_movies,
        })

    user_purchases = []
    if request.user.is_authenticated:
        user_items = (
            Item.objects.filter(order__user=request.user)
            .values('movie_id', 'movie__name')
            .annotate(total=Sum('quantity'))
            .order_by('-total')
        )
        user_purchases = [{'id': x['movie_id'], 'name': x['movie__name'], 'count': x['total']} for x in user_items]

    return JsonResponse({'regions': regions, 'my_purchases': user_purchases})
