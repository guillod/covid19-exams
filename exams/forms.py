from django import forms

from .models import RenderedFiles


class DocumentForm(forms.ModelForm):

    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = RenderedFiles
        fields = ('no', 'firstname', 'lastname', )
        widgets = {
            'no': forms.TextInput(),
		}
