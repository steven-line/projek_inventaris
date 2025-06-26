

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib import messages

from .models import * 
from django.views import generic
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from .models import Peminjaman
# users/views.py
from django.contrib.auth.decorators import login_required



@login_required
def redirect_after_login(request):
    user = request.user
    if user.groups.filter(name='staff_me').exists():
        return redirect('/staff-me/dashboard/')
    else:
        return redirect('/catalog/')

@login_required
def barang_rusak_list (request):
    barang_rusak = Inventaris.objects.filter(kondisi='rusak')
    paginator = Paginator(barang_rusak, 25) 
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'barang_rusak_list': barang_rusak,
        'page_obj': page_obj
    }
    return render(request, 'catalog/list_barang_rusak.html', context)
# catalog/views.py

@login_required
def index(request):
    total_barang = Inventaris.objects.count()
    total_barang_baik = Inventaris.objects.filter(kondisi='baik').count()
    total_barang_rusak = Inventaris.objects.filter(kondisi='rusak').count()
    announcement = Announcement.objects.latest('created_at')
    aktivitas_terbaru = PemindahanDetail.objects.select_related(
        'inventaris', 'lokasi_tujuan', 'pemindahan'
    ).order_by('-pemindahan__created_at')[:3]
    context = {
        'aktivitas_terbaru': aktivitas_terbaru,
        'total_barang': total_barang,
        'total_barang_baik': total_barang_baik,
        'total_barang_rusak': total_barang_rusak,
        'announcement': announcement

    }
    return render(request, 'index.html', context)
   



class BarangListView(LoginRequiredMixin, ListView):
    model = Barang
    template_name = 'catalog/barang_list.html'  # Tentukan template yang akan digunakan
    context_object_name = 'list_barang'  # Nama variabel yang akan diteruskan ke template
    paginate_by = 5  # Menentukan jumlah barang per halaman

    def get_queryset(self):
        '''
        Menyesuaikan queryset untuk mendapatkan semua barang
        beserta jenis_barang dan inventaris yang relevan.
        '''
        list_barang = super().get_queryset()  # Ambil semua barang
        jenis_barang = JenisBarang.objects.all()
        detail_barang = Inventaris.objects.all()
        
        # Menambahkan total stok per barang
        for barang in list_barang:

        
            inventaris = Inventaris.objects.filter(barang=barang).count()
            total_stok = inventaris
            barang.total_stok = total_stok

        self.extra_context = {
            'jenis_barang': jenis_barang,
            'inventaris': detail_barang,
            'total_stok': total_stok
        }
        return list_barang

    
@login_required
def ajukan_pengembalian(request, pk):
    peminjaman = get_object_or_404(Peminjaman, pk=pk, user=request.user)

    if peminjaman.status != 'approved':
        messages.error(request, "Pengembalian hanya bisa diajukan untuk peminjaman yang disetujui.")
        return redirect('pinjam-barang')  

    peminjaman.status = 'pengembalian_diajukan'
    peminjaman.save()
    messages.success(request, "Pengajuan pengembalian berhasil dikirim. Menunggu validasi staff.")
    return redirect('pinjam-barang')

    
@login_required
def batalkan_peminjaman(request, pk):
    peminjaman = get_object_or_404(Peminjaman, pk=pk, user=request.user)
    if peminjaman.status != 'pending':
        messages.error(request, "Pembatalan hanya bisa diajukan untuk peminjaman yang pending.")
        return redirect('pinjam-barang') 

   
    peminjaman.status = 'peminjaman_dibatalkan'
    peminjaman.save()
    return redirect('pinjam-barang')


class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Barang
    context_object_name = 'items_detail'   
    template_name = 'catalog/items_detail.html' 
  

class RentalListView(LoginRequiredMixin, generic.ListView):
    model = Peminjaman
    template_name = 'catalog/pinjam_barang.html' 
    context_object_name = 'list_rental'
    
    def get_queryset(self):
        return Peminjaman.objects.filter(user=self.request.user)
        

class RentalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Peminjaman
    
    template_name = 'catalog/pinjam_barang_detail.html'



from catalog.forms import PeminjamanForm, PeminjamanDetailFormSet
from django.forms import inlineformset_factory



@login_required
def create_peminjaman(request):
    DetailFormSet = inlineformset_factory(
      Peminjaman,
      PeminjamanDetail,
      form=PeminjamanDetailInlineForm,
      formset= PeminjamanDetailFormSet,
      fields=('barang', 'jumlah'),
      extra=0,
      can_delete=False,
      validate_min=True,
      min_num=1
    )
   
    if request.method == "POST":
        peminjaman_form = PeminjamanForm(request.POST)
        formset = DetailFormSet(request.POST)

        if peminjaman_form.is_valid() and formset.is_valid():
            peminjaman = peminjaman_form.save(commit=False)
            peminjaman.user = request.user
            peminjaman.save()
            details = formset.save(commit=False)
            for detail in details:
                detail.peminjaman = peminjaman
                detail.save()

            return redirect('pinjam-barang') 
    else:
        peminjaman_form = PeminjamanForm()
        formset = DetailFormSet()

    context = {
        'peminjaman_form': peminjaman_form,
        'peminjaman_detail_formset': formset
    }
    return render(request, 'catalog/pinjam_form.html', context)


