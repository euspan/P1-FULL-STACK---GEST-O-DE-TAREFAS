# Gestão de Tarefas

Projeto acadêmico em Django para gerenciamento de tarefas, desenvolvido
na disciplina de Laboratório de Programação Full Stack (Universidade
de Vassouras).

## Sobre o projeto

Sistema de gestão de tarefas em que cada equipe vê somente os próprios
dados. O cadastro cobre projetos, membros, subtarefas e dependências
entre elas. Projeto, responsável e as duas pontas da dependência são
ForeignKey, sempre da mesma equipe. Cada usuário entra por um
Perfil, com a equipe e o papel `admin` ou `operador`.

## Tecnologias

- Python
- Django
- Django REST framework
- SQLite (banco de dados padrão de desenvolvimento)

## Models

- **Equipe**: nome e data de criação
- **Perfil**: liga um usuário do Django a uma equipe e define o papel
  (`admin` ou `operador`)
- **Membro**: nome, email, cargo, ativo e equipe
- **Projeto**: nome, descrição, data de início, concluído e equipe
- **Subtarefa**: título, descrição, projeto, responsável, prazo, equipe
  e status (`a fazer`, `fazendo` ou `feito`)
- **Dependencia**: a subtarefa depende de outra, com indicação se a
  dependência é obrigatória

## Funcionalidades

- Cadastro e gerenciamento dos dados pelo Django Admin
- Isolamento por equipe: as páginas e a API usam a equipe do Perfil do
  usuário logado
- Papéis: o `admin` vê o gráfico (Chart.js) e exporta o CSV; o operador vê
  as listas, o progresso e o ranking
- Uma subtarefa não passa para `feito` enquanto a dependência
  obrigatória estiver aberta. A mesma regra vale no Admin e na API
- Consultas nas páginas do app (exigem login):
  - `/` lista projetos, membros, subtarefas e dependências
  - `/projetos/` lista os projetos
  - `/pendentes/` lista subtarefas com status `a fazer` ou `fazendo`
  - `/buscar/?titulo=` busca subtarefas por parte do título, sem
    diferenciar maiúsculas de minúsculas (`titulo__icontains`)
  - `/status/?status=` filtra subtarefas pelo status
    (se o parâmetro não vier, usa `a fazer`)
  - `/progresso/` calcula o progresso da equipe e de cada projeto pela
    porcentagem de subtarefas com status `feito`. Aceita `inicio` e
    `fim` no prazo, mostra o ranking de responsáveis e, para o
    `admin`, o gráfico (Chart.js) por mês
  - `/progresso/csv/` baixa esse mesmo recorte. Só o `admin`
- API JSON, também restrita à equipe do usuário autenticado:
  - `/api/projetos/` e `/api/projetos/<id>/`
  - `/api/membros/` e `/api/membros/<id>/`
  - `/api/subtarefas/` e `/api/subtarefas/<id>/`
  - `/api/dependencias/` e `/api/dependencias/<id>/`

O status da subtarefa segue três etapas: `a fazer`, `fazendo` e `feito`.
O progresso não é um campo gravado: ele é calculado na consulta.

## Como rodar o projeto

```bash
# criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows

# instalar dependências
pip install -r requirements.txt

# aplicar as migrations
python manage.py migrate

# criar um superuser
python manage.py createsuperuser

# rodar os tests
python manage.py test

# rodar o servidor
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/admin`, crie uma equipe e um Perfil
ligando seu usuário a essa equipe. No papel, escolha Administrador
(`admin`) para ver o gráfico e o CSV. Sem o Perfil, as páginas pedem esse
cadastro.

Depois use `http://127.0.0.1:8000/` para as consultas,
`http://127.0.0.1:8000/progresso/` para o progresso e
`http://127.0.0.1:8000/api/projetos/` para a API. O login da API
navegável fica em `http://127.0.0.1:8000/api-auth/login/`.
