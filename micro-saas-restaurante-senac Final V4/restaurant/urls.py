from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView, DashboardView,
    MesaListView, MesaCreateView, MesaUpdateView, MesaDeleteView,
    PratoListView, PratoCreateView, PratoUpdateView, PratoDeleteView,
    CardapioPublicoView, InicioView,
    create_order, get_orders, update_order_status, delete_order
)

urlpatterns = [
    path('inicio/', InicioView.as_view(), name='inicio'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Mesas
    path('mesas/', MesaListView.as_view(), name='mesa_list'),
    path('mesas/nova/', MesaCreateView.as_view(), name='mesa_create'),
    path('mesas/<int:pk>/editar/', MesaUpdateView.as_view(), name='mesa_update'),
    path('mesas/<int:pk>/excluir/', MesaDeleteView.as_view(), name='mesa_delete'),

    # Pratos
    path('pratos/', PratoListView.as_view(), name='prato_list'),
    path('pratos/novo/', PratoCreateView.as_view(), name='prato_create'),
    path('pratos/<int:pk>/editar/', PratoUpdateView.as_view(), name='prato_update'),
    path('pratos/<int:pk>/excluir/', PratoDeleteView.as_view(), name='prato_delete'),

    # Cardápio Público
    path('cardapio/', CardapioPublicoView.as_view(), name='cardapio_publico'),
    
    # API
    path('api/pedido/novo/', create_order, name='create_order'),
    path('api/pedidos/', get_orders, name='get_orders'),
    path('api/pedido/<int:pk>/update_status/', update_order_status, name='update_order_status'),
    path('api/pedido/<int:pk>/delete/', delete_order, name='delete_order'),
]
