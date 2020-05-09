from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.list_assignments, name='home'),
    #path('upload', views.form_upload, name='upload'),
    path('upload/<int:assignment_id>', views.form_upload, name='upload')
    #path('/admin', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
