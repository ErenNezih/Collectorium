from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Category
from listings.models import Listing


def categories_list(request):
    """
    Ana kategori vitrini - Sadece ana kategorileri (parent=None) gösterir.
    FAILSAFE mantıkla yazılmıştır. Veritabanı boş olsa bile ASLA çökmemelidir.
    """
    main_categories = Category.objects.none()  # Default: boş queryset
    kategori_yok = False
    
    try:
        # Sadece ana kategorileri al (parent=None olanlar)
        main_categories = Category.objects.filter(parent__isnull=True).annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).order_by('name')
        
        # Eğer hiç kategori yoksa bayrağı ayarla
        if not main_categories.exists():
            kategori_yok = True
            
    except Exception:
        # Herhangi bir hata durumunda boş liste döndür
        main_categories = Category.objects.none()
        kategori_yok = True
    
    context = {
        'categories': main_categories,
        'kategori_yok': kategori_yok,
    }
    return render(request, 'catalog/categories_list.html', context)


def subcategory_list(request, parent_slug):
    """
    Alt kategori reyonları - Bir ana kategoriye tıklandığında alt kategorileri gösterir.
    FAILSAFE mantıkla yazılmıştır. Veritabanı boş olsa bile ASLA çökmemelidir.
    """
    parent_category = None
    subcategories = Category.objects.none()  # Default: boş queryset
    kategori_yok = False
    
    try:
        # Ana kategoriyi bul
        parent_category = get_object_or_404(Category, slug=parent_slug, parent__isnull=True)
        
        # Bu ana kategorinin alt kategorilerini al
        subcategories = Category.objects.filter(parent=parent_category).annotate(
            listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
        ).order_by('name')
        
        # Eğer hiç alt kategori yoksa bayrağı ayarla
        if not subcategories.exists():
            kategori_yok = True
            
    except Exception:
        # Herhangi bir hata durumunda boş liste döndür
        subcategories = Category.objects.none()
        kategori_yok = True
    
    context = {
        'parent_category': parent_category,
        'subcategories': subcategories,
        'kategori_yok': kategori_yok,
    }
    return render(request, 'catalog/subcategory_list.html', context)


def category_detail(request, slug):
    """Kategori detay sayfası - o kategorideki ilanları gösterir"""
    category = get_object_or_404(Category, slug=slug)
    
    # Kategorideki ilanlar (marketplace'e yönlendir)
    return render(request, 'catalog/category_detail.html', {'category': category})
