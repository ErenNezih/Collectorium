from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Category
from listings.models import Listing


def categories_list(request):
    """
    Kategoriler listesi sayfası - FAILSAFE mantıkla yazılmıştır.
    Veritabanı boş olsa bile ASLA çökmemelidir.
    """
    main_categories = Category.objects.none()  # Default: boş queryset
    categories_with_children = []
    kategori_yok = False
    
    try:
        # Tüm ana kategorileri al (listing sayısı önemli değil)
        main_categories = Category.objects.filter(parent__isnull=True).annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).order_by('name')
        
        # Alt kategorileri ekle
        for main_cat in main_categories:
            try:
                children = Category.objects.filter(parent=main_cat).annotate(
                    listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
                ).order_by('name')
                categories_with_children.append({
                    'main': main_cat,
                    'children': children
                })
            except Exception:
                # Bir kategori için hata varsa, sadece ana kategoriyi ekle
                categories_with_children.append({
                    'main': main_cat,
                    'children': Category.objects.none()
                })
        
        # Eğer hiç kategori yoksa bayrağı ayarla
        if not main_categories.exists():
            kategori_yok = True
            
    except Exception:
        # Herhangi bir hata durumunda boş liste döndür
        main_categories = Category.objects.none()
        categories_with_children = []
        kategori_yok = True
    
    context = {
        'categories_with_children': categories_with_children,
        'categories': main_categories,  # For backward compatibility
        'kategori_yok': kategori_yok,  # Template için bayrak
    }
    return render(request, 'catalog/categories_list.html', context)


def category_detail(request, slug):
    """Kategori detay sayfası - o kategorideki ilanları gösterir"""
    category = get_object_or_404(Category, slug=slug)
    
    # Kategorideki ilanlar (marketplace'e yönlendir)
    return render(request, 'catalog/category_detail.html', {'category': category})
