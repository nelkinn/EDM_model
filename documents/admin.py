from django.contrib import admin
from .models import Task, Document, FileDocument, FileTask, TaskAnswer, FileAnswer

admin.site.register(Task)
admin.site.register(FileTask)
admin.site.register(TaskAnswer)
admin.site.register(FileAnswer)
admin.site.register(Document)
admin.site.register(FileDocument)
