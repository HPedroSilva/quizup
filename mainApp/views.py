from typing import Any, Dict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
import json
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from mainApp.models import Question, Match

class AnswerQuestionView(TemplateView):
    """
    View que gerencia perguntas e respostas do usuário.
    """
    template_name = "answerQuestion.html"
    question = get_object_or_404(Question, pk=1) # Substituir a pk pela função que vai idicar a questão
    
    def get(self, request, *args, **kwargs):
        # Definir a questão que o usuário deve responder
        return super(AnswerQuestionView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Julgar a resposta do usuário para a questão que ele recebeu
        data = json.loads(request.body)
        answer = data.get("answer")
        judgment = "right" if answer == self.question.answer.pk else "wrong"
        return HttpResponse(headers={"judgment": judgment}, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        return context

class CreateMatchView(CreateView):
    model = Match
    fields = ["start_date", "users", "level", "categories"]
    template_name = "create-match-form.html"
    success_url = reverse_lazy("admin:index")