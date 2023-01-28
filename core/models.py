from django.db import models

class Language(models.Model):
	name = models.CharField(max_length=48)
	local_name = models.CharField(max_length=48)
	code = models.CharField(max_length=5)

	def __str__(self):
		return self.code

class String(models.Model):
	text = models.CharField(max_length=100)
	phrase = models.BooleanField(default=False)
	language = models.ForeignKey('Language', on_delete=models.CASCADE)

	def __str__(self):
		return self.text

class Translation(models.Model):
	source_string = models.ForeignKey('String', related_name="source_string",
									on_delete=models.CASCADE)
	target_string = models.ForeignKey('String', related_name="target_string",
								  on_delete=models.CASCADE)

	relevance = models.DecimalField(decimal_places=4, max_digits=5,
									blank=True, null=True)

	# dictionary = models.ForeignKey('Dictionary', blank=True, null=True,
	# 							   on_delete=models.CASCADE)
	notes = models.CharField(max_length=120, blank=True, null=True)

	def __str__(self):
		return "{0} = {1}".format(self.source_string.text,
								  self.target_string.text)

class Term(models.Model):
	string = models.ForeignKey('String', on_delete=models.CASCADE)
	text = models.ForeignKey('Text', on_delete=models.CASCADE)
	order = models.PositiveIntegerField()
	count = models.PositiveIntegerField()

	def __str__(self):
		return "#{0}: {1}({2})".format(self.order, self.string.text, self.count)

class Text(models.Model):
	title = models.CharField(max_length=127)
	author = models.CharField(max_length=127)
	language = models.ForeignKey('Language', on_delete=models.CASCADE)

	text = models.TextField()

	word_count = models.PositiveIntegerField(default=0, blank=True, null=True)
	vocabulary_count = models.PositiveIntegerField(default=0, blank=True,
												   null=True)
	head_word_count = models.PositiveIntegerField(default=0, blank=True,
												  null=True)

	def __str__(self):
		return "{0} by {1}".format(self.title, self.author)