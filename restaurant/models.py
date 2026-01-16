from django.db import models

class Mesa(models.Model):
    STATUS_CHOICES = [
        ('LIVRE', 'Livre'),
        ('OCUPADA', 'Ocupada'),
    ]
    numero = models.IntegerField(unique=True, verbose_name="Número da Mesa")
    capacidade = models.IntegerField(verbose_name="Capacidade (Pessoas)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='LIVRE', verbose_name="Status")

    def __str__(self):
        return f"Mesa {self.numero} - {self.get_status_display()}"

class Prato(models.Model):
    CATEGORIA_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('PRINCIPAL', 'Prato Principal'),
        ('BEBIDA', 'Bebida'),
        ('SOBREMESA', 'Sobremesa'),
    ]
    nome = models.CharField(max_length=100, verbose_name="Nome do Prato")
    descricao = models.TextField(verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço (R$)")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoria")
    imagem = models.ImageField(upload_to='pratos/', blank=True, null=True, verbose_name="Foto do Prato")

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('NOVO', 'Novo'),
        ('PREPARO', 'Em Preparo'),
        ('FINALIZADO', 'Finalizado'),
    ]
    mesa = models.IntegerField(verbose_name="Número da Mesa")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOVO', verbose_name="Status")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total do Pedido")

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Prato, on_delete=models.CASCADE)
    quantidade = models.IntegerField(verbose_name="Quantidade")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")

    @property
    def total_item(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
