from django import forms
from .models import ContactNote

class ContactNoteForm(forms.ModelForm):
    class Meta:
        model = ContactNote
        fields = ['name', 'email','message']
        widgets = {'message':forms.Textarea(attrs={'rows':5})}



    def clean_message(self):
        if self.cleaned_data['message']:
            if len(self.cleaned_data['message'].strip()) < 10 :
                raise forms.ValidationError('Message must contain at least 10 characters.')
            else :
                return self.cleaned_data['message']
        else :
            raise forms.ValidationError("Message must contain at least 10 characters.")


