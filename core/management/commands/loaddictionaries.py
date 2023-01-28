import os
import re
import time

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from tqdm import tqdm

from word_deva_4.core.models import Language, Term, Text, Translation, String

class Command(BaseCommand):
    help = 'Loads dictionaries from `dictionaries` to the database'

    def process_dictionary(self, dictionary_lines):
        dictionary = {}

        errors = 0
        missing_pos = 0

        for line in dictionary_lines:
            # Ignore Comments
            if line[0] == "#":
                continue

            # Ignore errors
            if line[0] == "!":
                errors += 1
                continue

            # Read page number
            if line[:3] == "p. ":
                page = int(line[3:].strip('\n'))
                continue
            
            # Skip empty lines
            if line == "\n":
                continue

            word, pos_def_str = line.split(', ', 1)
            
            definitions = []
            pos = None

            # Read POS
            for meaning in pos_def_str.split('; '):
                if meaning[:4] == "see ":
                    pos, target_words = "synonymn", meaning[5:]
                elif meaning[:4] == "adj.":
                    pos, target_words = "adjective", meaning[5:]
                elif meaning[:4] == "adv.":
                    pos, target_words = "adverb", meaning[5:]
                elif meaning[:5] == "n. m.":
                    pos, target_words = "noun", meaning[6:]
                elif meaning[:5] == "n. f.":
                    pos, target_words = "noun", meaning[6:]
                elif meaning[:2] == "n.":
                    pos, target_words = "noun", meaning[3:]
                elif meaning[:2] == "m.":
                    pos, target_words = "noun", meaning[3:]
                elif meaning[:2] == "f.":
                    pos, target_words = "noun", meaning[3:]
                elif meaning[:5] == "v. a.":
                    pos, target_words = "verb", meaning[6:]
                elif meaning[:2] == "v.":
                    pos, target_words = "verb", meaning[3:]
                elif meaning[:7] == "interj.":
                    pos, target_words = "interjection", meaning[8:]
                elif meaning[:5] == "conj.":
                    pos, target_words = "conjunction", meaning[6:]
                elif meaning[:5] == "prep.":
                    pos, target_words = "preposition", meaning[6:]
                elif meaning[:8] == "postpos.":
                    pos, target_words = "postposition", meaning[9:]
                elif meaning[:7] == "prefix.":
                    pos, target_words = "prefix", meaning[8:]
                elif meaning[:7] == "suffix.":
                    pos, target_words = "prefix", meaning[8:]
                elif meaning[:5] == "pron.":
                    pos, target_words = "pronoun", meaning[6:]
                elif meaning[:5] == "pron.":
                    pos, target_words = "pronoun", meaning[6:]
                elif meaning[:11] == "past. part.":
                    pos, target_words = "past participle", meaning[12:]
                else:
                    pos, target_words = None, meaning
                    missing_pos += 1

                target_words = target_words.strip('\n').strip('.')

                if pos:
                    target_words = target_words.split(', ')

                    for target_word in target_words:
                        definitions.append({'pos': pos, 'word': target_word})

            dictionary[word] = definitions


        # print("Errors: ", errors)
        # print("Missing POS: ", missing_pos)

        return dictionary

    def load_dictionary(self, processed_dictionary, language, to_language):
        for word, definitions in tqdm(processed_dictionary.items(), desc="Saving Entries"):
            for definition in definitions:
                source_string, source_string_created = String.objects.get_or_create(text=word, language=language)
                target_string, target_string_created = String.objects.get_or_create(text=definition["word"], language=to_language)

                # Create translation and reverse translation
                (translation,
                 translation_created) = Translation.objects.get_or_create(source_string=source_string, target_string=target_string)
                (rtranslation,
                 rtranslation_created) = Translation.objects.get_or_create(source_string=target_string, target_string=source_string)


    def handle(self, *args, **options):
        WORD_DEVA_PROJECT_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent

        self.DICTIONARIES_DIR = Path(WORD_DEVA_PROJECT_PATH, "word_deva_4/dictionaries/")

        for file_name in os.listdir(self.DICTIONARIES_DIR):
            if file_name.endswith('.txt'):
                with open(Path(self.DICTIONARIES_DIR, file_name)) as dictionary:
                    title = dictionary.readline().replace("title: ", "").strip('\n')
                    author = dictionary.readline().replace("author: ", "").strip('\n')
                    language_code = dictionary.readline().replace("language: ", "").strip('\n')
                    to_language_code = dictionary.readline().replace("to_language: ", "").strip('\n')

                    dictionary.readline() # Empty line

                    language = Language.objects.get(code=language_code)
                    to_language = Language.objects.get(code=to_language_code)
                    dictionary_lines = dictionary.readlines()

                    processed_dictionary = self.process_dictionary(dictionary_lines)
                    self.load_dictionary(processed_dictionary, language,
                                         to_language)
