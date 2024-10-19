from django.contrib import admin

from djangofun.django_x_wow.models import Character, SimcScore


class SimcScoreAdmin(admin.ModelAdmin):
    readonly_fields = ('rating_time',)


admin.site.register(Character)
admin.site.register(SimcScore)
