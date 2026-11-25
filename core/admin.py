from django.contrib import admin

from .models import Equipe, Perfil


class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criada_em')


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'equipe')
    list_filter = ('equipe',)


admin.site.register(Equipe, EquipeAdmin)
admin.site.register(Perfil, PerfilAdmin)
