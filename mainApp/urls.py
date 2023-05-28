from django.urls import path
from . import views

urlpatterns = [
    path("answer-question/", views.AnswerQuestionView.as_view(), name="answer_question"),
]