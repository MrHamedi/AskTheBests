from django.db.models.query import QuerySet
from django.shortcuts import render
from question.models import Question 
from rest_framework import generics 
from .serializers import QuestionSerializer
# Create your views here.


class QuestionsList(generics.ListAPIView):
    queryset=Question.objects.all()
    serializer_class=QuestionSerializer


class QuestionDetailView(generics.RetrieveAPIView):
    queryset=Question.objects.all()
    serializer_class=QuestionSerializer
