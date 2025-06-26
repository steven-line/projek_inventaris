from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
   
    path('barang/', views.list_barang, name='list_barang'),
    path('barang/tambah/', views.create_barang, name='create_barang'),
    path('barang/<int:id>/', views.detail_barang, name='detail_barang'),
    path('barang/<int:id>/edit/', views.update_barang, name='update_barang'),
    path('barang/<int:id>/hapus/', views.delete_barang, name='delete_barang'),
    path('lokasi/', views.list_lokasi, name='list_lokasi'),
    path('lokasi/tambah/', views.create_lokasi, name='create_lokasi'),
    path('lokasi/<int:id>/', views.detail_lokasi, name='detail_lokasi'),
    path('lokasi/<int:id>/edit/', views.update_lokasi, name='update_lokasi'),
    path('lokasi/<int:id>/hapus/', views.delete_lokasi, name='delete_lokasi'),
    path('inventaris/', views.list_inventaris, name='list_inventaris'),
    path('inventaris/tambah/', views.create_inventaris, name='create_inventaris'),
    path('inventaris/<str:kode_inventaris>/', views.detail_inventaris, name='detail_inventaris'),
    path('inventaris/<str:kode_inventaris>/edit/', views.update_inventaris, name='update_inventaris'),
    path('inventaris/<str:kode_inventaris>/hapus/', views.delete_inventaris, name='delete_inventaris'),
    path('jenis-barang/', views.list_jenis_barang, name='list_jenis_barang'),
    path('jenis-barang/tambah/', views.create_jenis_barang, name='create_jenis_barang'),
    path('jenis-barang/<int:id>/', views.detail_jenis_barang, name='detail_jenis_barang'),
    path('jenis-barang/<int:id>/edit/', views.update_jenis_barang, name='update_jenis_barang'),
    path('jenis-barang/<int:id>/hapus/', views.delete_jenis_barang, name='delete_jenis_barang'),

    path('peminjaman/', views.list_peminjaman, name='list_peminjaman'),
    path('peminjaman/belum_disetujui', views.list_peminjaman_belum_disetujui, name='list_peminjaman_belum_disetujui'),
    path('peminjaman/disetujui', views.list_peminjaman_disetujui, name='list_peminjaman_disetujui'),
    path('peminjaman/unit/pilih/<int:peminjaman_id>/', views.pilih_inventaris, name='pilih_inventaris'),
    path('peminjaman/<int:id>/', views.detail_peminjaman, name='detail_peminjaman'),
    path('peminjaman/<int:id>/edit/', views.update_peminjaman, name='update_peminjaman'),
       # Halaman daftar pengembalian untuk staff ME
    path('pengembalian/', views.list_pengembalian, name='list_pengembalian'),
    path('pengembalian/<int:id>/', views.detail_pengembalian, name='detail_pengembalian'),
    # Aksi verifikasi pengembalian (approve/reject)
    path('pengembalian/<int:id>/verifikasi/', views.verifikasi_pengembalian, name='verifikasi-pengembalian'),
    path('barang-dikembalikan/', views.list_barang_dikembalikan, name='list_barang_dikembalikan'),
    path('barang-dikembalikan/<int:id>/', views.detail_barang_dikembalikan, name='detail_barang_dikembalikan'),
    path('pemindahan/', views.list_pemindahan, name='list_pemindahan'),
    path('pemindahan/tambah/', views.create_pemindahan, name='create_pemindahan'),
    path('pemindahan/<int:id>/', views.detail_pemindahan, name='detail_pemindahan'),
    path('pemindahan/<int:id>/edit/', views.update_pemindahan, name='update_pemindahan'),
    
    path('pengumuman/', views.list_announcement, name='list_announcement'),
    path('pengumuman/tambah/', views.create_announcement, name='create_announcement'),
    path('pengumuman/<int:id>/', views.detail_announcement, name='detail_announcement'),
    path('pengumuman/<int:id>/edit/', views.update_announcement, name='update_announcement'),
    path('pengumuman/<int:id>/hapus/', views.delete_announcement, name='delete_announcement'),
]
