from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.timezone import now
from django.db import transaction
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import User

    
class JenisBarang(models.Model):  
    
    nama = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Jenis Barang'
        verbose_name_plural = 'Jenis Barang'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
class Lokasi(models.Model):
 
    
    lantai = models.IntegerField()
    ruangan = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lokasi'
        verbose_name_plural = 'Lokasi'
        unique_together = ('lantai', 'ruangan')
        ordering = ['lantai', 'ruangan']
    
    def __str__(self):
        return f"Lantai {self.lantai} - {self.ruangan}"

class Barang(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    jenis_barang = models.ForeignKey(JenisBarang, on_delete=models.PROTECT)
    deskripsi = models.TextField(blank=True)
    gambar = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Barang'
        verbose_name_plural = 'Barang'
        ordering = ['nama', 'jenis_barang']
    
    def __str__(self):
        return self.nama
    def get_absolute_url(self):
      return reverse('item-detail', args=[str(self.id)])

class Inventaris(models.Model):
    kode_inventaris = models.CharField(max_length=20, unique=True, primary_key=True, editable=False)
    KONDISI_CHOICES = (
        ('baik', 'Baik'),
        ('rusak', 'Rusak'),
        ('hilang', 'Hilang'),
    )
    
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    lokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE)
    kondisi = models.CharField(max_length=10, choices=KONDISI_CHOICES, default='baik')
    catatan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inventaris'
        verbose_name_plural = 'Inventaris'

        ordering = ['barang__nama', 'lokasi__lantai', 'lokasi__ruangan']
    
    def generate_code(self):
        kode_barang = slugify(self.barang.nama)[:2].upper()
        kode_lantai = f"{self.lokasi.lantai:02d}"
        kode_ruangan = ''.join(filter(str.isalnum, self.lokasi.ruangan.upper()))[:2]
        kode_unik = uuid.uuid4().hex[:4].upper()
        return f"INV-L{kode_lantai}-{kode_ruangan}-{kode_barang}-{kode_unik}"

    def save(self, *args, **kwargs):
        if not self.kode_inventaris:
            self.kode_inventaris = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
            return f"{self.kode_inventaris} - {self.barang.nama}"

class Peminjaman(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('pengembalian_diajukan', 'Pengembalian Diajukan'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
        ('peminjaman_dibatalkan', 'Peminjaman Dibatalkan')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='peminjaman_user')
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    catatan_staff = models.TextField(blank=True)
    keterangan = models.TextField(blank=False)
    tanggal_pinjam = models.DateField(default=now)
    tanggal_kembali = models.DateField(blank=True, null=True)
    tanggal_dikembalikan = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Peminjaman'
        verbose_name_plural = 'Peminjaman'
        ordering = ['-created_at', '-tanggal_pinjam']
        
  
    def get_absolute_url(self):
      return reverse('pinjam-detail', args=[str(self.id)])
  
    def __str__(self):
        return f"Peminjaman #{self.id} oleh {self.user.first_name} {self.user.last_name}"
    

class PeminjamanDetail(models.Model):
    peminjaman = models.ForeignKey(Peminjaman, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()

    

    class Meta:
        verbose_name = 'Detail Peminjaman'
        verbose_name_plural = 'Detail Peminjaman'
        ordering = ['peminjaman', 'barang__nama']
    
    def __str__(self):
        return f"Detail peminjaman #{self.peminjaman.id}"
   

class PeminjamanUnit(models.Model):
    peminjaman_detail = models.ForeignKey(PeminjamanDetail, on_delete=models.CASCADE)
    inventaris = models.ForeignKey(Inventaris, to_field="kode_inventaris", on_delete=models.CASCADE)
    kondisi_pinjam = models.CharField(max_length=100)
    kondisi_kembali = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['inventaris__barang__nama']
    def __str__(self):
        return f"Peminjaman per unit {self.peminjaman_detail}"
class Pemindahan(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    keterangan = models.TextField(blank=True)
    tanggal_pemindahan = models.DateField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pemindahan'
        verbose_name_plural = 'Pemindahan'
        ordering = ['-created_at', '-tanggal_pemindahan']
    
    def __str__(self):
        return f"Pemindahan #{self.id} oleh {self.staff.first_name} {self.staff.last_name}"
    

class PemindahanDetail(models.Model):
    pemindahan = models.ForeignKey(Pemindahan, on_delete=models.CASCADE)
    inventaris = models.ForeignKey(Inventaris,to_field='kode_inventaris', on_delete=models.CASCADE, blank=False)
    lokasi_awal = models.ForeignKey(Lokasi, on_delete=models.CASCADE, related_name='pemindahan_awal')
    lokasi_tujuan = models.ForeignKey(Lokasi, on_delete=models.CASCADE, related_name='pemindahan_tujuan', blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Detail Pemindahan'
        verbose_name_plural = 'Detail Pemindahan'
        ordering = ['pemindahan', 'inventaris__barang__nama']
    
    def __str__(self):
        return f"Detail pemindahan #{self.pemindahan.id}"
  

class Announcement(models.Model):
    title = models.CharField(blank=False, max_length=50)
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
