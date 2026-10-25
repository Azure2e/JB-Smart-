from decimal import Decimal

from .models import Produto


class Carrinho:
    """Carrinho guardado na sessão: {produto_id: quantidade}."""

    def __init__(self, request):
        self.session = request.session
        self.dados = self.session.setdefault("carrinho", {})

    def _guardar(self):
        self.session.modified = True

    def adicionar(self, produto, qtd=1):
        k = str(produto.pk)
        nova = min(self.dados.get(k, 0) + qtd, produto.stock)
        if nova > 0:
            self.dados[k] = nova
        self._guardar()

    def definir(self, produto, qtd):
        k = str(produto.pk)
        qtd = min(qtd, produto.stock)
        if qtd <= 0:
            self.dados.pop(k, None)
        else:
            self.dados[k] = qtd
        self._guardar()

    def remover(self, produto_id):
        self.dados.pop(str(produto_id), None)
        self._guardar()

    def limpar(self):
        self.session["carrinho"] = {}
        self._guardar()

    def itens(self):
        produtos = Produto.objects.filter(pk__in=self.dados.keys(), ativo=True)
        return [
            {"produto": p, "quantidade": self.dados[str(p.pk)],
             "subtotal": p.preco_final * self.dados[str(p.pk)]}
            for p in produtos
        ]

    def total(self):
        return sum((i["subtotal"] for i in self.itens()), Decimal("0.00"))

    def __len__(self):
        return sum(self.dados.values())
