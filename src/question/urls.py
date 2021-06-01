from django.urls import path
from .views import HomePageView , QuestionDetailView,comment_form,QuestionFormView


app_name="question"


urlpatterns = [
    path("question/<int:pk>/",QuestionDetailView.as_view(),name="questionDetail"),
    path("", HomePageView.as_view(),name="homepage"),
    path("question/<int:pk>/comment_form/",comment_form,name="comment_form"),
    path("question/ask_question/",QuestionFormView.as_view(),name="question_form"),
]