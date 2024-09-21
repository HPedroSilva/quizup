from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from mainApp import views
from mainApp.models import UserProfile


class MainAppViewTest(TestCase):
    def test_home_view_function_is_correct(self):
        function = resolve(reverse('mainapp:home'))
        self.assertIs(function.func.view_class, views.HomeView)

    def test_home_view_returns_status_code_200(self):
        username = 'my_user'
        password = 'my_pass'
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('mainapp:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_loads_correct_template(self):
        username = 'my_user'
        password = 'my_pass'
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('mainapp:home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_template_shows_no_matchs_found_if_no_matchs(self):
        username = 'my_user'
        password = 'my_pass'
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('mainapp:home'))
        self.assertIn(
            'Nenhuma partida encontrada!', response.content.decode('utf-8')
        )

    def test_match_view_function_is_correct(self):
        function = resolve(reverse('mainapp:match', kwargs={'pk': 1}))
        self.assertIs(function.func.view_class, views.MatchView)

    def test_answer_question_view_function_is_correct(self):
        function = resolve(reverse('mainapp:answer_question'))
        self.assertIs(function.func.view_class, views.AnswerQuestionView)

    def test_answer_question_view_returns_404_if_match_not_found(self):
        username = 'my_user'
        password = 'my_pass'
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        self.client.login(username=username, password=password)
        response = self.client.get(
            reverse('mainapp:answer_question'), data={'match': 100}
        )
        self.assertEqual(response.status_code, 404)

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
        function = resolve(
            reverse('mainapp:user_profile', kwargs={'username': 'user-name'})
        )
        self.assertIs(function.func.view_class, views.UserProfileView)
