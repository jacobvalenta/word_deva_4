import re
import os

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from tqdm import tqdm

from word_deva_4.core.models import Language, Term, Text, String

class Command(BaseCommand):
    help = 'Loads books from `books` to the database'

    def process_texts(self):
        for text in Text.objects.all():
            terms = Term.objects.filter(text=text)
            terms.update(order=0)

            words = re.sub(r"(?:\'|\"|\.|\,|।|\!|\?|\n|\#\s)", "", text.text)
            words = words.split()

            vocabulary_words = {}
            word_number = 0

            word_count = len(words)

            for word in words:
                if word in vocabulary_words:
                    vocabulary_words[word][1] += 1
                    continue

                word_number += 1
                vocabulary_words[word] = [word_number, 1]

            for word_str, (word_number, count) in tqdm(vocabulary_words.items(), desc="Creating Words and Terms"):
                word, word_created = String.objects.get_or_create(text=word_str, language=text.language)
                term, term_created = Term.objects.get_or_create(string=word, text=text, defaults={"order": word_number, "count": count})
                term.order = word_number
                term.count = count
                term.save()

            vocabulary_count = len(vocabulary_words)

            text.word_count = word_count
            text.vocabulary_count = vocabulary_count

            text.save()

            terms_to_delete = Term.objects.filter(order=0)
            terms_to_delete.delete()

    def save_books_to_db(self):
        for file_name in os.listdir(self.BOOK_DIR):
            if file_name.endswith('.txt'):
                with open(Path(self.BOOK_DIR, file_name)) as book:
                    title = book.readline().strip("title: ").strip('\n')
                    author = book.readline().strip("author: ").strip('\n')
                    language_code = book.readline().strip("language: ").strip('\n')

                    book.readline() # Empty line

                    language = Language.objects.get(code=language_code)
                    text = ''.join(book.readlines())

                    text_obj, text_obj_created = Text.objects.get_or_create(title=title, author=author, language=language)
                    text_obj.text = text
                    text_obj.save()

    def handle(self, *args, **options):
        WORD_DEVA_PROJECT_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent

        self.BOOK_DIR = Path(WORD_DEVA_PROJECT_PATH, "word_deva_4/books/")

        self.save_books_to_db()
        self.process_texts()
