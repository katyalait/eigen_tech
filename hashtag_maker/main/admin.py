from django.contrib import admin
from .models import Document, Sentence, Word

admin.site.register(Document)
admin.site.register(Sentence)
admin.site.register(Word)
