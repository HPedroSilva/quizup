from django.test import TestCase
from django.urls import reverse


class MainAppURLsTest(TestCase):
    def test_mainApp_home_url_is_correct(self):
        url = reverse('mainapp:home')
        self.assertEqual(url, '/')

    def test_mainApp_match_url_is_correct(self):
        url = reverse('mainapp:match', kwargs={'pk': 1})
        self.assertEqual(url, '/match/1/')

    def test_mainApp_answer_question_url_is_correct(self):
        url = reverse('mainapp:answer_question')
        self.assertEqual(url, '/answer-question/')

    def test_mainApp_create_match_url_is_correct(self):
        url = reverse('mainapp:create_match')
        self.assertEqual(url, '/create-match/')

    def test_mainApp_user_matches_url_is_correct(self):
        url = reverse('mainapp:user_matches')
        self.assertEqual(url, '/user-matches/')

    def test_mainApp_import_questions_url_is_correct(self):
        url = reverse('mainapp:import_questions')
        self.assertEqual(url, '/import-questions/')

    def test_mainApp_user_profile_url_is_correct(self):
        url = reverse('mainapp:user_profile', kwargs={'username': 'user-name'})
        self.assertEqual(url, '/profile/user-name')