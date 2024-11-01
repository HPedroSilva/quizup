from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from mainApp.models import (
    Category,
    Match,
    Option,
    Question,
    UserAnswer,
    UserProfile,
)


class MainAppTestBase(TestCase):
    def login(self, username='my_user', password='my_pass'):
        self.client.login(username=username, password=password)

    def make_user(
        self,
        username='my_user',
        password='my_pass',
        first_name='my_user_first_name',
        last_name='my_user_last_name',
        super_user=False,
    ):
        if super_user is True:
            user = User.objects.create_superuser(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

        UserProfile.objects.create(user=user)
        return user

    def make_logged_user(
        self, username='my_user', password='my_pass', super_user=False
    ):
        user = self.make_user(
            username=username, password=password, super_user=super_user
        )
        self.login(username, password)
        return user

    def make_category(self, name='category_name'):
        return Category.objects.create(name=name)

    def make_question(
        self,
        text='question_text',
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

    def make_match(
        self,
        start_date=None,
        level='1',
        users=None,
        category=None,
        questions_number=3,
    ):
        if start_date is None:
            start_date = timezone.now()

        if category is None:
            category = self.make_category()

        if users is None:
            users = [self.make_user()]

        questions = [
            self.make_question(category=category)
            for _ in range(questions_number)
        ]

        match = Match.objects.create(
            start_date=start_date,
            level=level,
        )

        match.users.add(*users)
        match.categories.add(category)
        match.questions.add(*questions)

        return match

    def make_option(self, question=None, text='Test Option', answer=False):
        if question is None:
            question = self.make_question()
        return Option.objects.create(
            question=question, text=text, answer=answer
        )

    def make_user_answer(
        self,
        user=None,
        match=None,
        question=None,
        option=None,
        correct=False,
        is_expired=False,
    ):
        if user is None:
            user = self.make_user()
        if match is None:
            match = self.make_match(users=[user])
        if question is None:
            question = match.questions.first()
        if option is None:
            option = self.make_option(question=question, answer=correct)

        return UserAnswer.objects.create(
            user=user,
            question=question,
            option=option,
            match_answer=match,
            is_expired=is_expired,
        )
