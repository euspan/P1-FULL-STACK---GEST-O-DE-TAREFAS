from django.contrib import admin

from .models import Dependencia, Membro, Projeto, Subtarefa


def _filtrar_pela_equipe(admin_obj, db_field, request, kwargs, campos):
    if request.user.is_superuser or db_field.name not in campos:
        return
    perfil = getattr(request.user, 'perfil', None)
    if perfil is None:
        return
    kwargs['queryset'] = db_field.related_model.objects.filter(equipe=perfil.equipe)


class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'equipe')
    list_filter = ('equipe',)


class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'equipe')
    list_filter = ('equipe',)


class SubtarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'projeto', 'responsavel', 'equipe')
    list_filter = ('equipe', 'status')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        _filtrar_pela_equipe(self, db_field, request, kwargs, {'projeto', 'responsavel'})
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('subtarefa', 'subtarefa_dependente', 'obrigatoria', 'equipe')
    list_filter = ('equipe',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        _filtrar_pela_equipe(
            self, db_field, request, kwargs, {'subtarefa', 'subtarefa_dependente'},
        )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Membro, MembroAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Subtarefa, SubtarefaAdmin)
admin.site.register(Dependencia, DependenciaAdmin)
