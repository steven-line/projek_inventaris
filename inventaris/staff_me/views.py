
from .decorators import staff_me_required 
# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count, Sum, Q
from catalog.models import Barang, Lokasi, Peminjaman, Inventaris
from django.forms import inlineformset_factory
@login_required
@staff_me_required
def dashboard(request):
    total_barang = Barang.objects.count()
    total_lokasi = Lokasi.objects.count()
    peminjaman_baru = Peminjaman.objects.filter(status='pending').count()
    peminjaman = Peminjaman.objects.filter(status='ápproved')
    peminjaman_detail = PeminjamanDetail.objects.filter(peminjaman__in=peminjaman)
    peminjaman_unit = PeminjamanUnit.objects.filter(peminjaman_detail__in=peminjaman_detail).count()
    total_unit_rusak = Inventaris.objects.filter(kondisi='rusak').count() 
    context = {
        'total_barang': total_barang,
        'total_lokasi': total_lokasi,
        'peminjaman_baru': peminjaman_baru,
        'peminjaman_unit': peminjaman_unit,
        'total_unit_rusak': total_unit_rusak
     
       
    }
    return render(request, 'staff_me/dashboard.html', context)


@login_required
@staff_me_required
def create_barang(request):
    context = {}
    if request.method == 'POST':
        form = BarangForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_barang')  # Ganti dengan URL tujuan setelah simpan
    else:
        form = BarangForm()
    context['form'] = form
    return render(request, "staff_me/create_barang.html", context)

@login_required
@staff_me_required
def list_barang(request):
    query = request.GET.get("q", "")
    barang_list = Barang.objects.all()

    if query:
        barang_list = Barang.objects.filter(
        Q(nama__icontains=query) |
        Q(jenis_barang__nama__icontains=query)
    ).order_by('nama').distinct()


    paginator = Paginator(barang_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }

    return render(request, "staff_me/list_barang.html", context)

@login_required
@staff_me_required
def detail_barang(request, id):
    context={}
    context["data"] = Barang.objects.get(id=id)
    return render(request, "staff_me/detail_barang.html", context)


@login_required
@staff_me_required
def update_barang(request, id):
    barang = get_object_or_404(Barang, id=id)

    if request.method == 'POST':
        form = BarangForm(request.POST, request.FILES, instance=barang)
        if form.is_valid():
            form.save()
            return redirect('list_barang')
    else:
        form = BarangForm(instance=barang)

    context = {'form': form, 'barang': barang}
    return render(request, 'staff_me/update_barang.html', context)

@staff_me_required
@login_required
def delete_barang(request, id):
    # dictionary for initial data with 
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Barang, id = id)


    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to 
        # home page
        return redirect("list_barang")

    return render(request, "staff_me/delete_barang.html", context)
@login_required
@staff_me_required
def list_lokasi(request):
    query = request.GET.get("q", "")
    lokasi_list = Lokasi.objects.all()

    if query:
        lokasi_list = Lokasi.objects.filter(
        Q(lantai__icontains=query) |
        Q(ruangan__icontains=query)
    ).order_by('ruangan').distinct()


    paginator = Paginator(lokasi_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }

    return render(request, "staff_me/list_lokasi.html", context)

@login_required
@staff_me_required
def create_lokasi(request):
    context = {}
    if request.method == 'POST':
        form = LokasiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_lokasi')  # Ganti dengan URL tujuan setelah simpan
    else:
        form = LokasiForm()
    context['form'] = form
    return render(request, "staff_me/create_lokasi.html", context)
@login_required
@staff_me_required
def detail_lokasi(request, id):
    context={}
    context["data"] = Lokasi.objects.get(id=id)
    return render(request, "staff_me/detail_lokasi.html", context)


@staff_me_required
@login_required
def delete_lokasi(request, id):
    # dictionary for initial data with 
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Lokasi, id = id)


    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to 
        # home page
        return redirect("list_lokasi")

    return render(request, "staff_me/delete_lokasi.html", context)



@login_required
@staff_me_required
def update_lokasi(request, id):
    lokasi = get_object_or_404(Lokasi, id=id)

    if request.method == 'POST':
        form = LokasiForm(request.POST, instance=lokasi)
        if form.is_valid():
            form.save()
            return redirect('list_lokasi')
    else:
        form = LokasiForm(instance=lokasi)

    context = {'form': form, 'lokasi': lokasi}
    return render(request, 'staff_me/update_lokasi.html', context)



@login_required
@staff_me_required
def list_inventaris(request):
    query = request.GET.get("q", "")
    inventaris_list = Inventaris.objects.all()

    if query:
        inventaris_list = Inventaris.objects.filter(
        Q(barang__nama__icontains=query) |
        Q(lokasi__lantai__icontains=query)|
        Q(lokasi__ruangan__icontains=query)
    ).order_by('barang').distinct()


    paginator = Paginator(inventaris_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }
  
    return render(request, "staff_me/list_inventaris.html", context)

