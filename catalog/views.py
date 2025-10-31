from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Category
from listings.models import Listing


def categories_list(request):
    """Kategoriler listesi sayfası"""
    # Show all main categories (parent=None) regardless of listing count
    # This ensures categories are visible even before any listings are created
    main_categories = Category.objects.filter(parent__isnull=True).annotate(
        listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
    ).order_by('name')
    
    # Get subcategories for each main category
    categories_with_children = []
    for main_cat in main_categories:
        children = Category.objects.filter(parent=main_cat).annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).order_by('name')
        categories_with_children.append({
            'main': main_cat,
            'children': children
        })
    
    context = {
        'categories_with_children': categories_with_children,
        'categories': main_categories,  # For backward compatibility
    }
    return render(request, 'catalog/categories_list.html', context)


def category_detail(request, slug):
    """Kategori detay sayfası - o kategorideki ilanları gösterir"""
    category = get_object_or_404(Category, slug=slug)
    
    # Kategorideki ilanlar (marketplace'e yönlendir)
    return render(request, 'catalog/category_detail.html', {'category': category})
