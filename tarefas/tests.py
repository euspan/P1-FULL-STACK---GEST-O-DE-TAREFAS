from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import Equipe, Perfil
from tarefas.models import Dependencia, Membro, Projeto, Subtarefa


class FuncionalidadesTest(TestCase):
    def setUp(self):
        self.equipe_a = Equipe.objects.create(nome='Equipe A')
        self.equipe_b = Equipe.objects.create(nome='Equipe B')
        self.equipe_c = Equipe.objects.create(nome='Equipe C')
        self.admin_a = User.objects.create_user('admin_a', password='senha12345')
        self.operador_a = User.objects.create_user('operador_a', password='senha12345')
        self.admin_b = User.objects.create_user('admin_b', password='senha12345')
        self.admin_c = User.objects.create_user('admin_c', password='senha12345')
        Perfil.objects.create(usuario=self.admin_a, equipe=self.equipe_a, papel='admin')
        Perfil.objects.create(usuario=self.operador_a, equipe=self.equipe_a, papel='operador')
        Perfil.objects.create(usuario=self.admin_b, equipe=self.equipe_b, papel='admin')
        Perfil.objects.create(usuario=self.admin_c, equipe=self.equipe_c, papel='admin')

        self.projeto_a = self._projeto('Projeto A', self.equipe_a)
        self.projeto_b = self._projeto('Projeto B', self.equipe_b)
        self.membro_a = self._membro('Ana', self.equipe_a)
        self.membro_b = self._membro('Bruno', self.equipe_b)
        self.feita = self._sub('feita', self.projeto_a, self.membro_a, 'feito', date(2026, 3, 10))
        self.aberta = self._sub('aberta', self.projeto_a, self.membro_a, 'a fazer', date(2026, 1, 5))
        self.outra = self._sub('outra', self.projeto_a, self.membro_a, 'a fazer', date(2026, 1, 6))
        self._sub('da b', self.projeto_b, self.membro_b, 'feito', date(2026, 3, 10))
        self.pre = self.aberta
        self.bloqueada = self.outra
        Dependencia.objects.create(
            subtarefa=self.bloqueada,
            subtarefa_dependente=self.pre,
            obrigatoria=True,
            equipe=self.equipe_a,
        )

    def _projeto(self, nome, equipe):
        return Projeto.objects.create(
            nome=nome, descricao='d', data_inicio=date(2026, 1, 1), equipe=equipe,
        )

    def _membro(self, nome, equipe):
        return Membro.objects.create(
            nome=nome, email=f'{nome}@exemplo.com', cargo='dev', equipe=equipe,
        )

    def _sub(self, titulo, projeto, membro, status, prazo):
        return Subtarefa.objects.create(
            titulo=titulo,
            descricao='d',
            projeto=projeto,
            responsavel=membro,
            prazo=prazo,
            status=status,
            equipe=projeto.equipe,
        )

    def test_lista_mostra_so_a_equipe(self):
        self.client.force_login(self.admin_a)
        resposta = self.client.get('/')
        self.assertContains(resposta, 'Projeto A')
        self.assertNotContains(resposta, 'Projeto B')

    def test_api_sem_login_recusa(self):
        resposta = self.client.get('/api/projetos/')
        self.assertEqual(resposta.status_code, 403)

    def test_api_nao_mostra_outra_equipe(self):
        self.client.force_login(self.admin_a)
        resposta = self.client.get('/api/projetos/')
        self.assertEqual(
            [item['nome'] for item in resposta.json()],
            ['Projeto A'],
        )

    def test_progresso_conta_so_a_equipe(self):
        self.client.force_login(self.admin_a)
        resposta = self.client.get('/progresso/')
        self.assertEqual(resposta.context['kpis']['total'], 3)
        self.assertEqual(resposta.context['kpis']['feitas'], 1)
        self.assertEqual(resposta.context['kpis']['percentual'], 33)

    def test_periodo_filtra_o_progresso(self):
        self.client.force_login(self.admin_a)
        resposta = self.client.get('/progresso/?inicio=2026-01-01&fim=2026-01-31')
        self.assertEqual(resposta.context['kpis']['total'], 2)
        self.assertEqual(resposta.context['kpis']['feitas'], 0)

    def test_data_invalida_nao_quebra_o_progresso(self):
        self.client.force_login(self.admin_a)
        resposta = self.client.get('/progresso/?inicio=abc')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['kpis']['total'], 3)

    def test_progresso_vazio(self):
        self.client.force_login(self.admin_c)
        resposta = self.client.get('/progresso/')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context['kpis']['percentual'], 0)
        self.assertContains(resposta, 'Nenhum projeto cadastrado.')

    def test_operador_nao_ve_serie_nem_exporta(self):
        self.client.force_login(self.operador_a)
        pagina = self.client.get('/progresso/')
        self.assertFalse(pagina.context['mostra_series'])
        exportacao = self.client.get('/progresso/csv/')
        self.assertEqual(exportacao.status_code, 403)

    def test_admin_exporta_csv_da_propria_equipe(self):
        self.client.force_login(self.admin_a)
        resposta = self.client.get('/progresso/csv/')
        self.assertEqual(resposta.status_code, 200)
        texto = resposta.content.decode()
        self.assertIn('Projeto A', texto)
        self.assertNotIn('Projeto B', texto)

    def test_nao_conclui_com_dependencia_aberta(self):
        self.bloqueada.status = 'feito'
        with self.assertRaises(ValidationError):
            self.bloqueada.full_clean()
        self.client.force_login(self.admin_a)
        resposta = self.client.patch(
            f'/api/subtarefas/{self.bloqueada.pk}/',
            {'status': 'feito'},
            content_type='application/json',
        )
        self.assertEqual(resposta.status_code, 400)
        self.pre.status = 'feito'
        self.pre.save()
        self.bloqueada.full_clean()
