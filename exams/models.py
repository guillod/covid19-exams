from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
import os

def directory_path(instance, filename):
    # assignment file
    if isinstance(instance, AssignmentFile):
        random = get_random_string(length=32)
        return f'Assignments/{instance.assignment.id}_{random}/{filename}'
    # student file
    elif isinstance(instance, File):
        r = instance.rendered
        return f'Outputs/{r.ue}/{r.firstname}_{r.lastname}_{r.no}_{timezone.localtime(r.uploaded_at).strftime("%Y-%m-%dT%H:%M:%S")}/{filename}'
    else:
        return "garbage/{filename}"

class Assignment(models.Model):

    class Meta:
        verbose_name = 'Examen'

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

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to=directory_path)

    @property
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

    def __str__(self):
        return ""

class RenderedFiles(models.Model):

    no = models.BigIntegerField("Numéro d'étudiant")
    firstname = models.CharField("Prénom", max_length=255)
    lastname = models.CharField("Nom", max_length=255)
    assignment = models.ForeignKey(Assignment, verbose_name="Examen", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField("Date de dépôt", default=timezone.now)

    @property
    def ue(self):
        return self.assignment.ue

    def files_number(self):
         return self.file_set.count()
    files_number.short_description = 'Nombre de fichiers'

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.no}"

    class Meta:
        verbose_name = 'Examen rendu'
        verbose_name_plural = 'Examens rendus'

class File(models.Model):
    rendered = models.ForeignKey(RenderedFiles, on_delete=models.CASCADE)
    file = models.FileField(upload_to=directory_path)

    class Meta:
        verbose_name = 'Fichier rendu'
        verbose_name_plural = 'Fichiers rendus'
