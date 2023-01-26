# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .pagination import Limit200Pagination
from .serializers import TextSerializer, StringSerializer

from .models import Text, String

class TextViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Text.objects.all() # TODO: filter by languages
        serializer = TextSerializer(queryset, many=True)
        return Response(serializer.data)

class StringViewSet(viewsets.ModelViewSet):
    model = String
    queryset = String.objects.all()
    serializer_class = StringSerializer
    pagination_class = Limit200Pagination

    def list(self, request):
        queryset = String.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)