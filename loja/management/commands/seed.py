from django.core.management.base import BaseCommand

from loja.models import Categoria, Produto

DADOS = {
    ("Frutas e Legumes", "🍎"): [("Maçã Gala 1kg", "1.99", 30, 80), ("Banana 1kg", "1.49", 0, 60),
                                 ("Tomate 1kg", "2.29", 15, 40), ("Batata 2kg", "1.89", 0, 70)],
    ("Talho e Peixaria", "🥩"): [("Peito de frango 1kg", "5.49", 10, 30), ("Bife de vaca 500g", "8.99", 0, 20),
                                  ("Salmão fresco 400g", "7.99", 20, 15)],
    ("Laticínios", "🥛"): [("Leite meio-gordo 1L", "0.79", 0, 200), ("Iogurte natural 4un", "1.39", 0, 90),
                           ("Queijo flamengo 200g", "2.49", 25, 50)],
    ("Padaria", "🍞"): [("Pão de forma", "1.29", 0, 40), ("Pão alentejano", "1.49", 0, 25)],
    ("Mercearia", "🍝"): [("Esparguete 500g", "0.89", 0, 120), ("Arroz carolino 1kg", "1.35", 10, 100),
                          ("Azeite virgem extra 750ml", "6.99", 15, 35)],
    ("Bebidas", "🥤"): [("Água 1,5L", "0.45", 0, 300), ("Sumo de laranja 1L", "1.79", 0, 60),
                        ("Cerveja 6x33cl", "3.99", 20, 45)],
}


class Command(BaseCommand):
    help = "Cria categorias e produtos de exemplo."

    def handle(self, *args, **opts):
        for (nome, emoji), produtos in DADOS.items():
            cat, _ = Categoria.objects.get_or_create(nome=nome, defaults={"emoji": emoji})
            for n, preco, promo, stock in produtos:
                Produto.objects.get_or_create(
                    nome=n, defaults={"categoria": cat, "preco": preco, "promocao": promo, "stock": stock})
        self.stdout.write(self.style.SUCCESS("Dados de exemplo criados."))
