from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        return handle_post(request)
    else:
        return handle_get(request)


def handle_post(request):
    form = SubscriptionForm(request.POST)

    if form.is_valid():  # o método is_valid() já chama o full_clean()
        # form.full_clean()  # transforma string da requisição para objetos Python

        body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)

        mail.send_mail('Confirmação de inscrição',
                       body,
                       'contato@eventex.com.br',
                       ['contato@eventex.com.br', form.cleaned_data['email']])

        messages.success(request, 'Inscrição realizada com sucesso!')

        return HttpResponseRedirect('/inscricao/')

    else:
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})


def handle_get(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)
