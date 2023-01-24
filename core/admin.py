from django.contrib import admin

from .models import Language, Term, Text, Word

admin.site.register(Language)
admin.site.register(Term)
admin.site.register(Text)
admin.site.register(Word)