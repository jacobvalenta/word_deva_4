from django.contrib import admin

from .models import Language, String, Term, Text, Translation

class TermAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_word', 'count']
    list_filter = ['text']

    @admin.display(ordering='string__text')
    def get_word(self, obj):
        return obj.string.text

admin.site.register(Language)
admin.site.register(String)
admin.site.register(Term, TermAdmin)
admin.site.register(Text)
admin.site.register(Translation)