from .cart import Carrinho


def carrinho(request):
    return {"carrinho_qtd": len(Carrinho(request))}
