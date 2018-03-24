from django.core import mail
from django.test import TestCase


class SubscribePostValidTest(TestCase):

    def setUp(self):
        data = dict(name='Leonardo Marcelino', cpf='12345678901',
                    email='leonardo.marcelino@gmail.com', phone='19-99258-6382')

        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]


    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscrition_email_to(self):
        expect = ['contato@eventex.com.br', 'leonardo.marcelino@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscrition_email_body(self):

        contents = [
            'Leonardo Marcelino',
            '12345678901',
            'leonardo.marcelino@gmail.com',
            '19-99258-6382'
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)