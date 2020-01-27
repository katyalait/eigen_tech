from django.db import models

class Document(models.Model):
    file_name = models.CharField(max_length=120)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.file_name

class Sentence(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    sentence_text = models.CharField(max_length=500)

    def __str__(self):
        return self.sentence_text

class Word(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    sentence_id = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)
    index_in_sentence = models.IntegerField()

    def __str__(self):
        return self.word
