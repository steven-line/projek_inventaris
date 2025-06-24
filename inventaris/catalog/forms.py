from django import forms

from django.utils import timezone
from django.forms import BaseInlineFormSet
from catalog.models import *
class PeminjamanForm(forms.ModelForm):
     
    class Meta:
        
        model = Peminjaman
        fields = ['tanggal_pinjam', 'tanggal_dikembalikan', 'keterangan']
        widgets = {
            'tanggal_pinjam': forms.DateInput(attrs={"type":"date"}),
            'tanggal_dikembalikan': forms.DateInput(attrs={"type":"date"}),
            'keterangan': forms.Textarea()
        }
    def clean(self):
        cleaned_data = super().clean()
        tanggal_pinjam = cleaned_data.get("tanggal_pinjam")
        tanggal_dikembalikan = cleaned_data.get("tanggal_dikembalikan")
        if tanggal_pinjam < timezone.now().date():
            raise ValidationError("tanggal pinjam tidak boleh sebelum hari ini")
        if tanggal_pinjam > tanggal_dikembalikan:
            raise ValidationError("tanggal dikembalikan harus lebih besar dari tanggal peminjaman")
        if tanggal_dikembalikan < timezone.now().date():
              raise ValidationError("tanggal dikembalikan tidak boleh sebelum hari ini")
        return cleaned_data
    

class PeminjamanDetailInlineForm(forms.ModelForm):
    class Meta:
        model = PeminjamanDetail
        fields = ['barang', 'jumlah']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  # Ambil hanya barang yang memiliki inventaris TERSEDIA
        print("== DEBUG: Barang yang masuk ke select ==")
        tersedia_ids = []
        for barang in Barang.objects.all():
            tersedia = get_inventaris_tersedia(barang)
            print(f"Barang: {barang.nama} | Total inventaris baik: {Inventaris.objects.filter(barang=barang, kondisi='baik').count()} | Inventaris tersedia: {tersedia.count()}")
            if tersedia.exists():
                tersedia_ids.append(barang.id)

        print(f"tersedia_ids = {tersedia_ids}")
        self.fields['barang'].queryset = Barang.objects.filter(id__in=tersedia_ids)

   
from django.db.models import Q
def get_inventaris_tersedia(barang):
    semua_inventaris = Inventaris.objects.filter(barang=barang, kondisi='baik')

    dipinjam_ids = PeminjamanUnit.objects.filter(
        inventaris__barang=barang,
        peminjaman_detail__peminjaman__status__in=['pending', 'approved', 'pengembalian_diajukan']
    ).values_list('inventaris', flat=True)

    return semua_inventaris.exclude(kode_inventaris__in=dipinjam_ids)

    
class PeminjamanDetailFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        barang_terpilih = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                barang = form.cleaned_data.get("barang")
                jumlah = form.cleaned_data.get("jumlah")
                
                if not barang:
                    raise ValidationError("Setiap baris harus memiliki barang yang dipilih.")
                if barang in barang_terpilih:
                    raise ValidationError(f"Barang '{barang}' dipilih lebih dari sekali.")
                barang_terpilih.append(barang)
                inventaris_tersedia = get_inventaris_tersedia(barang)
                jumlah_tersedia = inventaris_tersedia.count()
                if jumlah > jumlah_tersedia:
                 raise ValidationError(f"Jumlah barang '{barang}' melebihi unit tersedia ({jumlah_tersedia} unit tersedia).")