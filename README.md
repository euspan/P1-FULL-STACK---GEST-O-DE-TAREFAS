# Gestão de Tarefas

Projeto acadêmico em Django para gerenciamento de tarefas, desenvolvido
na disciplina de Laboratório de Programação Full Stack (Universidade
de Vassouras).

## Sobre o projeto

Sistema de gestão de tarefas em que cada equipe vê somente os próprios
dados. O cadastro cobre projetos, membros, subtarefas e dependências
entre elas. Os vínculos entre subtarefa, projeto, membro e dependência
continuam em campos inteiros (`projeto_id`, `responsavel_id`,
`subtarefa_id` e `subtarefa_dependente_id`). A equipe de cada registro
é uma chave estrangeira.

## Tecnologias

- Python
- Django
- Django REST framework
- SQLite (banco de dados padrão de desenvolvimento)

## Models

- **Equipe**: nome e data de criação
- **Perfil**: liga um usuário do Django a uma equipe
- **Membro**: nome, email, cargo, ativo e equipe
- **Projeto**: nome, descrição, data de início, concluído e equipe
- **Subtarefa**: título, descrição, projeto, responsável, prazo, equipe
  e status (`a fazer`, `fazendo` ou `feito`)
- **Dependencia**: a subtarefa em `subtarefa_id` depende da subtarefa em
  `subtarefa_dependente_id`, com indicação se a dependência é obrigatória

## Funcionalidades

- Cadastro e gerenciamento dos dados pelo Django Admin
- Isolamento por equipe: as páginas e a API usam a equipe do Perfil do
  usuário logado
- Consultas nas páginas do app (exigem login):
  - `/` lista projetos, membros, subtarefas e dependências
  - `/projetos/` lista os projetos
  - `/pendentes/` lista subtarefas com status `a fazer` ou `fazendo`
  - `/buscar/?titulo=` busca subtarefas por parte do título, sem
    diferenciar maiúsculas de minúsculas (`titulo__icontains`)
  - `/status/?status=` filtra subtarefas pelo status
    (se o parâmetro não vier, usa `a fazer`)
  - `/progresso/` calcula o progresso da equipe e de cada projeto pela
    porcentagem de subtarefas com status `feito`
- API JSON, também restrita à equipe do usuário autenticado:
  - `/api/projetos/` e `/api/projetos/<id>/`
  - `/api/membros/` e `/api/membros/<id>/`
  - `/api/subtarefas/` e `/api/subtarefas/<id>/`
  - `/api/dependencias/` e `/api/dependencias/<id>/`

O status da subtarefa segue três etapas: `a fazer`, `fazendo` e `feito`.
O progresso não é um campo gravado: ele é calculado na consulta.
O Admin não impede gravar uma subtarefa como `feito` quando a
dependência ainda está aberta.

## Como rodar o projeto

```bash
# criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows

# instalar dependências
pip install -r requirements.txt

# aplicar as migrações
python manage.py migrate

# criar um usuário administrador
python manage.py createsuperuser

# rodar o servidor
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/admin`, crie uma equipe e um Perfil
ligando seu usuário a essa equipe. Sem o Perfil, as páginas pedem esse
cadastro.

Depois use `http://127.0.0.1:8000/` para as consultas,
`http://127.0.0.1:8000/progresso/` para o progresso e
`http://127.0.0.1:8000/api/projetos/` para a API. O login da API
navegável fica em `http://127.0.0.1:8000/api-auth/login/`.
