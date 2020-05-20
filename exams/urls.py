from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.list_assignments, name='home'),
    path('upload/<uuid:assignment_id>/', views.form_upload, name='upload'),
    path('download/<str:ue>/<str:other>_<uuid:rendered_id>/<str:filename>', views.download, name='download'),
    path('assignment/<uuid:assignment_id>/<str:filename>', views.assignment, name='assignment'),
    path('list/', views.list_files, name='list')
]
