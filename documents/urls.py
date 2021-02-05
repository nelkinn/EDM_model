from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('tasks/<int:pk>/', views.select_task, name='select_task'),
    path('tasks/<int:pk>/history/<int:id_answer>/', views.history_task, name='history_task'),
    path('tasks/task_new/', views.task_new, name='task_new'),
    path('tasks/mytasks/', views.my_tasks, name='my_tasks'),
    path('tasks/mytasks/<int:pk>/', views.select_mytask, name='select_mytask'),
    path('documents/', views.docs_list, name='docs_list'),
    path('documents/<str:group>', views.docs_list, name='docs_list'),
    path('documents/<int:pk>/', views.select_doc, name='select_doc'),
    path('documents/<str:group>/<int:pk>', views.select_doc, name='select_doc'),
    path('documents/doc_new/', views.doc_new, name='doc_new'),

]
