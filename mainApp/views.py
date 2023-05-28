from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from mainApp.models import Question

class AnswerQuestionView(TemplateView):
    """
    View que exibirá cada pergunta para o usuário responder.
    """
    template_name = "answerQuestion.html"
    question = get_object_or_404(Question, pk=1) # Substituir a pk pela função que vai idicar a questão
    
    def get(self, request, *args, **kwargs):
        return super(AnswerQuestionView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        return context