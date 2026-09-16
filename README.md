# Gestão de Tarefas

Projeto acadêmico em Django para gerenciamento de tarefas, desenvolvido
na disciplina de Laboratório de Programação Full Stack (Universidade
de Vassouras).

## Sobre o projeto

Sistema básico de back-end para gestão de tarefas em equipe, com
cadastro de projetos, membros, subtarefas e dependências entre elas.

## Tecnologias

- Python
- Django
- SQLite (banco de dados padrão de desenvolvimento)

## Models

- **Membro**: nome, email, cargo, ativo
- **Projeto**: nome, descrição, data de início, concluído
- **Subtarefa**: título, descrição, projeto, responsável, prazo, concluída
- **Dependencia**: relação entre subtarefas (uma subtarefa depende da
  conclusão de outra), com indicação se é obrigatória

## Funcionalidades

- Cadastro e gerenciamento dos dados pelo Django Admin
- Checagem manual de dependências via ORM antes de concluir uma
  subtarefa (evita marcar tarefas como concluídas fora de ordem)

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

Acesse `http://127.0.0.1:8000/admin` para gerenciar os dados.


