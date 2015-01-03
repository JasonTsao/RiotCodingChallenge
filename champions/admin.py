from django.contrib import admin
from champions.models import Champion, Spell, GeneralSpell

admin.site.register(Champion)
admin.site.register(Spell)
admin.site.register(GeneralSpell)