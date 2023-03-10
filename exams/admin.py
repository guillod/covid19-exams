from django.contrib import admin
from django.db.models import Count
from django.forms import BaseInlineFormSet

from .models import Assignment, AssignmentFile, RenderedFiles, File

class FilesInline(admin.TabularInline):
    model = AssignmentFile
    extra = 1
    verbose_name = 'Sujet'
    verbose_name_plural = 'Sujets'

class RenderedFilesInline(admin.TabularInline):
    model = RenderedFiles
    readonly_fields = ['first_name', 'last_name', 'uploaded_at', 'files_number', ]
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('ue', 'description', 'start_at', 'end_at', )
    fields = (('ue', 'description'), ('start_at', 'end_at'), )
    inlines = [FilesInline, RenderedFilesInline]
    save_as = True

class RenderedFileInline(admin.TabularInline):
    model = File
    extra = 0

class OutputAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'no', 'first_name', 'last_name', 'uploaded_at', 'files_number', )
    fields = ('assignment', 'user', 'full_name', 'uploaded_at', )
    readonly_fields = ('full_name', )
    inlines = [RenderedFileInline]
    list_filter = ('assignment',)

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(RenderedFiles, OutputAdmin)
