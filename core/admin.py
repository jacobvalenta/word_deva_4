from django.contrib import admin

from .models import Language, String, Term, Text

admin.site.register(Language)
admin.site.register(String)
admin.site.register(Term)
admin.site.register(Text)