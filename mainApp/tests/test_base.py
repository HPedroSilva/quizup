from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from mainApp.models import Category, Match, Option, Question, UserProfile


class MainAppTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def login(self, username='my_user', password='my_pass'):
        self.client.login(username=username, password=password)

    def make_user(self, username='my_user', password='my_pass', super=False):
        if super is True:
            user = User.objects.create_superuser(
                username=username, password=password
            )
        else:
            user = User.objects.create_user(
                username=username, password=password
            )

        UserProfile.objects.create(user=user)
        return user

    def make_logged_user(
        self, username='my_user', password='my_pass', super=False
    ):
        user = self.make_user(username, password, super)
        self.login(username, password)
        return user

    def make_category(self, name='category_name'):
        return Category.objects.create(name=name)

    def make_question(
        self,
        text='question_1_text',
        category_data=None,
        category=None,
        level='1',
        active=True,
    ):
        if category_data is None:
            category_data = {}

        if category is None:
            category = self.make_category(**category_data)

        return Question.objects.create(
            text=text,
            category=category,
            level=level,
            active=active,
        )

    def make_match(self, start_date=None, level='1', user=None, category=None):
        if start_date is None:
            start_date = timezone.now()

        if category is None:
            category = self.make_category()

        if user is None:
            user = self.make_user()

        self.make_question(category=category)
        self.make_question(category=category)
        self.make_question(category=category)

        match = Match.objects.create(
            start_date=start_date,
            level=level,
        )
        match.users.add(user)
        match.categories.add(category)

        return match

    def make_option(self, question=None, text='Test Option', answer=False):
        if question is None:
            question = self.make_question()
        return Option.objects.create(
            question=question, text=text, answer=answer
        )
