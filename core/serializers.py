from rest_framework import serializers

class TextSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    language = serializers.CharField(source='language.code')

class StringSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=32)
    language = serializers.CharField(source='language.code')
    phrase = serializers.BooleanField()