@login_required
@staff_me_required
def create_inventaris(request):
    context = {}
    if request.method == 'POST':
        form = InventarisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_inventaris')  # Ganti dengan URL tujuan setelah simpan
    else:
        form = InventarisForm()
    context['form'] = form
    return render(request, "staff_me/create_inventaris.html", context)
@login_required
@staff_me_required
def detail_inventaris(request, kode_inventaris):
    context={}
    context["data"] = Inventaris.objects.get(kode_inventaris=kode_inventaris)
    return render(request, "staff_me/detail_inventaris.html", context)


@staff_me_required
@login_required
def delete_inventaris(request, kode_inventaris):

    context = {}
    obj = get_object_or_404(Inventaris, kode_inventaris=kode_inventaris)


    if request.method =="POST":
        obj.delete()
        return redirect("list_inventaris")

    return render(request, "staff_me/delete_inventaris.html", context)



@login_required
@staff_me_required
def update_inventaris(request, kode_inventaris):
    inventaris = get_object_or_404(Inventaris, kode_inventaris=kode_inventaris)

    if request.method == 'POST':
        form = InventarisForm(request.POST, request.FILES, instance=inventaris)
        if form.is_valid():
            form.save()
            return redirect('list_inventaris')
    else:
        form = InventarisForm(instance=inventaris)

    context = {'form': form, 'inventaris': inventaris}
    return render(request, 'staff_me/update_inventaris.html', context)




@login_required
@staff_me_required
def list_peminjaman(request):
    query = request.GET.get("q", "")
    peminjaman_list = Peminjaman.objects.exclude(status='pengembalian_diajukan').exclude(status='returned')

    if query:
        peminjaman_list = Peminjaman.objects.filter(
        Q(user__username__icontains=query)|
        Q(tanggal_pinjam__icontains=query)
    ).order_by('user').distinct()


    paginator = Paginator(peminjaman_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }

    return render(request, "staff_me/list_peminjaman.html", context)

@login_required
@staff_me_required
def list_peminjaman_belum_disetujui(request):
    query = request.GET.get("q", "")
    peminjaman_list = Peminjaman.objects.filter(status="pending")

    if query:
        peminjaman_list = Peminjaman.objects.filter(
        Q(user__username__icontains=query)|
        Q(tanggal_pinjam__icontains=query)
    ).order_by('user').distinct()


    paginator = Paginator(peminjaman_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }

    return render(request, "staff_me/list_peminjaman_belum_disetujui.html", context)

@login_required
@staff_me_required
@transaction.atomic
def pilih_inventaris(request, peminjaman_id):
    peminjaman = get_object_or_404(Peminjaman, id=peminjaman_id)
    semua_detail = peminjaman.peminjamandetail_set.all()

    if request.method == 'POST':
        form = PilihSemuaInventarisForm(request.POST, peminjaman=peminjaman)
        if form.is_valid():
            for detail in semua_detail:
                field_name = f'inventaris_{detail.id}'
                selected_units = form.cleaned_data[field_name]

                if selected_units.count() != detail.jumlah:
                    messages.error(request, f"Jumlah unit untuk {detail.barang.nama} harus {detail.jumlah}")
                    return redirect('pilih_inventaris', peminjaman.id)

                if PeminjamanUnit.objects.filter(peminjaman_detail=detail).exists():
                    messages.warning(request, f"Inventaris untuk {detail.barang.nama} sudah pernah dipilih.")
                    return redirect('list_peminjaman_disetujui')

                for unit in selected_units:
                    PeminjamanUnit.objects.create(
                        peminjaman_detail=detail,
                        inventaris=unit,
                        kondisi_pinjam=unit.kondisi
                    )

            peminjaman.status = 'approved'
            peminjaman.save()
            messages.success(request, "Seluruh inventaris berhasil dipilih dan peminjaman disetujui.")
            return redirect('list_peminjaman_disetujui')
    else:
        form = PilihSemuaInventarisForm(peminjaman=peminjaman)

    return render(request, 'staff_me/pilih_inventaris.html', {
        'form': form,
        'peminjaman': peminjaman,
    })


