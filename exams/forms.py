from django import forms
from django.core.exceptions import ValidationError

from .models import RenderedFiles

def validator_file(obj):
    max_filesize = 20 # in MB
    file_size = obj.size
    print(file_size)
    if file_size > max_filesize*1024*1024:
        raise ValidationError(f"La taille maximale autorisée est {max_filesize}MB.")

class DocumentForm(forms.ModelForm):

    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), validators=[validator_file])

    class Meta:
        model = RenderedFiles
        fields = ('no', 'firstname', 'lastname', )
        widgets = {
            'no': forms.TextInput(),
		}
