import os
import openai

from google.cloud import translate

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import TodoSerializer

from ..models import Todo


class TodoViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):

    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(author=self.request.user)

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            item = serializer.save(author=self.request.user)
            return Response({'id': item.id, 'title': item.title}, status=200)
        return Response(serializer.errors, status=400)

    def put(self, *args, **kwargs):
        try:
            instance = Todo.objects.get(id=self.request.data.get('id'))
        except:
            instance = None

        if instance:
            serializer = self.serializer_class(data=self.request.data, instance=instance)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Successfully updated'}, status=200)
            return Response(serializer.errors, status=400)
        return Response({'message': 'Instance not found'}, status=400)


class TranslateViewSet(ViewSet):

    permission_classes = (AllowAny,)

    def translate_sentences(self, *args, **kwargs):
        sentence = self.request.data.get('sentence')
        target_language = self.request.data.get('target', 'fil')

        openai.api_key = os.getenv("OPENAI_API_KEY")
        project_id = os.getenv("PROJECT_ID")

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Translate this sentence into 3 simpler sentences. {sentence}",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )
            simplified_texts = response.choices[0]['text'].lstrip().split('\n')

            client = translate.TranslationServiceClient()
            location = "global"
            parent = f"projects/{project_id}/locations/{location}"
            trans_response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": simplified_texts,
                    "mime_type": "text/plain",
                    "source_language_code": "en-US",
                    "target_language_code": target_language,
                }
            )
            translated = []
            for translation in trans_response.translations:
                translated.append(translation.translated_text)
            return Response({'simplified': simplified_texts, 'translated': translated}, status=200)
        except:
            return Response({'message': 'Invalid input'}, status=400)