@login_required
@staff_me_required
def create_pemindahan(request):
    PemindahanDetailInlineFormset = inlineformset_factory(Pemindahan, PemindahanDetail, form=PemindahanDetailForm, extra=1,validate_min=True,
    min_num=1, can_delete=False)
    if request.method == "POST":
        pemindahan_form = PemindahanForm(request.POST)
        pemindahan_detail_formset = PemindahanDetailInlineFormset(request.POST)
        if pemindahan_form.is_valid() and pemindahan_detail_formset.is_valid():
            pemindahan = pemindahan_form.save()
            pemindahan_details = pemindahan_detail_formset.save(commit=False)
            for pemindahan_detail in pemindahan_details:
                pemindahan_detail.pemindahan = pemindahan
                pemindahan_detail.lokasi_awal = pemindahan_detail.inventaris.lokasi
                pemindahan_detail.save()
            return redirect('list_pemindahan')
    else :
        pemindahan_form = PemindahanForm()
        pemindahan_detail_formset = PemindahanDetailInlineFormset()
    context = {
        "pemindahan_form": pemindahan_form,
        "pemindahan_detail_formset": pemindahan_detail_formset
    }
    return render(request, "staff_me/create_pemindahan.html",context)

@login_required
@staff_me_required
def list_peminjaman_disetujui(request):
    query = request.GET.get("q", "")
    peminjaman_list = Peminjaman.objects.filter(status="approved")

    if query:
        peminjaman_list = Peminjaman.objects.filter(
        Q(user__username__icontains=query)|
        Q(tanggal_pinjam__icontains=query)
    ).order_by('user').distinct()


    paginator = Paginator(peminjaman_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }

    return render(request, "staff_me/list_peminjaman_disetujui.html", context)

@login_required
@staff_me_required
def detail_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)
    data_detail = PeminjamanDetail.objects.filter(peminjaman=peminjaman)

    context = {
        "data": peminjaman,
        "data_detail": data_detail
    }
    return render(request, "staff_me/detail_peminjaman.html", context)

@login_required
@staff_me_required
def update_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)
    if request.method == 'POST':
        form = PeminjamanForm(request.POST, instance=peminjaman)
        if form.is_valid():
            form.save()
            return redirect('list_peminjaman')
    else:
        form = PeminjamanForm(instance=peminjaman)

    context = {'form': form, 'peminjaman': peminjaman}
    return render(request, 'staff_me/update_peminjaman.html', context)


@login_required
@staff_me_required
def list_jenis_barang(request):
    query = request.GET.get("q", "")
    jenis_barang_list = JenisBarang.objects.all()

    if query:
        jenis_barang_list = JenisBarang.objects.filter(
        Q(nama__icontains=query)
    ).order_by('nama').distinct()


    paginator = Paginator(jenis_barang_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }
    return render(request, "staff_me/list_jenis_barang.html", context)

@login_required
@staff_me_required
def create_jenis_barang(request):
    context = {}
    if request.method == 'POST':
        form = JenisBarangForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_jenis_barang')  # Ganti dengan URL tujuan setelah simpan
    else:
        form = JenisBarangForm()
    context['form'] = form
    return render(request, "staff_me/create_jenis_barang.html", context)
@login_required
@staff_me_required
def detail_jenis_barang(request, id):
    context={}
    context["data"] = JenisBarang.objects.get(id=id)
    return render(request, "staff_me/detail_jenis_barang.html", context)


@staff_me_required
@login_required
def delete_jenis_barang(request, id):
    # dictionary for initial data with 
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(JenisBarang, id=id)


    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to 
        # home page
        return redirect("list_jenis_barang")

    return render(request, "staff_me/delete_jenis_barang.html", context)



@login_required
@staff_me_required
def update_jenis_barang(request, id):
    jenis_barang = get_object_or_404(JenisBarang, id=id)

    if request.method == 'POST':
        form = JenisBarangForm(request.POST, request.FILES, instance=jenis_barang)
        if form.is_valid():
            form.save()
            return redirect('list_jenis_barang')
    else:
        form = JenisBarangForm(instance=jenis_barang)

    context = {'form': form, 'jenis_barang': jenis_barang}
    return render(request, 'staff_me/update_jenis_barang.html', context)



@login_required
@staff_me_required
def list_pemindahan(request):
    query = request.GET.get("q", "")
    pemindahan_list = Pemindahan.objects.all()

    if query:
        pemindahan_list = Pemindahan.objects.filter(
        Q(staff__username__icontains=query)|
        Q(tanggal_pemindahan__icontains=query)
    ).order_by('staff').distinct()


    paginator = Paginator(pemindahan_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }
    return render(request, "staff_me/list_pemindahan.html", context)

@login_required
@staff_me_required
def detail_pemindahan(request, id):
    pemindahan = get_object_or_404(Pemindahan, id=id)
    data_detail = PemindahanDetail.objects.filter(pemindahan=pemindahan)

    context = {
        "data": pemindahan,
        "data_detail": data_detail
    }
    return render(request, "staff_me/detail_pemindahan.html", context)
