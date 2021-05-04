from django.shortcuts import render
from .models import Question 
# Create your views here.
from django.views.generic import ListView,DetailView 
from django.contrib.auth.mixins import LoginRequiredMixin


#The view of the homepage  
class HomePageView(ListView):
    model=Question
    template_name="question/homepage.html"
    context_object_name="questions"
    paginate_by=4


class QuestionDetailView(DetailView,):
    """
        This is the view of detail page of questions 
    """
    model=Question 
    template_name="question/questionDetail.html"
    context_object_name="question"
    
