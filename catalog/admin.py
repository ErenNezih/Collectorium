from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'get_full_path', 'created_at')
    list_filter = ('parent', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    list_select_related = ('parent',)
    
    # Show only top-level categories in parent dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_full_path(self, obj):
        """Display hierarchical path for categories"""
        if obj.parent:
            return f"{obj.parent.name} > {obj.name}"
        return obj.name
    get_full_path.short_description = 'Kategori Yolu'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'created_at')
    list_filter = ('category', 'brand', 'created_at')
    search_fields = ('name', 'brand', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)