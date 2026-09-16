from django.contrib import admin
from .models import Projeto, Subtarefa, Dependencia, Membro

admin.site.register(Projeto)
admin.site.register(Subtarefa)
admin.site.register(Dependencia)
admin.site.register(Membro)
