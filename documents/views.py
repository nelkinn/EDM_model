from django.shortcuts import render, get_object_or_404, HttpResponse
from django.utils import timezone
from .models import Task, Document, FileDocument, TaskAnswer, FileTask
from .forms import DocumentForm, FileForm, TaskAnwswerForm, FileTaskForm, TaskForm
from django.shortcuts import redirect
from django.urls import resolve
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth.models import User


def main(request):
    return render(request, 'documents/base.html', {})


def tasks_list(request):
    today = datetime.now().date()
    yesterday = datetime.now().date() - timedelta(days=1)
    actual_tasks = Task.objects.filter(Q(receiver__lte=request.user), Q(status='1') | Q(status='2')).order_by('final_date')
    today_tasks = Task.objects.filter(Q(receiver__lte=request.user), Q(create_date=today)).order_by('-create_date')
    yesterday_tasks = Task.objects.filter(Q(receiver__lte=request.user), Q(create_date=yesterday)).order_by('-create_date')
    later_tasks = Task.objects.filter(Q(receiver__lte=request.user), Q(create_date__range=[yesterday - timedelta(days=27), yesterday - timedelta(days=1)])).order_by('-create_date')
    latTasks_list = []
    for task in later_tasks:
        latTasks_list.append({'date': task.create_date, 'object': task})
    return render(request, 'documents/task_list.html', {'actual_tasks': actual_tasks, 'today_tasks': today_tasks,
                                                        'yesterday_tasks': yesterday_tasks, 'today': today, 'yesterday': yesterday,
                                                        'later_tasks': later_tasks, 'latTasks_list': latTasks_list})


def my_tasks(request):
    today = datetime.now().date()
    yesterday = datetime.now().date() - timedelta(days=1)
    my_tasks = Task.objects.filter(Q(author__lte=request.user), Q(status='1') | Q(status='2')).order_by('final_date')
    today_tasks = Task.objects.filter(Q(author__lte=request.user), Q(create_date=today)).order_by('-create_date')
    yesterday_tasks = Task.objects.filter(Q(author__lte=request.user), Q(create_date=yesterday)).order_by('-create_date')
    later_tasks = Task.objects.filter(Q(author__lte=request.user), Q(create_date__range=[yesterday - timedelta(days=27), yesterday - timedelta(days=1)])).order_by('-create_date')
    latTasks_list = []
    for task in later_tasks:
        latTasks_list.append({'date': task.create_date, 'object': task})
    return render(request, 'documents/task_mylist.html', {'my_tasks': my_tasks, 'today_tasks': today_tasks,
                                                        'yesterday_tasks': yesterday_tasks, 'today': today, 'yesterday': yesterday,
                                                        'later_tasks': later_tasks, 'latTasks_list': latTasks_list})


def select_task(request, pk):
    count = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk)).count()
    answers = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk))
    latest_answer = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk)).order_by('-id')
    if answers:
        latest_answer = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk)).order_by('-id')[0]
    if request.method == 'POST':
        answerForm = TaskAnwswerForm(request.POST)
        fileForm = FileTaskForm(request.FILES)
        if answerForm.is_valid():
            selection_task = Task.objects.get(pk=pk)
            selection_task.status = '2'
            selection_task.save()
            answer = answerForm.save(commit=False)
            answer.author = request.user
            answer.task = Task.objects.get(pk=pk)
            answer.name = 'Отчет о выполнении №' + str(count + 1)
            answer.save()
            if fileForm.is_valid():
                files = request.FILES.getlist('files')
                for f in files:
                    file = FileTaskForm(answer=answer, file=f)
                    file.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        selection_task = Task.objects.get(pk=pk)
        answerForm = TaskAnwswerForm()
        fileForm = FileTaskForm()
        return render(request, 'documents/task_info.html', {'selection_task': selection_task, 'answerForm': answerForm,
                                                            'fileForm': fileForm, 'answers': answers, 'latest_answer': latest_answer})


def select_mytask(request, pk):
    count = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk)).count()
    answers = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk))
    latest_answer = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk)).order_by('-id')
    if answers:
        latest_answer = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk)).order_by('-id')[0]
    if request.method == 'POST':
        answerForm = TaskAnwswerForm(request.POST)
        fileForm = FileTaskForm(request.FILES)
        if answerForm.is_valid():
            selection_task = Task.objects.get(pk=pk)
            selection_task.status = '2'
            selection_task.save()
            answer = answerForm.save(commit=False)
            answer.author = request.user
            answer.task = Task.objects.get(pk=pk)
            answer.name = 'Отчет о выполнении №' + str(count + 1)
            answer.save()
            if fileForm.is_valid():
                files = request.FILES.getlist('files')
                for f in files:
                    file = FileTaskForm(answer=answer, file=f)
                    file.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        selection_task = Task.objects.get(pk=pk)
        answerForm = TaskAnwswerForm()
        fileForm = FileTaskForm()
        return render(request, 'documents/task_myinfo.html', {'selection_task': selection_task, 'answerForm': answerForm,
                                                            'fileForm': fileForm, 'answers': answers, 'latest_answer': latest_answer})


def history_task(request, pk, id_answer):
    count = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk)).count()
    answers = TaskAnswer.objects.filter(task=Task.objects.get(pk=pk))
    selection_task = Task.objects.get(pk=pk)
    selection_answer = TaskAnswer.objects.get(pk=id_answer)
    answer_file = selection_answer.fileanswer_set.all()
    return render(request, 'documents/task_info.html', {'selection_task': selection_task, 'answers': answers,
                                                        'selection_answer': selection_answer, 'answer_file': answer_file})


def task_new(request):
    if request.method == 'POST':
        taskForm = TaskForm(request.POST)
        fileForm = FileTaskForm(request.FILES)
        if taskForm.is_valid():
            task = taskForm.save(commit=False)
            task.author = request.user
            task.save()
            if fileForm.is_valid():
                files = request.FILES.getlist('files')
                for f in files:
                    file = FileTask(task=task, file = f)
                    file.save()
            return redirect('select_task', task.pk)
    else:
        taskForm = TaskForm()
        taskForm.fields["receiver"].queryset = User.objects.exclude(pk=request.user.id)
        fileForm = FileTaskForm()
    return render(request, 'documents/task_new.html', {'taskForm': taskForm, 'fileForm': fileForm})


def docs_list(request, group=''):
    if group == '':
        docs = Document.objects.all().order_by('-create_date')
    else:
        docs = Document.objects.filter(group=group).order_by('-create_date')
    current_url = request.path
    return render(request, 'documents/doc_list.html', {'docs': docs, 'test': current_url})


def select_doc(request, pk, group=''):
    test = request.META.get('HTTP_REFERER')
    if group == '':
        docs = Document.objects.all().order_by('-create_date')
    else:
        docs = Document.objects.filter(group=group).order_by('-create_date')
    selection_doc = Document.objects.get(pk=pk)
    doc_file = selection_doc.filedocument_set.all()
    return render(request, 'documents/doc_info.html', {'docs': docs, 'doc_file': doc_file, 'selection_doc': selection_doc})


def doc_new(request):
    if request.method == 'POST':
        docForm = DocumentForm(request.POST)

        if docForm.is_valid():
            doc = docForm.save(commit=False)
            files = request.FILES.getlist('files')
            doc.registrator = request.user
            doc.save()
            for f in files:
                file = FileDocument(document=doc, file = f)
                file.save()
            return redirect('docs_list')
    else:
        docForm = DocumentForm()
        fileForm = FileForm()
    return render(request, 'documents/doc_new.html', {'docForm': docForm, 'fileForm': fileForm})
