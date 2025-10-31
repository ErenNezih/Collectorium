# Generated migration for Collectorium category system
# This migration adds 8 main categories and ~72 subcategories

from django.db import migrations


def create_categories(apps, schema_editor):
    """
    Create the complete category hierarchy for Collectorium.
    """
    Category = apps.get_model('catalog', 'Category')
    db_alias = schema_editor.connection.alias
    
    # CRITICAL: Fix collation for name and slug fields (MariaDB/MySQL specific)
    # Both fields need utf8mb4 to support Turkish characters (ı, ğ, ü, ş, ç, ö)
    with schema_editor.connection.cursor() as cursor:
        try:
            # Fix name column collation to utf8mb4 (required for Turkish characters)
            cursor.execute("""
                ALTER TABLE catalog_category 
                MODIFY COLUMN name VARCHAR(100) 
                CHARACTER SET utf8mb4 
                COLLATE utf8mb4_general_ci
            """)
            
            # Fix slug column collation to utf8mb4
            cursor.execute("""
                ALTER TABLE catalog_category 
                MODIFY COLUMN slug VARCHAR(100) 
                CHARACTER SET utf8mb4 
                COLLATE utf8mb4_general_ci
            """)
        except Exception as e:
            # If we can't fix collation, log but continue
            # The raw SQL approach below will handle queries
            import sys
            print(f"Warning: Could not fix collation: {e}", file=sys.stderr)
    
    # Main categories data structure
    categories_data = {
        'Koleksiyon Kartları (TCG & Spor)': [
            'Pokémon Kartları',
            'Magic: The Gathering (MTG) Kartları',
            'Yu-Gi-Oh! Kartları',
            'Lorcana Kartları',
            'One Piece Card Game',
            'Flesh and Blood Kartları',
            'Futbolcu Kartları (Panini, Topps vb.)',
            'Basketbol Kartları (NBA vb.)',
            'Telefon Kartları & Artist Kartları',
            'Diğer Oyun Kartları',
        ],
        'Figürler & Oyuncaklar': [
            'Aksiyon Figürleri (Genel)',
            'Star Wars Figürleri',
            'Marvel Figürleri',
            'DC Comics Figürleri',
            'Funko Pop! Figürleri',
            'Heykeller & Büstler (Statues)',
            'Anime & Manga Figürleri',
            'LEGO (Setler & Minifigürler)',
            'Vintage & Retro Oyuncaklar',
            'Minyatürler & Masaüstü Oyun Figürleri',
        ],
        'Çizgi Roman & Kitap': [
            'ABD Çizgi Romanları (Floppies & Ciltler)',
            'Nostaljik Türk Çizgi Romanları (Teksas, Tommiks, Zagor vb.)',
            'Manga (Japon Çizgi Romanları)',
            'Gerekli Şeyler Yayınları',
            'Marmara Çizgi Yayınları',
            'JBC Yayıncılık & Diğerleri',
            'Nadir & İlk Baskı Kitaplar',
            'İmzalı Kitaplar & Çizgi Romanlar',
            'Fanzinler & Bağımsız Yayınlar',
            'Efemera (Gazete, Dergi, Broşür)',
        ],
        'Para & Pul (Nümismatik & Filateli)': [
            'Osmanlı Dönemi Paraları (Akçe, Kuruş vb.)',
            'Cumhuriyet Dönemi Madeni Paraları',
            'Cumhuriyet Dönemi Kağıt Paraları',
            'Antik & Roma Paraları',
            'Yabancı Madeni & Kağıt Paralar',
            'Osmanlı & Erken Dönem Pullar',
            'Cumhuriyet Dönemi Pulları',
            'Yabancı Ülke Pulları',
            'Madalyalar, Nişanlar ve Rozetler',
            'Jetonlar & Markalar',
        ],
        'Müzik & Sinema Objeleri': [
            'Plaklar (Vinil) - 33\'lük LP',
            'Plaklar (Vinil) - 45\'lik',
            'Kasetler',
            'Nadir CD\'ler & Müzik Setleri',
            'Film Afişleri & Posterler',
            'Lobi Kartları & Sinema Fotoğrafları',
            'Konser Biletleri, Broşürleri ve Hatıraları',
            'İmzalı Objeler & Fotoğraflar',
            'Müzik & Sinema Dergileri',
            'Enstrümanlar & Müzik Ekipmanları',
        ],
        'Model & Diecast Araçlar': [
            'Hot Wheels & Matchbox',
            '1:18 Ölçekli Model Arabalar',
            '1:24 Ölçekli Model Arabalar',
            '1:43 Ölçekli Model Arabalar',
            '1:64 Ölçekli Model Arabalar',
            'Model Kitler (Maket - Uçak, Gemi, Araba)',
            'Askeri Modeller (Tank, Uçak vb.)',
            'Trenler & Demiryolu Modelleri',
            'Figürlü Dioramalar ve Setler',
            'Uzaktan Kumandalı Modeller',
        ],
        'Antika & Sanat Objeleri': [
            'Antika Mobilya & Dekorasyon',
            'Porselen & Seramik Objeler (Tabak, Vazo vb.)',
            'Cam Objeler & Murano',
            'Tablolar (Yağlı Boya, Suluboya vb.)',
            'Heykeller & Büstler',
            'Antika Saatler (Cep, Masa, Duvar)',
            'Gümüş & Değerli Objeler',
            'Tarihi Belgeler & El Yazmaları',
            'Antika Silahlar & Kılıçlar',
            'Halı & Kilim',
        ],
        'Popüler Kültür & Hobi Objeleri': [
            'Tespihler',
            'Çakmaklar (Zippo vb.) & Tütün Objeleri',
            'Anahtarlıklar & Pinler',
            'Kutu Oyunları (Board Games) & Puzzle\'lar',
            'Promosyonel & Markalı Ürünler (Coca-Cola vb.)',
            'Koleksiyonluk Bıçaklar & Çakılar',
            'Kalemler & Yazı Gereçleri',
            'Koleksiyon Aksesuarları (Albüm, Stand, Koruyucu)',
            'Şişe Kapakları & Bardak Altlıkları',
            'Diğer Hobi & Popüler Kültür Ürünleri',
        ],
    }
    
    # Helper function to create slug
    def create_slug(name):
        import re
        slug = name.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars except spaces and hyphens
        slug = re.sub(r'[-\s]+', '-', slug)  # Replace spaces and multiple hyphens with single hyphen
        slug = slug.strip('-')  # Remove leading/trailing hyphens
        return slug
    
    # Create main categories and their children
    # CRITICAL: Use raw SQL for existence check to avoid collation issues
    # This bypasses Django ORM's collation handling
    db_alias = schema_editor.connection.alias
    
    for main_category_name, subcategories in categories_data.items():
        # Create main category - use raw SQL to check existence (collation-safe)
        main_slug = create_slug(main_category_name)
        
        # Check existence using raw SQL with BINARY comparison (collation-safe)
        # BINARY forces byte-by-byte comparison, bypassing collation entirely
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("""
                SELECT id FROM catalog_category 
                WHERE BINARY slug = BINARY %s
                LIMIT 1
            """, [main_slug])
            result = cursor.fetchone()
            main_category_id = result[0] if result else None
        
        if main_category_id:
            main_category = Category.objects.using(db_alias).get(pk=main_category_id)
        else:
            main_category = Category.objects.using(db_alias).create(
                name=main_category_name,
                slug=main_slug,
                parent=None,
            )
        
        # Create subcategories - use raw SQL for existence check
        for subcategory_name in subcategories:
            sub_slug = create_slug(subcategory_name)
            
            with schema_editor.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM catalog_category 
                    WHERE BINARY slug = BINARY %s
                    LIMIT 1
                """, [sub_slug])
                result = cursor.fetchone()
                sub_category_id = result[0] if result else None
            
            if not sub_category_id:
                Category.objects.using(db_alias).create(
                    name=subcategory_name,
                    slug=sub_slug,
                    parent=main_category,
                )


def reverse_categories(apps, schema_editor):
    """
    Remove the categories created by this migration.
    """
    Category = apps.get_model('catalog', 'Category')
    db_alias = schema_editor.connection.alias
    
    # Helper function to create slug (same as forward migration)
    def create_slug(name):
        import re
        slug = name.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    # Delete in reverse order (children first, then parents)
    # Use raw SQL to avoid collation issues
    main_category_names = [
        'Koleksiyon Kartları (TCG & Spor)',
        'Figürler & Oyuncaklar',
        'Çizgi Roman & Kitap',
        'Para & Pul (Nümismatik & Filateli)',
        'Müzik & Sinema Objeleri',
        'Model & Diecast Araçlar',
        'Antika & Sanat Objeleri',
        'Popüler Kültür & Hobi Objeleri',
    ]
    
    for main_name in main_category_names:
        main_slug = create_slug(main_name)
        
        # Find category using raw SQL with BINARY comparison (collation-safe)
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("""
                SELECT id FROM catalog_category 
                WHERE BINARY slug = BINARY %s
                AND parent_id IS NULL
                LIMIT 1
            """, [main_slug])
            result = cursor.fetchone()
            category_id = result[0] if result else None
        
        if category_id:
            category = Category.objects.using(db_alias).get(pk=category_id)
            # Delete all children first
            Category.objects.using(db_alias).filter(parent=category).delete()
            # Then delete the parent
            category.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_product_brand_index'),
    ]

    operations = [
        migrations.RunPython(create_categories, reverse_categories),
    ]

