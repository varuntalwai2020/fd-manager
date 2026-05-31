from django.urls import path
from .views import (
    dashboard,
    add_fd,
    edit_fd,
    delete_fd,
    mis_report
)
from .views import export_excel
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add/', add_fd, name='add_fd'),
    path('edit/<int:id>/', edit_fd, name='edit_fd'),
    path('delete/<int:id>/', delete_fd, name='delete_fd'),
    path('mis/', mis_report, name='mis_report'),
    path('export/excel/', export_excel, name='export_excel'),
    
]