"""
Collectorium - Google OAuth Kurulum Komutu
AEGIS Operasyonu - Yönetim Kolaylığı

Bu komut, Google OAuth entegrasyonu için gerekli Site nesnesini
otomatik olarak oluşturur ve yapılandırır.

Kullanım:
    python manage.py setup_google_oauth
"""

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Google OAuth entegrasyonu için Site ayarlarını yapılandırır'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('='*60))
        self.stdout.write(self.style.HTTP_INFO('COLLECTORIUM - GOOGLE OAUTH KURULUM'))
        self.stdout.write(self.style.HTTP_INFO('='*60))
        self.stdout.write('')

        # Site nesnesini kontrol et veya oluştur
        try:
            site = Site.objects.get(pk=1)
            self.stdout.write(self.style.WARNING(f'✓ Mevcut site bulundu: {site.domain}'))
            
            # Eğer varsayılan example.com ise, güncelle
            if site.domain == 'example.com':
                site.domain = '127.0.0.1:8000'
                site.name = 'Collectorium (Development)'
                site.save()
                self.stdout.write(self.style.SUCCESS('✓ Site bilgileri güncellendi!'))
                self.stdout.write(self.style.SUCCESS(f'  Domain: {site.domain}'))
                self.stdout.write(self.style.SUCCESS(f'  Name: {site.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'  Site zaten yapılandırılmış: {site.name}'))
        
        except Site.DoesNotExist:
            site = Site.objects.create(
                pk=1,
                domain='127.0.0.1:8000',
                name='Collectorium (Development)'
            )
            self.stdout.write(self.style.SUCCESS('✓ Yeni site oluşturuldu!'))
            self.stdout.write(self.style.SUCCESS(f'  Domain: {site.domain}'))
            self.stdout.write(self.style.SUCCESS(f'  Name: {site.name}'))
        
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('='*60))
        self.stdout.write(self.style.HTTP_INFO('SONRAKİ ADIMLAR'))
        self.stdout.write(self.style.HTTP_INFO('='*60))
        self.stdout.write('')
        self.stdout.write('1. Django Admin paneline giriş yapın:')
        self.stdout.write(self.style.HTTP_REDIRECT('   http://127.0.0.1:8000/admin/'))
        self.stdout.write('')
        self.stdout.write('2. "Social applications" bölümünü bulun')
        self.stdout.write('')
        self.stdout.write('3. "Add social application" butonuna tıklayın')
        self.stdout.write('')
        self.stdout.write('4. Formu doldurun:')
        self.stdout.write('   - Provider: Google')
        self.stdout.write('   - Name: Google OAuth')
        self.stdout.write('   - Client id: Google Cloud Console\'dan aldığınız Client ID')
        self.stdout.write('   - Secret key: Google Cloud Console\'dan aldığınız Secret')
        self.stdout.write(f'   - Sites: "{site.name}" seçin')
        self.stdout.write('')
        self.stdout.write('5. "Save" butonuna tıklayın')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✓ AEGIS Operasyonu hazır! Google ile giriş aktive edilmeye hazır.'))
        self.stdout.write('')