@login_required
@staff_me_required
def update_pemindahan(request, id):
    pemindahan = get_object_or_404(Pemindahan, id=id)
    PemindahanDetailFormSet = inlineformset_factory(
        Pemindahan,
        PemindahanDetail,
        form=PemindahanDetailForm,  
        formset=BasePemindahanDetailFormSet,
        extra=0,
        can_delete=False
    )
    if request.method == 'POST':
        form = PemindahanForm(request.POST, instance=pemindahan)
        formset = PemindahanDetailFormSet(request.POST, instance=pemindahan)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('list_pemindahan')
    else:
        form = PemindahanForm(instance=pemindahan)
        formset = PemindahanDetailFormSet(instance=pemindahan)

    context = {'form': form, 'pemindahan': pemindahan, 'formset': formset}
    return render(request, 'staff_me/update_pemindahan.html', context)

from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib import messages

@login_required
@staff_me_required
def list_pengembalian(request):
    query = request.GET.get("q", "")
    pengembalian_list = Peminjaman.objects.filter(Q(status='pengembalian_diajukan'))

    if query:
        pengembalian_list = Peminjaman.objects.filter(
        Q(staff__username__icontains=query)|
        Q(tanggal_pinjam__icontains=query)
    ).order_by('user').distinct()


    paginator = Paginator(pengembalian_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }
    # Ambil semua pengajuan pengembalian dari user (status = 'returned')
  
    return render(request, "staff_me/list_pengembalian.html", context)
@login_required
@staff_me_required
def verifikasi_pengembalian(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)

    if peminjaman.status != 'pengembalian_diajukan':
        messages.error(request, "Status peminjaman ini tidak valid untuk diverifikasi.")
        return redirect('list_pengembalian')  # Ganti sesuai URL staff

    # Update status dan kembalikan stok
    peminjaman.status = 'returned'
    peminjaman.tanggal_kembali = timezone.now().date()
    peminjaman.save()  # stok otomatis ditambah karena kamu sudah handle di `save()`
    messages.success(request, "Barang berhasil diverifikasi sebagai dikembalikan.")
    return redirect('list_pengembalian')

@login_required
@staff_me_required
def detail_pengembalian(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)
    data_detail = PeminjamanDetail.objects.filter(peminjaman=peminjaman)
    data_unit = PeminjamanUnit.objects.filter(peminjaman_detail__in=data_detail)
    context = {
        "data": peminjaman,
        "data_detail": data_detail,
        "data_unit": data_unit
    }
    return render(request, "staff_me/detail_pengembalian.html", context)


@login_required
@staff_me_required
def list_barang_dikembalikan(request):
    query = request.GET.get("q", "")
    pengembalian_list = Peminjaman.objects.filter(Q(status='returned'))
    
    if query:
        pengembalian_list = Peminjaman.objects.filter(
        Q(staff__username__icontains=query)|
        Q(tanggal_pinjam__icontains=query)
    ).order_by('user').distinct()


    paginator = Paginator(pengembalian_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }
    return render(request, "staff_me/list_barang_dikembalikan.html", context)
@login_required
@staff_me_required
def detail_barang_dikembalikan(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)
    data_detail = PeminjamanDetail.objects.filter(peminjaman=peminjaman)
    data_unit = PeminjamanUnit.objects.filter(peminjaman_detail__in=data_detail)
    context = {
        "data": peminjaman,
        "data_detail": data_detail,
        "data_unit": data_unit
    }
    return render(request, "staff_me/detail_barang_dikembalikan.html", context)


@login_required
@staff_me_required
def create_announcement(request):
    context = {}
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_announcement')  # Ganti dengan URL tujuan setelah simpan
    else:
        form = AnnouncementForm()
    context['form'] = form
    return render(request, "staff_me/create_announcement.html", context)

@login_required
@staff_me_required
def list_announcement(request):
    query = request.GET.get("q", "")
    announcement_list = Announcement.objects.order_by('-created_at')

    if query:
        announcement_list = Announcement.objects.filter(
        Q(title__icontains=query) |
        Q(message__icontains=query)
    ).order_by('created_at')


    paginator = Paginator(announcement_list, 5)  # tampilkan 5 barang per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "dataset": page_obj,
        "query": query,
        "page_obj": page_obj,
    }

    return render(request, "staff_me/list_announcement.html", context)

@login_required
@staff_me_required
def detail_announcement(request, id):
    context={}
    context["data"] = Announcement.objects.get(id=id)
    return render(request, "staff_me/detail_announcement.html", context)


@login_required
@staff_me_required
def update_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('list_announcement')
    else:
        form = AnnouncementForm(instance=announcement)

    context = {'form': form, 'announcement': announcement}
    return render(request, 'staff_me/update_announcement.html', context)

@staff_me_required
@login_required
def delete_announcement(request, id):
    # dictionary for initial data with 
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Announcement, id = id)


    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to 
        # home page
        return redirect("list_announcement")

    return render(request, "staff_me/delete_announcement.html", context)