from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(JenisBarang)
admin.site.register(Barang)
admin.site.register(Inventaris)
admin.site.register(Pemindahan)
admin.site.register(PemindahanDetail)
admin.site.register(Peminjaman)
admin.site.register(PeminjamanDetail)
admin.site.register(PeminjamanUnit)
admin.site.register(Lokasi)
admin.site.register(Announcement)