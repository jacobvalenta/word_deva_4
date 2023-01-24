import os

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from word_deva_4.core.models import Language, Term, Text, Word

class Command(BaseCommand):
    help = 'Loads books from `books` to the database'

    def process_texts(self):
        for text in Text.objects.all():
            words = text.text.replace("'", "").replace('"', "").replace(".", "").replace(",", "").replace('।', "").replace('-', ' ').replace('!', "").replace('?', "").replace("\n", "")

            vocabulary_words = {}
            word_number = 0

            for word in words.split():
                if word in vocabulary_words:
                    vocabulary_words[word][1] += 1
                    continue

                word_number += 1
                vocabulary_words[word] = [word_number, 1]

            for word_str, (word_number, count) in vocabulary_words.items():
                word, word_created = Word.objects.get_or_create(text=word_str, language=text.language)
                term, term_created = Term.objects.get_or_create(word=word, text=text, order=word_number, count=count)


            print(len(vocabulary_words))

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
