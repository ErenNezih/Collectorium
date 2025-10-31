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
    debug_info = {}  # Debug için
    
    try:
        # DEBUG: Önce tüm kategorileri kontrol et
        all_categories_count = Category.objects.count()
        debug_info['all_categories_count'] = all_categories_count
        
        # DEBUG: Ana kategorileri say
        main_categories_count = Category.objects.filter(parent__isnull=True).count()
        debug_info['main_categories_count'] = main_categories_count
        
        # Sadece ana kategorileri al (parent=None olanlar)
        # Annotation'ı güvenli hale getir - eğer hata verirse basit sorgu kullan
        try:
            main_categories = Category.objects.filter(parent__isnull=True).annotate(
                listing_count=Count('products__listings', filter=Q(products__listings__is_active=True))
            ).order_by('name')
        except Exception as annot_error:
            # Annotation hatası varsa, basit sorgu kullan
            debug_info['annotation_error'] = str(annot_error)
            main_categories = Category.objects.filter(parent__isnull=True).order_by('name')
        
        # Eğer hiç kategori yoksa bayrağı ayarla
        if not main_categories.exists():
            kategori_yok = True
            debug_info['reason'] = 'No categories found in database'
        else:
            debug_info['found_categories'] = main_categories.count()
            
    except Exception as e:
        # Herhangi bir hata durumunda boş liste döndür
        main_categories = Category.objects.none()
        kategori_yok = True
        debug_info['error'] = str(e)
    
    context = {
        'categories': main_categories,
        'kategori_yok': kategori_yok,
        'debug_info': debug_info,  # Template'de gösterilecek
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
