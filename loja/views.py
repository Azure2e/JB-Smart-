from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Carrinho
from .forms import CheckoutForm, RegistoForm
from .models import Categoria, Encomenda, ItemEncomenda, Produto


def lista(request):
    produtos = Produto.objects.filter(ativo=True).select_related("categoria")
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat")
    so_promo = request.GET.get("promo")
    if q:
        produtos = produtos.filter(Q(nome__icontains=q) | Q(categoria__nome__icontains=q))
    if cat:
        produtos = produtos.filter(categoria_id=cat)
    if so_promo:
        produtos = produtos.filter(promocao__gt=0)
    return render(request, "loja/lista.html", {
        "produtos": produtos, "categorias": Categoria.objects.all(),
        "q": q, "cat": cat, "so_promo": so_promo,
    })


@require_POST
def adicionar(request, pk):
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    if produto.stock < 1:
        messages.error(request, f"{produto.nome} está esgotado.")
    else:
        Carrinho(request).adicionar(produto)
        messages.success(request, f"{produto.nome} adicionado ao carrinho.")
    return redirect(request.META.get("HTTP_REFERER") or "lista")


def carrinho_view(request):
    c = Carrinho(request)
    return render(request, "loja/carrinho.html", {"itens": c.itens(), "total": c.total()})


@require_POST
def atualizar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    try:
        qtd = int(request.POST.get("quantidade", 1))
    except ValueError:
        qtd = 1
    Carrinho(request).definir(produto, qtd)
    return redirect("carrinho")


@require_POST
def remover(request, pk):
    Carrinho(request).remover(pk)
    return redirect("carrinho")


@login_required
def checkout(request):
    c = Carrinho(request)
    itens = c.itens()
    if not itens:
        messages.info(request, "O carrinho está vazio.")
        return redirect("lista")

    form = CheckoutForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                enc = form.save(commit=False)
                enc.cliente = request.user
                enc.total = c.total()
                enc.save()
                for i in itens:
                    p = Produto.objects.select_for_update().get(pk=i["produto"].pk)
                    if p.stock < i["quantidade"]:
                        raise ValueError(f"Stock insuficiente para {p.nome}.")
                    p.stock -= i["quantidade"]
                    p.save(update_fields=["stock"])
                    ItemEncomenda.objects.create(
                        encomenda=enc, produto=p,
                        quantidade=i["quantidade"], preco_unit=p.preco_final)
        except ValueError as erro:
            messages.error(request, str(erro))
            return redirect("carrinho")
        c.limpar()
        return redirect("encomenda_ok", pk=enc.pk)
    return render(request, "loja/checkout.html", {"form": form, "itens": itens, "total": c.total()})


@login_required
def encomenda_ok(request, pk):
    enc = get_object_or_404(Encomenda, pk=pk, cliente=request.user)
    return render(request, "loja/encomenda_ok.html", {
        "enc": enc,
        "pix_key": settings.PIX_KEY,
        "pix_name": settings.PIX_NAME,
    })


@login_required
def encomendas(request):
    lista_enc = request.user.encomendas.prefetch_related("itens__produto")
    return render(request, "loja/encomendas.html", {"encomendas": lista_enc})


def registo(request):
    form = RegistoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        messages.success(request, "Conta criada. Bem-vindo à JB Smart!")
        return redirect("lista")
    return render(request, "registration/registo.html", {"form": form})


def manifest(request):
    return render(request, "loja/manifest.json", content_type="application/manifest+json")


def service_worker(request):
    resp = render(request, "loja/sw.js", content_type="application/javascript")
    resp["Service-Worker-Allowed"] = "/"
    resp["Cache-Control"] = "no-cache"
    return resp


def offline(request):
    return render(request, "loja/offline.html")


def dias_d(request):
    """Página DIAS D – dias especiais com ofertas."""
    produtos = Produto.objects.filter(ativo=True, promocao__gt=0).select_related("categoria")
    return render(request, "loja/dias_d.html", {"produtos": produtos})
