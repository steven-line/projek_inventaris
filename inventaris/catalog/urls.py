from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('barang/', views.BarangListView.as_view(), name='barang'),
    path('barang/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('pinjam-barang/', views.RentalListView.as_view(), name='pinjam-barang'),
    path('barang-rusak/', views.barang_rusak_list, name='barang-rusak'),
    path("peminjaman/<int:pk>/batalkan-peminjaman/", views.batalkan_peminjaman, name="batalkan-peminjaman"),

    path('pinjam-detail/<int:pk>', views.RentalDetailView.as_view(), name='pinjam-detail'),
    path("create-pinjam/", views.create_peminjaman, name="create-peminjaman"),
    path("peminjaman/<int:pk>/ajukan-pengembalian/", views.ajukan_pengembalian, name="ajukan-pengembalian"),

]
 
