from django.db import models

class Language(models.Model):
	name = models.CharField(max_length=48)
	local_name = models.CharField(max_length=48)
	code = models.CharField(max_length=5)

	def __str__(self):
		return self.code

class Word(models.Model):
	text = models.CharField(max_length=32)
	language = models.ForeignKey('Language', on_delete=models.CASCADE)

class Term(models.Model):
	word = models.ForeignKey('Word', on_delete=models.CASCADE)
	text = models.ForeignKey('Text', on_delete=models.CASCADE)
	order = models.PositiveIntegerField()
	count = models.PositiveIntegerField()

class Text(models.Model):
	title = models.CharField(max_length=127)
	author = models.CharField(max_length=127)
	language = models.ForeignKey('Language', on_delete=models.CASCADE)

	text = models.TextField()

	word_count = models.PositiveIntegerField(default=0, blank=True, null=True)
	vocabulary_count = models.PositiveIntegerField(default=0, blank=True, null=True)
	head_word_count = models.PositiveIntegerField(default=0, blank=True, null=True)

	def __str__(self):
		return "{0} by {1}".format(self.title, self.author)