from django.contrib import admin
from .models import Profile, APIUsage, Sugestao, Resposta

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan')  # Exibe o usuário e o plano na lista
    list_filter = ('plan',)         # Adiciona um filtro por plano
    search_fields = ('user__username', 'user__email')  # Permite buscar pelo nome de usuário ou e-mail
    list_editable = ('plan',)       # Permite editar o plano diretamente na lista


@admin.register(APIUsage)
class APIUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'requests_made', 'last_reset')
    search_fields = ('user__username',)
    list_filter = ('last_reset',)


class RespostaInline(admin.StackedInline):
    model = Resposta
    extra = 1  # Permite adicionar respostas diretamente

class SugestaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_envio')  # Exibe no painel
    search_fields = ('titulo', 'autor__username')  # Permite busca por título e usuário
    list_filter = ('data_envio',)  # Filtro por data
    inlines = [RespostaInline]  # Permite responder direto na sugestão

admin.site.register(Sugestao, SugestaoAdmin)
admin.site.register(Resposta)
