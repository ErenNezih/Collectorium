import django_filters
from .models import Category
from listings.models import Listing


class ListingFilter(django_filters.FilterSet):
    """
    Professional filtering system for marketplace listings.
    Supports category hierarchy and price range filtering.
    """
    
    # Category filter - supports both parent and child categories
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        method='filter_category',
        label='Kategori'
    )
    
    # Price range filters
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Minimum Fiyat'
    )
    
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Maksimum Fiyat'
    )
    
    # Condition filter
    condition = django_filters.ChoiceFilter(
        choices=Listing.CONDITION_CHOICES,
        label='Durum'
    )
    
    # Search filter
    search = django_filters.CharFilter(
        method='filter_search',
        label='Ara'
    )
    
    class Meta:
        model = Listing
        fields = ['category', 'condition', 'min_price', 'max_price']
    
    def filter_category(self, queryset, name, value):
        """
        Filter by category, including all child categories.
        """
        if value:
            # Get all child categories recursively
            child_categories = Category.objects.filter(
                parent=value
            ).values_list('id', flat=True)
            
            # Include the selected category and all its children
            category_ids = [value.id] + list(child_categories)
            
            return queryset.filter(product__category__id__in=category_ids)
        return queryset
    
    def filter_search(self, queryset, name, value):
        """
        Search across title, product name, brand, store name, and description.
        """
        if value:
            from django.db.models import Q
            return queryset.filter(
                Q(title__icontains=value) |
                Q(product__name__icontains=value) |
                Q(product__brand__icontains=value) |
                Q(store__name__icontains=value) |
                Q(description__icontains=value)
            )
        return queryset

