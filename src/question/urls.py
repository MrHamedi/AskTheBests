from django.urls import path
from .views import HomePageView,comment_form,QuestionFormView, question_detail_view,liker_view,comment_liker_view


app_name="question"


urlpatterns = [
    path("", HomePageView,name="homepage"),
    path("question/<int:pk>/",question_detail_view,name="questionDetail"),
    path("question/<int:pk>/comment_form/",comment_form,name="comment_form"),
    path("question/<int:pk>/<str:order>/liker/",liker_view,name="liker_view"),
    path("comment/<int:pk>/<str:order>/liker/",comment_liker_view,name="comment_liker_view"),
    path("question/ask_question/",QuestionFormView.as_view(),name="question_form"),
]