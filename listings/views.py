from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .models import Listing, ListingImage
from .forms import ListingForm, ImageUploadForm
from stores.models import Store
from accounts.mixins import SellerRequiredMixin
from .mixins import ListingOwnerRequiredMixin
from cart.forms import CartAddListingForm

class ListingCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('my_listings') # Bu URL'i birazdan oluşturacağız

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_form'] = ImageUploadForm(self.request.POST, self.request.FILES)
        else:
            context['image_form'] = ImageUploadForm()
        context['page_title'] = "Yeni İlan Oluştur"
        return context

    def form_valid(self, form):
        # Formdan gelen ilanı veritabanına kaydetmeden önce mağaza bilgisini ata
        form.instance.store = self.request.user.store
        
        image_form = ImageUploadForm(self.request.POST, self.request.FILES)
        
        if image_form.is_valid():
            # form_valid'e gelindiğinde 'form' zaten valid'dir.
            # Sadece image_form'u kontrol etmemiz yeterli.
            self.object = form.save()
            
            images = self.request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=self.object, image=image)
            
            messages.success(self.request, "İlanınız başarıyla oluşturuldu.")
            return redirect(self.get_success_url())
        
        messages.error(self.request, "Lütfen formdaki hataları düzeltin.")
        return self.form_invalid(form)

class ListingUpdateView(LoginRequiredMixin, SellerRequiredMixin, ListingOwnerRequiredMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html' # Oluşturma formunu yeniden kullanıyoruz
    success_url = reverse_lazy('my_listings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Şablonun başlığını dinamik olarak değiştiriyoruz
        context['page_title'] = "İlanı Düzenle"
        
        # Resim formu şimdilik boş kalabilir, resim yönetimi ayrı bir adım olacak
        context['image_form'] = ImageUploadForm() 
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('store', None)
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" ilanınız başarıyla güncellendi.')
        return super().form_valid(form)

class ListingDeleteView(LoginRequiredMixin, SellerRequiredMixin, ListingOwnerRequiredMixin, DeleteView):
    model = Listing
    template_name = 'listings/listing_confirm_delete.html'
    success_url = reverse_lazy('my_listings')

    def form_valid(self, form):
        # Mesajı, nesne silinmeden önce oluşturuyoruz.
        messages.success(self.request, f'"{self.object.title}" başlıklı ilanınız başarıyla silindi.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Şablona, silinecek ilanın kendisini ve bir sayfa başlığını gönderiyoruz
        context['listing'] = self.get_object()
        context['page_title'] = "İlanı Sil"
        return context

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listing_detail.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_add_form'] = CartAddListingForm()
        return context
