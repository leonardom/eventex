from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html must contain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fiels"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))



class SubscribePostTest(TestCase):
    """
    DADO que um visitante acessa /inscricao/
    QUANDO ele preenche o formulário
        e nome, cpf, email e telefone de confirmação
        e ele clica em enviar
    ENTÃO o sistema envia um e-mail de confirmação
        e o rementente é contato@eventex.com.br
        e o destinatário é o visitante
        e o remetente está em cópia carbono
        e o visitante é redirecionado para /inscricao/
        e o visitante vê uma mensagem de sucesso.
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

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscrition_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'leonardo.marcelino@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscrition_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Leonardo Marcelino', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('leonardo.marcelino@gmail.com', email.body)
        self.assertIn('19-99258-6382', email.body)


class SubscribeInvalidPostTest(TestCase):
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


class SubscribeSuccessMessage(TestCase):
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