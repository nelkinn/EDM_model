import os
from django.db import models
from django.conf import settings
from django.utils import timezone


class Task(models.Model):
    task_group = (
        ('Поручение', 'Поручение'),
        ('Согласование', 'Согласование'),
        ('На ознакомление', 'На ознакомление'),
        ('На подпись', 'На подпись'),
        ('На регистрацию', 'На регистрацию'),
    )

    status_list = (
        ('1', 'Задание передано'),
        ('2', 'Передан ответ'),
        ('3', 'Задание окончено'),
        ('4', 'Задание просрочено'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks', verbose_name='Поручитель')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name='Кому')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    group = models.CharField(max_length=25, choices=task_group, verbose_name='Тип', default='Поручение')
    text = models.TextField(verbose_name='Сообщение')
    quickly = models.BooleanField(verbose_name='Срочно', default=False)
    create_date = models.DateField(default=timezone.now, verbose_name='Дата создания')
    final_date = models.DateTimeField(default=timezone.now, verbose_name='Выполнить до')
    status = models.CharField(max_length=20, choices=status_list, default='1', verbose_name='Этап выполнения')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def only_date(self):
        return self.created_date.strftime("%d %A %Y")

    def displayStatus(tself):
        if self.status == '1':
            if self.receiver == id:
                return 'Ожидание выполнения'
        elif self.status == '2':
            if self.receiver == id:
                return 'Ожидание ответа'
            elif self.author == id:
                return 'Получен ответ'
        elif self.status == '4':
            if self.author == id:
                return 'Задание не было выполнено'

    def __str__(self):
        return self.title

    def test(self):
        return 0

class FileTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/tasks', verbose_name='Файл', null=True, blank=True)

    class Meta:
        verbose_name = 'Файл задачи'
        verbose_name_plural = 'Файлы задач'

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def css_class(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'pdf'
        if extension == '.docx':
            return 'word'
        if extension == '.xlsx':
            return 'xlsx'

    def __str__(self):
        return self.file.name


class TaskAnswer(models.Model):
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    text = models.TextField(verbose_name='Сообщение', default='')

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    def number(self):
        return self.name[len(self.name)-2:]

    def __str__(self):
        return self.task.title + ': ' + self.name

class FileAnswer(models.Model):
    answer = models.ForeignKey(TaskAnswer, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/answers', verbose_name='Файл', null=True, blank=True)

    class Meta:
        verbose_name = 'Файл ответа'
        verbose_name_plural = 'Файлы ответов'

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def css_class(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'pdf'
        if extension == '.docx':
            return 'word'
        if extension == '.xlsx':
            return 'xlsx'

    def __str__(self):
        return self.file.name

class Document(models.Model):
    doc_group = (
        ('Приказ', 'Приказ'),
        ('Договор', 'Договор'),
        ('Протокол', 'Протокол'),
        ('Отчет', 'Отчет'),
        ('Акт', 'Акт'),
        ('Счет', 'Счет'),
        ('Накладная', 'Накладная'),
        ('Докладная записка', 'Докладная записка'),
    )
    registrator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='registrator', verbose_name='Регистратор')
    title = models.CharField(max_length=40, verbose_name='Заголовок')
    group = models.CharField(max_length=25, choices=doc_group, verbose_name='Тип')
    author = models.CharField(max_length=30, verbose_name='От кого')
    create_date = models.DateTimeField(default=timezone.now)
    signature = models.BooleanField(verbose_name='Требуется подпись')
    signer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='signer', verbose_name='Подписант')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def only_date(self):
        return self.create_date.strftime("%d %A %Y")

    def __str__(self):
        return self.title


class FileDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents', verbose_name='Файл')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def css_class(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'pdf'
        if extension == '.docx':
            return 'word'
        if extension == '.xlsx':
            return 'xlsx'

    def __str__(self):
        return self.file.name
