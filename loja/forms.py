from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Encomenda


class RegistoForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = (
            "nome_completo", "email", "telefone",
            "modo", "morada", "codigo_postal", "cidade",
            "metodo_pagamento", "notas",
        )
        widgets = {
            "notas": forms.Textarea(attrs={"rows": 2}),
            "modo": forms.RadioSelect,
            "metodo_pagamento": forms.RadioSelect,
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["email"].initial = user.email
            self.fields["nome_completo"].initial = user.get_full_name() or user.username

    def clean(self):
        dados = super().clean()
        if dados.get("modo") == Encomenda.ENTREGA:
            if not dados.get("morada"):
                self.add_error("morada", "Indique a morada completa para entrega.")
            if not dados.get("codigo_postal"):
                self.add_error("codigo_postal", "Indique o código postal.")
            if not dados.get("cidade"):
                self.add_error("cidade", "Indique a cidade.")
        return dados
