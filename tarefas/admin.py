from django.contrib import admin

from .models import Dependencia, Membro, Projeto, Subtarefa


class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'equipe')
    list_filter = ('equipe',)


class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'equipe')
    list_filter = ('equipe',)


class SubtarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'equipe')
    list_filter = ('equipe', 'status')


class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('subtarefa_id', 'subtarefa_dependente_id', 'equipe')
    list_filter = ('equipe',)


admin.site.register(Membro, MembroAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Subtarefa, SubtarefaAdmin)
admin.site.register(Dependencia, DependenciaAdmin)
