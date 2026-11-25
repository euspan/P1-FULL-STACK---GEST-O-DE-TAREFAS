from django.contrib import admin

from .models import Equipe, Perfil


class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criada_em')


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'equipe', 'papel')
    list_filter = ('equipe', 'papel')


admin.site.register(Equipe, EquipeAdmin)
admin.site.register(Perfil, PerfilAdmin)
