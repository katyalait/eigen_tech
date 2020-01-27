from django import forms
from .models import Document
import logging
logger = logging.getLogger(__name__)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file_name', 'file']

class FilterForm(forms.Form):
    document_set = Document.objects.all()
    number_of_words = forms.IntegerField()
    documents = forms.MultipleChoiceField(choices=[(doc.id, str(doc.file_name)) for doc in document_set], widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        document_set = Document.objects.all()
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['documents'] = forms.MultipleChoiceField(choices=[(doc.id, str(doc.file_name)) for doc in document_set], widget=forms.CheckboxSelectMultiple())
