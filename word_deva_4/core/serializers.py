from rest_framework import serializers

from .models import String, Translation

class TranslationNestedSerializer(serializers.ModelSerializer):
    target_string = serializers.CharField(source="target_string.text", max_length=100)
    relevance = serializers.IntegerField(default=0)

    class Meta:
        model = Translation
        fields = ("target_string", "relevance")

class TextSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    language = serializers.CharField(source='language.code')

class StringSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=32)
    language = serializers.CharField(source='language.code')
    phrase = serializers.BooleanField()

    translations = TranslationNestedSerializer(source="source_string", many=True, read_only=True)

    class Meta:
        model = String
        fields = ("text", "language", "phrase", "translations")
