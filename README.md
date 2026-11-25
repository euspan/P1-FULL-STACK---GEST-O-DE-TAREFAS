# Gestão de Tarefas

Projeto acadêmico em Django para gerenciamento de tarefas, desenvolvido
na disciplina de Laboratório de Programação Full Stack (Universidade
de Vassouras).

## Sobre o projeto

Sistema básico de back-end para gestão de tarefas em equipe, com
cadastro de projetos, membros, subtarefas e dependências entre elas.
Os vínculos são guardados em campos inteiros (`projeto_id`,
`responsavel_id`, `subtarefa_id` e `subtarefa_dependente_id`).

## Tecnologias

- Python
- Django
- SQLite (banco de dados padrão de desenvolvimento)

## Models

- **Membro**: nome, email, cargo, ativo
- **Projeto**: nome, descrição, data de início, concluído
- **Subtarefa**: título, descrição, projeto, responsável, prazo e status
  (`a fazer`, `fazendo` ou `feito`)
- **Dependencia**: a subtarefa em `subtarefa_id` depende da subtarefa em
  `subtarefa_dependente_id`, com indicação se a dependência é obrigatória

## Funcionalidades

- Cadastro e gerenciamento dos dados pelo Django Admin
- Consultas nas páginas do app:
  - `/` lista projetos, membros, subtarefas e dependências
  - `/projetos/` lista os projetos
  - `/pendentes/` lista subtarefas com status `a fazer` ou `fazendo`
  - `/buscar/?titulo=` busca subtarefas por parte do título, sem
    diferenciar maiúsculas de minúsculas (`titulo__icontains`)
  - `/status/?status=` filtra subtarefas pelo status
    (se o parâmetro não vier, usa `a fazer`)

O status da subtarefa segue três etapas: `a fazer`, `fazendo` e `feito`.
O Admin não impede gravar uma subtarefa como `feito` quando a
dependência ainda está aberta.

## Como rodar o projeto

```bash
# criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows

# instalar dependências
pip install django

# aplicar as migrações
python manage.py migrate

# criar um usuário administrador
python manage.py createsuperuser

# rodar o servidor
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` para as consultas e
`http://127.0.0.1:8000/admin` para gerenciar os dados.
