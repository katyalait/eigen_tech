from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Count
from .models import Document, Word, Sentence
from .forms import DocumentForm, FilterForm
from .document_parser import create_sentence_objects, create_table


class FilteredWordView(ListView):
    template_name = 'filtered_words.html'
    model = Word
    context_object_name = 'words'
    document_ids = [doc.id for doc in Document.objects.all()]
    queryset = []

    def get_queryset(self):
        self.form = FilterForm(data=self.request.GET or None)
        if self.request.GET and self.form.is_valid():
            # filter using the form's cleaned_data
            number_of_words = int(self.request.GET.get('number_of_words'))
            documents_to_use = self.request.GET.getlist('documents')
            self.document_ids = documents_to_use
            queryset = Word.objects.filter(document_id__in=documents_to_use).values_list('word', flat=True).annotate(word_count=Count('word')).order_by('-word_count').distinct()[:number_of_words]
        else:
            queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        """Extract table to display given form filters"""
        context_data = super().get_context_data(**kwargs)
        word_set = list(context_data['object_list'])
        table = create_table(word_set, self.document_ids)
        context_data['table'] = table
        context_data['form'] = self.form
        return context_data

class UploadFileView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'upload_document.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()

        """Create sentence and word objects from the document."""
        create_sentence_objects(self.object)
        return super().form_valid(form)
