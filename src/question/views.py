from django.shortcuts import render
from .models import Question 
from django.views.generic import ListView,DetailView,FormView 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.urls import reverse
from .models import Comment


class HomePageView(ListView):
    """
        This is the view of the homepage
    """
    model=Question
    template_name="question/homepage.html"
    context_object_name="questions"
    paginate_by=4


class QuestionDetailView(DetailView):
    """
        This is the view of detail page of questions 
    """
    model=Question 
    template_name="question/questionDetail.html"
    context_object_name="question"

    def get_context_data(self,**kwargs):
        context=super(QuestionDetailView,self).get_context_data(**kwargs)
        context["comment_form"]=CommentForm
        return(context)


class CommnetFormView(FormView):

    model=Comment
    form_class=CommentForm

    def get_success_url(self):
        return reverse('question:questionDetail', kwargs={'id': self.comment.id})
