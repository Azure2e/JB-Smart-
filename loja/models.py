from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=80)
    imagem = models.ImageField(upload_to="categorias/", blank=True, null=True)
    emoji = models.CharField(max_length=4, default="🛒", blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="produtos")
    nome = models.CharField(max_length=120)
    preco = models.DecimalField("Preço (R$)", max_digits=8, decimal_places=2)
    promocao = models.PositiveSmallIntegerField("Desconto (%)", default=0)
    stock = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to="produtos/", blank=True, storage=None)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def preco_final(self):
        desconto = Decimal(100 - min(self.promocao, 100)) / Decimal(100)
        return (self.preco * desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Encomenda(models.Model):
    ENTREGA, RECOLHA = "entrega", "recolha"
    MODOS = [(ENTREGA, "Entrega ao domicílio"), (RECOLHA, "Recolha na loja")]
    ESTADOS = [("pendente", "Pendente"), ("preparar", "Em preparação"),
               ("pronta", "Pronta"), ("concluida", "Concluída"), ("cancelada", "Cancelada")]
    PAGAMENTOS = [
        ("pix", "PIX"),
        ("dinheiro", "Dinheiro na entrega/recolha"),
        ("mbway", "MB WAY"),
        ("multibanco", "Multibanco"),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="encomendas")
    criada = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendente")
    modo = models.CharField("Modo", max_length=10, choices=MODOS, default=ENTREGA)
    metodo_pagamento = models.CharField("Método de pagamento", max_length=20, choices=PAGAMENTOS, default="pix")

    # Dados do cliente (checkout seguro)
    nome_completo = models.CharField("Nome completo", max_length=150)
    email = models.EmailField("Email")
    telefone = models.CharField(max_length=20)
    morada = models.CharField("Morada completa", max_length=255, blank=True)
    codigo_postal = models.CharField("Código postal", max_length=10, blank=True)
    cidade = models.CharField(max_length=80, blank=True)
    notas = models.TextField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["-criada"]

    def __str__(self):
        return f"Encomenda #{self.pk} - {self.nome_completo}"


class ItemEncomenda(models.Model):
    encomenda = models.ForeignKey(Encomenda, related_name="itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unit = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.preco_unit * self.quantidade



