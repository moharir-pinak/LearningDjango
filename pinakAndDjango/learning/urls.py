from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.learning, name='learnings_home'),
    path('<int:pk>/', views.learning_detail, name='learning_detail'),
    # path('learnings_forms/', views.learning_form, name='learning_forms'),
    path('learnings_forms/', views.learning_form, name='learning_forms'),
    
]