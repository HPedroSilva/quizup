from typing import Any, Dict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from mainApp.models import Option, Question, Match, UserAnswer
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from mainApp.forms import ImportQuestionsForm
from django.conf import settings
from django.utils import timezone
import os
import json

class AnswerQuestionView(LoginRequiredMixin, TemplateView):
    """
    View que gerencia perguntas e respostas do usuário.
    """
    template_name = "answerQuestion.html"
    question = Question.objects.none()
    match = Match.objects.none()
    question_start_time = None
    
    def get(self, request, *args, **kwargs):
        match_pk = request.GET.get("match")
        match = get_object_or_404(Match, pk=match_pk)
        self.user = request.user

        if request.user in match.users.all():
            user_answer = UserAnswer.objects.none()
            self.match = match
            answered_questions = match.questions.filter(useranswer__user = request.user, useranswer__match_answer = match)
            pre_answered_questions = match.questions.filter(useranswer__user = request.user, useranswer__match_answer = match, useranswer__end_date=None)
            not_answered_questions = match.questions.exclude(pk__in = answered_questions)
            for question in pre_answered_questions:
                user_answer = UserAnswer.objects.filter(user = request.user, match_answer = match, question = question).first()
                if user_answer:
                    duration = timezone.now() - user_answer.start_date
                    if duration.seconds < 20:
                        self.question = question
                        break
                    else:
                        user_answer.end_date = timezone.now()
                        user_answer.is_expired = True
                        user_answer.save()
            if not self.question:
                self.question = not_answered_questions.first()
                if self.question:
                    user_answer = UserAnswer(user=request.user, question=self.question, start_date=timezone.now(), match_answer=match)
                    user_answer.save()
            if user_answer:
                duration = timezone.now() - user_answer.start_date
                self.question_start_time = 20 - min(duration.seconds, 20)
            else:
                self.question_start_time = 20
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
        
        user_answer = UserAnswer.objects.filter(user = request.user, match_answer = match, question = question).first()
        if user_answer:
            duration = timezone.now() - user_answer.start_date
            if not user_answer.is_done and request.user in match.users.all() and question in match.questions.all() and option in question.option_set.all(): # Verificações de segurança, para evitar fraudes (o usuário está na partida, a questão é da partida, a opção é da questão, essa questão não foi respondida por esse usuário na partida)

                user_answer.end_date = timezone.now()

                if duration.seconds < 20:
                    user_answer.option=option
                    judgment = "right" if user_answer.judgment else "wrong"

                else:
                    user_answer.is_expired = True
                    judgment = "expired"

                user_answer.save()
                return HttpResponse(headers={"judgment": judgment}, status=200)
        
        return HttpResponse(status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        context['match'] = self.match
        context['user_questions_answered'] = self.match.get_user_questions_answered(self.user)
        context['question_start_time'] = self.question_start_time
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

class ImportQuestionsView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "import_questions.html"
    form_class = ImportQuestionsForm
    success_url = reverse_lazy("mainapp:user_matches")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form_file = form.cleaned_data['file']
        file_path = os.path.join(settings.CONTENT_ROOT, "file.json")
        levels = [level[0] for level in LEVEL_CHOICES]
        
        with open(file_path, "wb+") as destination:
            for chunk in form_file.chunks():
                destination.write(chunk)
        
        file = open(file_path, "r")
        file_data = file.read()
        questions = json.loads(file_data)

        for question_import in questions:
            question_text = question_import.get("text", "")
            question_category = question_import.get("category", "")
            question_level = question_import.get("level", "")
            options_import = question_import.get("options")

            if question_category:
                category = Category.objects.filter(name__icontains=question_category).first()
            
            if question_level and question_level in levels and question_text and category:
                question = Question(text=question_text, category=category, level=question_level)
                question.save()
                
                for option_import in options_import:
                    option_text = option_import.get("text", "")
                    option_answer = option_import.get("answer", "")
                    
                    if question and option_text and option_answer:
                        option = Option(question=question, text=option_text, answer=option_answer)
                        option.save()

        return super(ImportQuestionsView, self).form_valid(form)
    
class UserProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "user_profile.html"
