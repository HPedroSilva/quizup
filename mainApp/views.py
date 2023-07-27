from typing import Any, Dict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from mainApp.models import Option, Question, Match, UserAnswer
from django.contrib.auth.models import User

class AnswerQuestionView(LoginRequiredMixin, TemplateView):
    """
    View que gerencia perguntas e respostas do usuário.
    """
    template_name = "answerQuestion.html"
    question = Question.objects.none()
    match = Match.objects.none()
    
    def get(self, request, *args, **kwargs):
        match_pk = request.GET.get("match")
        match = get_object_or_404(Match, pk=match_pk)
        self.user = request.user

        if request.user in match.users.all():
            self.match = match
            answered_questions = match.questions.filter(useranswer__user = request.user, useranswer__match_answer = match)
            self.question = match.questions.exclude(pk__in = answered_questions).first()
            return super(AnswerQuestionView, self).get(request, *args, **kwargs)
        else:
            return HttpResponse("Você não está nessa partida")

    
    def post(self, request, *args, **kwargs):
        # Julgar a resposta do usuário para a questão que ele recebeu
        data = json.loads(request.body)
        match_pk = data.get("match")
        match = get_object_or_404(Match, pk=match_pk)
        question_pk = data.get("question")
        question = get_object_or_404(Question, pk=question_pk)
        option_pk = data.get("option")
        option = get_object_or_404(Option, pk=option_pk)
        
        if not UserAnswer.objects.filter(user=request.user, question=question, match_answer=match).exists() and request.user in match.users.all() and question in match.questions.all() and option in question.option_set.all(): # Verificações de segurança, para evitar fraudes (o usuário está na partida, a questão é da partida, a opção é da questão, essa questão não foi respondida por esse usuário na partida)
            user_answer = UserAnswer(user=request.user, question=question, option=option, match_answer=match)
            user_answer.save()

            judgment = "right" if user_answer.judgment else "wrong"
            return HttpResponse(headers={"judgment": judgment}, status=200)
        
        return HttpResponse(status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        context['match'] = self.match
        context['user_questions_answered'] = self.match.get_user_questions_answered(self.user)
        return context

class CreateMatchView(LoginRequiredMixin, CreateView):
    model = Match
    fields = ["users", "level", "categories"]
    template_name = "createMatchForm.html"
    success_url = reverse_lazy("mainapp:home")

class MatchView(LoginRequiredMixin, DetailView):
    model = Match
    template_name = "match.html"
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super(MatchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        self.object = self.get_object()
        userQuestionsToAnswer = self.object.user_questions_to_answer(self.request.user)
        context["userQuestionsToAnswer"] = userQuestionsToAnswer
        return context

class UserMatchesView(LoginRequiredMixin, ListView):
    model = Match
    template_name = "userMatches.html"
    context_object_name = "userMatches"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        userMatches = self.get_queryset().filter(users=self.request.user)
        context["userMatches"] = userMatches
        return context
    
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        allowed_filters = ['in_progress_matches', 'finished_matches', 'wins', 'podium_matches']
        user = self.request.user.userprofile
        self.userMatches = user.matches
        filter = str(request.GET.get('filter', ''))
        if filter and filter in allowed_filters:
            self.userMatches = getattr(user, filter, None)
        self.userMatches = self.userMatches.order_by("-start_date")[:6]
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["userMatches"] = self.userMatches
        return context
    
class UserProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "user_profile.html"