from typing import Any, Dict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
import json
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from mainApp.models import Option, Question, Match, UserAnswer

class AnswerQuestionView(TemplateView):
    """
    View que gerencia perguntas e respostas do usuário.
    """
    template_name = "answerQuestion.html"
    question = Question.objects.none()
    match = Match.objects.none()
    
    def get(self, request, *args, **kwargs):
        match_pk = request.GET.get("match")
        match = get_object_or_404(Match, pk=match_pk)
        self.match = match
        self.question = match.questions.all().exclude(Q(Q(useranswer__user = request.user) and Q(useranswer__match_answer = self.match))).first()
        return super(AnswerQuestionView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Julgar a resposta do usuário para a questão que ele recebeu
        # Falta adicionar verificações nos dados, pois serão recebidos do lado do usuário
        data = json.loads(request.body)
        match_pk = data.get("match")
        match = get_object_or_404(Match, pk=match_pk)
        question_pk = data.get("question")
        question = get_object_or_404(Question, pk=question_pk)
        option_pk = data.get("option")
        option = get_object_or_404(Option, pk=option_pk)
        
        user_answer = UserAnswer(user=request.user, question=question, option=option, match_answer=match)
        user_answer.save()

        judgment = "right" if user_answer.judgment else "wrong"
        return HttpResponse(headers={"judgment": judgment}, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        context['match'] = self.match
        return context

class CreateMatchView(CreateView):
    model = Match
    fields = ["start_date", "users", "level", "categories"]
    template_name = "createMatchForm.html"
    success_url = reverse_lazy("admin:index")

class UserMatchesView(ListView):
    model = Match
    template_name = "userMatches.html"
    context_object_name = "userMatches"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        userMatches = self.get_queryset().filter(users=self.request.user)
        context["userMatches"] = userMatches
        return context