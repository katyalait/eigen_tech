from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import re
from .models import Sentence, Word

def create_sentence_objects(document):
    """
    Creates sentence objects in the database along with the associated word objects.
    param document: Document populated model
    return: None
    """
    doc_file = open(document.file.path, "r").read()
    sentences = sent_tokenize(doc_file)

    stop_words = set(stopwords.words('english'))
    stop_words.add('let')
    for sentence in sentences:
        if len(sentence)<=1:
            continue
        # Extract leading and ending quotation marks
        sentence = sentence.strip('\"')
        new_sentence = Sentence(document_id=document, sentence_text=sentence)
        new_sentence.save()
        word_tokens = word_tokenize(sentence)
        for i in range(len(word_tokens)):
            word = (word_tokens[i]).lower()
            if not word in stop_words and word.isalpha():
                # Create objects only for alphabetic, non-stop words
                new_word = Word(document_id=document, sentence_id=new_sentence, word=word, index_in_sentence=i)
                new_word.save()

def create_table(word_set, allowed_docs):
    """
    Creates content for filtered table given a set of words and the allowed docs.
    param word_set: list of strings corresponding to words in the database
    param allowed_docs: list of document ids allowed
    return: table dictionary with each word in word_set as key and a dictionary
            as its value with documents and sentences word is in and the number of
            occurences of the word.
    """
    table = {}
    for word in word_set:
        all_words= list(Word.objects.filter(word=word, document_id__in=allowed_docs))
        table[word] = {'documents':[], 'sentences':[], 'occurences': 0}
        occurences = 0
        for item in all_words:
            sentence_objects = list(Sentence.objects.filter(id=item.sentence_id.id))
            for sentence in sentence_objects:
                if str(sentence.document_id.id) in allowed_docs:
                    # Convert to str because doc_ids stored as strings
                    if not sentence.document_id.file_name in table[word]['documents']:
                        table[word]['documents'].append(sentence.document_id.file_name)
                    # Create tokens out of the words/punctuation in the sentence
                    word_tokens = word_tokenize(sentence.sentence_text)
                    # Surround the word by <b> element
                    word_tokens.insert(item.index_in_sentence, "<b>")
                    word_tokens.insert(item.index_in_sentence+2, "</b>")
                    # Convert back to sentence use detokenizer method
                    new_sent = TreebankWordDetokenizer().detokenize(word_tokens)
                    occurences +=1
                    table[word]['sentences'].append(new_sent)
        table[word]['occurences'] = occurences
    return table
