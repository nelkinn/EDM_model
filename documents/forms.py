from django import forms
from .models import Document, TaskAnswer, Task


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'author', 'group', 'signature')

"""class FileForm(forms.ModelForm):
    class Meta:
        model = FileDocument
        fields = ('file',)"""

class FileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class TaskAnwswerForm(forms.ModelForm):
    class Meta:
        model = TaskAnswer
        fields = 'text',


class FileTaskForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'receiver', 'group', 'text', 'quickly', 'final_date',)
