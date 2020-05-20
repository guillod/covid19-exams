from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.urls import reverse
import os, uuid

def directory_path(instance, filename):
    # assignment file
    if isinstance(instance, AssignmentFile):
        return f'assignment/{instance.assignment.id}/{filename}'
    # student file
    elif isinstance(instance, File):
        print(filename)
        r = instance.rendered
        return f'download/{r.ue}_{r.description}/{r.first_name}_{r.last_name}_{r.no}_{timezone.localtime(r.uploaded_at).strftime("%Y-%m-%dT%H:%M:%S")}_{r.id}/{filename}'
    else:
        return "garbage/{filename}"

class Assignment(models.Model):

    class Meta:
        verbose_name = 'Examen'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ue = models.CharField("Code UE", max_length=255, help_text="par exemple LU2MA100")
    description = models.CharField("Description", max_length=255)
    start_at = models.DateTimeField("Date d'ouverture")
    end_at = models.DateTimeField("Date limite de remise")

    def __str__(self):
        return f"{self.ue} - {self.description}"

    def current(self):
        return self.start_at < timezone.now() < self.end_at

    def files(self):
        if self.current():
            return self.assignmentfile_set.all()

class AssignmentFile(models.Model):

    class Meta:
        verbose_name = 'Fichier sujet'
        verbose_name_plural = 'Fichiers sujet'

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to=directory_path, max_length=500)

    def icon(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'fa-file-pdf'
        elif extension == '.ipynb':
            return 'fa-file-code'
        elif extension == '.html':
            return 'fa-file-alt'
        else:
            return 'fa-file'

    def url(self):
        return "aaa"

    def get_absolute_url(self):
        return self.file.url

    def __str__(self):
        return ""

class RenderedFiles(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name="Numéro étudiant", on_delete=models.CASCADE)
    #no = models.BigIntegerField("Numéro d'étudiant")
    #firstname = models.CharField("Prénom", max_length=255)
    #lastname = models.CharField("Nom", max_length=255)
    assignment = models.ForeignKey(Assignment, verbose_name="Examen", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField("Date de dépôt", default=timezone.now)

    @property
    def ue(self):
        return self.assignment.ue

    @property
    def description(self):
        return self.assignment.description

    @property
    def no(self):
        return self.user.username
    no.fget.short_description = "Numéro d'étudiant"

    @property
    def first_name(self):
        return self.user.first_name
    first_name.fget.short_description = 'Prénom'

    @property
    def last_name(self):
        return self.user.last_name
    last_name.fget.short_description = 'Nom'

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name
    full_name.fget.short_description = 'Nom complet'

    @property
    def files_number(self):
         return self.file_set.count()
    files_number.fget.short_description = 'Nombre de fichiers'

    def files(self):
        return self.file_set.all()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.no}"

    class Meta:
        verbose_name = 'Examen rendu'
        verbose_name_plural = 'Examens rendus'

class File(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rendered = models.ForeignKey(RenderedFiles, on_delete=models.CASCADE)
    file = models.FileField(upload_to=directory_path, max_length=500)

    class Meta:
        verbose_name = 'Fichier rendu'
        verbose_name_plural = 'Fichiers rendus'

    def icon(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'fa-file-pdf'
        elif extension == '.ipynb':
            return 'fa-file-code'
        elif extension == '.html':
            return 'fa-file-alt'
        else:
            return 'fa-file'

    def get_absolute_url(self):
        return self.file.url

    def __str__(self):
        return ""
