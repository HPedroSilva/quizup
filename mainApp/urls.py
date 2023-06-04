from django.urls import path
from . import views

urlpatterns = [
    path("answer-question/", views.AnswerQuestionView.as_view(), name="answer_question"),
    path("create-match/", views.CreateMatchView.as_view(), name="create_match"),
]