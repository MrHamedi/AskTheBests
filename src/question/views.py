from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render , reverse ,redirect
from .models import Question 
from django.views.generic import ListView,DetailView,CreateView 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm,QuestionForm
from django.urls import reverse
from .models import Comment
from django.contrib.auth.decorators import login_required


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


@login_required
def comment_form(request,pk):
    question=Question.objects.get(id=pk)
    if(request.method=="POST"):
        form=CommentForm(data=request.POST)
        if(form.is_valid()):
            new_comment=form.save(commit=False)
            new_comment.author=request.user 
            new_comment.question=question
            new_comment.score=0
            new_comment.save()

    else:
        form=CommentForm()
    return(redirect("question:questionDetail",question.id))


class QuestionFormView(LoginRequiredMixin,CreateView):
    model=Question
    form_class=QuestionForm
    template_name="question/question_form.html" 

    def form_valid(self, form):
        m_tags = form.cleaned_data['tags']
        obj = form.save(commit=False)
        obj.author= self.request.user
        obj.slug=obj.slug_maker()
        obj.save()        
        obj.tags.add(*m_tags)
        obj.save()
        return(redirect(obj.get_absolute_url()))

