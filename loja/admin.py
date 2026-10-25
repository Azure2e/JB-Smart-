from django.contrib import admin

from .models import Categoria, Encomenda, ItemEncomenda, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "emoji")


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "promocao", "stock", "ativo")
    list_filter = ("categoria", "ativo")
    list_editable = ("preco", "promocao", "stock", "ativo")
    search_fields = ("nome",)


class ItemInline(admin.TabularInline):
    model = ItemEncomenda
    extra = 0
    readonly_fields = ("produto", "quantidade", "preco_unit")


@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome_completo", "email", "telefone", "cidade", "modo", "metodo_pagamento", "total", "estado", "criada")
    list_filter = ("estado", "modo", "metodo_pagamento")
    list_editable = ("estado",)
    search_fields = ("nome_completo", "email", "telefone", "morada", "cidade")
    readonly_fields = ("criada", "total")
    inlines = [ItemInline]
    fieldsets = (
        ("Cliente", {"fields": ("cliente", "nome_completo", "email", "telefone")}),
        ("Endereço", {"fields": ("modo", "morada", "codigo_postal", "cidade")}),
        ("Pagamento e Estado", {"fields": ("metodo_pagamento", "estado", "total", "criada")}),
        ("Notas", {"fields": ("notas",), "classes": ("collapse",)}),
    )
