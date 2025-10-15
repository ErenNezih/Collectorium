from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Category
from listings.models import Listing


def categories_list(request):
    """Kategoriler listesi sayfası"""
    categories = Category.objects.annotate(
        listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
    ).filter(listing_count__gt=0).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'catalog/categories_list.html', context)


def category_detail(request, slug):
    """Kategori detay sayfası - o kategorideki ilanları gösterir"""
    category = get_object_or_404(Category, slug=slug)
    
    # Kategorideki ilanlar (marketplace'e yönlendir)
    return render(request, 'catalog/category_detail.html', {'category': category})
