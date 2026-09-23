from django.http import HttpResponse


def inicio(request):
    html = '''
    <h1>Gestor de Tarefas</h1>
    <ul>
        <li><a href="/admin/">Django Admin</a></li>
        <li><a href="/projetos/">Listar Projetos</a></li>
        <li><a href="/pendentes/">Listar Subtarefas Pendentes</a></li>
        <li><a href="/buscar/?titulo=">Buscar Subtarefa por Título</a></li>
        <li><a href="/status/?status=a fazer">Filtrar por Status</a></li>
    </ul>
    '''
    return HttpResponse(html)