# Word Deva (`word_deva_4`)

## Installing

	git clone https://github.com/jacobvalenta/word_deva_4.git
	cd word_deva_4

	python manage.py migrate
	python manage.py loaddata "languages"
	python manage.py loaddictionaries
	python manage.py loadbooks

## Testing

	manage.py test