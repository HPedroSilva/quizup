from django.test import TestCase
from django.urls import resolve, reverse

from mainApp import views


class MainAppViewTest(TestCase):
    def test_home_view_function_is_correct(self):
        function = resolve(reverse('mainapp:home'))
        self.assertIs(function.func.view_class, views.HomeView)

    def test_match_view_function_is_correct(self):
        function = resolve(reverse('mainapp:match', kwargs={'pk': 1}))
        self.assertIs(function.func.view_class, views.MatchView)

    def test_answer_question_view_function_is_correct(self):
        function = resolve(reverse('mainapp:answer_question'))
        self.assertIs(function.func.view_class, views.AnswerQuestionView)

    def test_create_match_view_function_is_correct(self):
        function = resolve(reverse('mainapp:create_match'))
        self.assertIs(function.func.view_class, views.CreateMatchView)

    def test_user_matches_view_function_is_correct(self):
        function = resolve(reverse('mainapp:user_matches'))
        self.assertIs(function.func.view_class, views.UserMatchesView)

    def test_import_questions_view_function_is_correct(self):
        function = resolve(reverse('mainapp:import_questions'))
        self.assertIs(function.func.view_class, views.ImportQuestionsView)

    def test_user_profile_view_function_is_correct(self):
        function = resolve(reverse('mainapp:user_profile', kwargs={'username': 'user-name'}))
        self.assertIs(function.func.view_class, views.UserProfileView)