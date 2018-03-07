from django.contrib import admin

from .models import Query, Answer, Statement

admin.site.register(Query)
admin.site.register(Answer)
admin.site.register(Statement)
