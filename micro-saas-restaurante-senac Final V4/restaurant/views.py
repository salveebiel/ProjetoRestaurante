from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Mesa, Prato, Pedido, ItemPedido
from .forms import MesaForm, PratoForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class InicioView(TemplateView):
    template_name = 'restaurant/inicio.html'

class CustomLoginView(LoginView):
    template_name = 'restaurant/login.html'
    redirect_authenticated_user = True

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'restaurant/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mesas'] = Mesa.objects.count()
        context['mesas_livres'] = Mesa.objects.filter(status='LIVRE').count()
        context['mesas_ocupadas'] = Mesa.objects.filter(status='OCUPADA').count()
        context['total_pratos'] = Prato.objects.count()
        return context

# Mesa CRUD
class MesaListView(LoginRequiredMixin, ListView):
    model = Mesa
    template_name = 'restaurant/mesa_list.html'
    context_object_name = 'mesas'

class MesaCreateView(LoginRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'restaurant/mesa_form.html'
    success_url = reverse_lazy('mesa_list')

class MesaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'restaurant/mesa_form.html'
    success_url = reverse_lazy('mesa_list')

class MesaDeleteView(LoginRequiredMixin, DeleteView):
    model = Mesa
    template_name = 'restaurant/mesa_confirm_delete.html'
    success_url = reverse_lazy('mesa_list')

# Prato CRUD
class PratoListView(LoginRequiredMixin, ListView):
    model = Prato
    template_name = 'restaurant/prato_list.html'
    context_object_name = 'pratos'

class PratoCreateView(LoginRequiredMixin, CreateView):
    model = Prato
    form_class = PratoForm
    template_name = 'restaurant/prato_form.html'
    success_url = reverse_lazy('prato_list')

class PratoUpdateView(LoginRequiredMixin, UpdateView):
    model = Prato
    form_class = PratoForm
    template_name = 'restaurant/prato_form.html'
    success_url = reverse_lazy('prato_list')

class PratoDeleteView(LoginRequiredMixin, DeleteView):
    model = Prato
    template_name = 'restaurant/prato_confirm_delete.html'
    success_url = reverse_lazy('prato_list')

# Cardápio Público
class CardapioPublicoView(ListView):
    model = Prato
    template_name = 'restaurant/cardapio_publico.html'
    context_object_name = 'pratos'
    ordering = ['categoria', 'nome']

# API Endpoints
@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)
        mesa = data.get('mesa')
        itens = data.get('itens', [])

        if not mesa or not itens:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)

        pedido = Pedido.objects.create(mesa=mesa)
        
        total_pedido = 0
        for item in itens:
            try:
                produto = Prato.objects.get(id=item['id'])
                qty = int(item['qty'])
                preco = produto.preco
                
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=qty,
                    preco_unitario=preco
                )
                total_pedido += (preco * qty)
            except Prato.DoesNotExist:
                continue
        
        pedido.total = total_pedido
        pedido.save()
        
        return JsonResponse({'message': 'Pedido criado com sucesso!', 'order_id': pedido.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_orders(request):
    # Only allow admin to see orders? Assuming admin session for dashboard.
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    pedidos = Pedido.objects.all().order_by('-data_criacao').prefetch_related('itens__produto')
    data = []
    for p in pedidos:
        itens = []
        for i in p.itens.all():
            itens.append({
                'produto_id': i.produto.id,
                'nome': i.produto.nome,
                'quantidade': i.quantidade,
                'preco': str(i.preco_unitario),
                'total_item': str(i.total_item)
            })
        data.append({
            'id': p.id,
            'mesa': p.mesa,
            'data': p.data_criacao.strftime('%d/%m/%Y %H:%M'),
            'total': str(p.total),
            'status': p.get_status_display(),
            'status_code': p.status,
            'itens': itens
        })
    return JsonResponse(data, safe=False)

@require_POST
def update_order_status(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status not in ['NOVO', 'PREPARO', 'FINALIZADO']:
            return JsonResponse({'error': 'Status inválido'}, status=400)

        pedido = Pedido.objects.get(pk=pk)
        pedido.status = new_status
        pedido.save()

        return JsonResponse({'message': 'Status atualizado com sucesso!'})
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def delete_order(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        pedido = Pedido.objects.get(pk=pk)
        pedido.delete()
        return JsonResponse({'message': 'Pedido excluído com sucesso!'})
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido não encontrado'}, status=404)
