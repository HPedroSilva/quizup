from django.urls import path
from . import views

app_name = "mainapp"

urlpatterns = [
    path("answer-question/", views.AnswerQuestionView.as_view(), name="answer_question"),
    path("create-match/", views.CreateMatchView.as_view(), name="create_match"),
    path("user-matches/", views.UserMatchesView.as_view(), name="user_matches"),
]