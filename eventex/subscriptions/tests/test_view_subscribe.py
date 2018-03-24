from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGetTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get /incricao must return status code 2000"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


    def test_csrf(self):
        """Html must contain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValidTest(TestCase):
    """
    DADO que um visitante acessa /inscricao/
    QUANDO ele preenche o formulário
        e nome, cpf, email e telefone de confirmação
        e ele clica em enviar
    ENTÃO o sistema envia um e-mail de confirmação
        e o visitante é redirecionado para /inscricao/
    """

    def setUp(self):
        data = dict(name='Leonardo Marcelino', cpf='12345678901',
                    email='leonardo.marcelino@gmail.com', phone='19-99258-6382')

        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class SubscribePostInvalidTest(TestCase):
    """
    DADO que um visitante acessa /inscricao/
    QUANDO ele NÃO preenche o formulário
        e nome, cpf, email e telefone de confirmação
        e ele clica em enviar
    ENTÃO o sistema deve exibir erros.
    """

    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_format(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessageTest(TestCase):
    """
    DADO que um visitante acessa /inscricao/
    QUANDO ele preenche o formulário
        e nome, cpf, email e telefone de confirmação
        e ele clica em enviar
    ENTÃO o visitante vê uma mensagem de sucesso.
    """

    def test_message(self):
        data = dict(name='Leonardo Marcelino', cpf='12345678901',
                    email='leonardo.marcelino@gmail.com', phone='19-99258-6382')

        resp = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(resp, 'Inscrição realizada com sucesso!')