from catalog.models import *
from django import forms
from django.utils import timezone
from django.forms import BaseInlineFormSet
from django.contrib.auth.models import User, Group
class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = [
            "nama", "jenis_barang", "deskripsi", "gambar"
        ]

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            "title", "message"
        ]

class LokasiForm(forms.ModelForm):
    class Meta:
        model = Lokasi
        fields = ["lantai", "ruangan"]

class InventarisForm(forms.ModelForm):
    class Meta:
        model = Inventaris
        fields = ['barang', 'lokasi', 'kondisi', 'catatan']


class JenisBarangForm(forms.ModelForm):
    class Meta:
        model = JenisBarang
        fields = ['nama']

class PemindahanForm(forms.ModelForm):
    class Meta:
        model = Pemindahan
        fields = ['staff', 'tanggal_pemindahan', 'keterangan']
        widgets = {
           'tanggal_pemindahan': forms.DateInput(attrs={"type":"date"}),
           'keterangan': forms.Textarea()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            staff_group = Group.objects.get(name='staff_me')
            self.fields['staff'].queryset = User.objects.filter(groups=staff_group)
        except Group.DoesNotExist:
            self.fields['staff'].queryset = User.objects.none()  # kalau grup ga ada, kosongkan queryset


    def clean(self):
        cleaned_data = super().clean()
        tanggal_pemindahan = cleaned_data.get("tanggal_pemindahan")
        if tanggal_pemindahan < timezone.now().date():
            raise ValidationError("tanggal pemindahan tidak boleh sebelum hari ini")
        return cleaned_data


class PemindahanDetailForm(forms.ModelForm):
   
    class Meta:
        model = PemindahanDetail
        fields = ['inventaris', 'lokasi_tujuan']
 
    

    def clean(self):
        cleaned_data = super().clean()
        inventaris = cleaned_data.get('inventaris')
        lokasi_tujuan = cleaned_data.get('lokasi_tujuan')

        if inventaris and lokasi_tujuan:
            lokasi_awal = inventaris.lokasi  
            if lokasi_awal == lokasi_tujuan:
                raise ValidationError("Lokasi tujuan tidak boleh sama dengan lokasi awal.")


class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        widgets = {
           'tanggal_kembali': forms.DateInput(attrs={"type":"date"})
        }
        exclude = ['user', 'keterangan', 'tanggal_pinjam', 'tanggal_dikembalikan']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            staff_group = Group.objects.get(name='staff_me')
            self.fields['staff'].queryset = User.objects.filter(groups=staff_group)
        except Group.DoesNotExist:
            self.fields['staff'].queryset = User.objects.none()  # kalau grup ga ada, kosongkan queryset
