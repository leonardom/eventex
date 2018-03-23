from django import forms


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome', required=True)
    cpf = forms.CharField(label='CPF', required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Telefone', required=True)