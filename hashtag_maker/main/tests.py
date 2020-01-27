from django.test import TestCase
from .models import Document, Sentence, Word
from .forms import DocumentForm, FilterForm
from .document_parser import create_sentence_objects, create_table
from django.core.files import File
from django.urls import reverse

from django.db.models import Count
import os
from django.conf import settings

class DocumentTest(TestCase):

    def create_document(self, file_name="test_file.txt", file="documents/test_file.txt"):
        filepath = os.path.join(settings.MEDIA_ROOT, file)
        fp = File(open(filepath, "rb"))
        doc = Document.objects.create(file_name=file_name, file=fp)
        doc.save()
        return doc

    def test_document_creation(self, filename="test_file.txt"):
        doc = self.create_document()
        self.assertTrue(isinstance(doc, Document))
        self.assertEqual(doc.file_name, filename)

class SentenceTest(TestCase):

    def create_sentence(self, doc, sentence_text="Example sentence"):
        return Sentence.objects.create(document_id=doc, sentence_text=sentence_text)

    def test_sentence_creation(self, sentence_text="Example sentence"):
        doc = DocumentTest().create_document()
        sentence = self.create_sentence(doc)
        self.assertTrue(isinstance(sentence, Sentence))
        self.assertEqual(sentence.document_id, doc)
        self.assertEqual(sentence.sentence_text, sentence_text)

class TestDocumentParser(TestCase):
    sentences = [["Good Morning America.", "Thank you, and God Bless the United States of America."],["Hello America, it is another great day in our free country.", "Count your blessings and thank your loved ones."]]
    words = [["good", "morning", "america", "thank", "god", "bless", "united", "states", "america"],["hello", "america", "another", "great", "day", "free", "country", "count", "blessings", "thank", "loved", "ones"]]
    table_1 = {"america": {"documents": ["test2.txt"], "sentences": ["<b> America </b>, America, America, it is another great, great day in our free country.", "America, <b> America </b>, America, it is another great, great day in our free country.", "America, America, <b> America </b>, it is another great, great day in our free country."], "occurences":3}, "great": {"documents": ["test2.txt"], "sentences": ["America, America, America, it is another <b> great </b>, great day in our free country.", "America, America, America, it is another great, <b> great </b> day in our free country."], "occurences":2}}

    def test_create_sentence_objects(self):
        document_1 = Document(file_name="test_file.txt", file="documents/test_file.txt")
        document_1.save()
        create_sentence_objects(document_1)
        doc_words = Word.objects.filter(document_id=document_1).values_list('word', flat=True)
        doc_sents = Sentence.objects.filter(document_id=document_1).values_list('sentence_text', flat=True)
        for i in range(len(doc_words)):
            self.assertEqual(self.words[0][i], doc_words[i])
        for i in range(len(doc_sents)):
            self.assertEqual(self.sentences[0][i], doc_sents[i])

    def test_create_table(self, number_of_words=2):
        document_2 = Document(file_name="test2.txt", file="documents/test_file2.txt")
        document_2.save()
        create_sentence_objects(document_2)
        # Testing only second document
        allowed_doc_ids = [(str(document_2.id))]
        word_set = Word.objects.filter(document_id__in=allowed_doc_ids).values_list('word', flat=True).annotate(word_count=Count('word')).order_by('-word_count').distinct()[:number_of_words]
        table =  create_table(word_set, allowed_doc_ids)
        for word in table:
            self.assertEqual(table[word]['documents'],self.table_1[word]['documents'])
            self.assertEqual(table[word]['sentences'],self.table_1[word]['sentences'])
            self.assertEqual(table[word]['occurences'],self.table_1[word]['occurences'])

class TestViews(TestCase):
    def test_filtered_list_view(self):
        #d = DocumentTest().create_document()
        url = reverse("home")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_valid_form(self):
        document_1 = Document(file_name="test_file.txt", file="documents/test_file.txt")
        document_1.save()
        data = {'number_of_words': "2", 'documents': [str(document_1.id)]}
        form = FilterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'number_of_words': '', 'documents': [1000]}
        form = FilterForm(data=data)
        self.assertFalse(form.is_valid())
