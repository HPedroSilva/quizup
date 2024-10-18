from django.core.exceptions import ValidationError
from django.test import tag

from .test_base import MainAppTestBase


class MatchModelTest(MainAppTestBase):
    def setUp(self) -> None:
        self.match = self.make_match()
        return super().setUp()

    def test_match_level_raises_error_if_level_not_valid(self):
        self.match.level = "11"

        with self.assertRaises(ValidationError):
            self.match.full_clean()

    def test_match_get_play_url_returns_correct_url(self):
        self.assertEqual(
            self.match.get_play_url(),
            f'/answer-question/?match={self.match.pk}',
        )

    def test_get_user_score_returns_correct_score_when_none_answered(self):
        user = self.match.users.first()
        self.assertEqual(self.match.get_user_score(user), 0)

    def test_get_user_score_returns_correct_score(self):
        user = self.match.users.first()
        questions = self.match.questions.all()[:3]
        answers = [True, False, True]

        for question, answer in zip(questions, answers):
            self.make_user_answer(
                user=user,
                match=self.match,
                correct=answer,
                question=question,
            )

        self.assertEqual(self.match.get_user_score(user), 2)

    def test_get_user_questions_answered_returns_correct_number_when_none_answered(
        self,
    ):
        user = self.match.users.first()
        self.assertEqual(self.match.get_user_questions_answered(user), 0)

    def test_get_user_questions_answered_returns_correct_number(self):
        user = self.match.users.first()
        questions = self.match.questions.all()[:3]
        answers = [True, False, True]

        for question, answer in zip(questions, answers):
            self.make_user_answer(
                user=user,
                match=self.match,
                correct=answer,
                question=question,
            )

        self.assertEqual(self.match.get_user_questions_answered(user), 3)

    def test_user_questions_to_answer_returns_correct_questions_when_none_answered(
        self,
    ):
        '''
        When none of the questions in a match have been answered, user_questions_to_answer must returnall questions in
        the match
        '''
        user = self.match.users.first()
        questions = self.match.questions.all().order_by('pk')[:3]
        questions_to_answer = self.match.user_questions_to_answer(
            user
        ).order_by('pk')

        self.assertQuerySetEqual(questions_to_answer, questions)

    def test_user_questions_to_answer_returns_correct_questions_when_all_answered(
        self,
    ):
        '''
        When all the questions in a match have been answered, user_questions_to_answer must return zero questions
        '''
        user = self.match.users.first()
        questions = self.match.questions.all()[:3]

        for question in questions:
            self.make_user_answer(
                user=user,
                match=self.match,
                correct=False,
                question=question,
            )

        questions_to_answer = self.match.user_questions_to_answer(user)
        self.assertEqual(len(questions_to_answer), 0)

    @tag('todo')
    def test_is_ready_to_finish_is_correct(self):
        pass

    @tag('todo')
    def test_is_finished_is_correct(self):
        pass

    @tag('todo')
    def test_get_score_returns_correct_score(self):
        pass

    @tag('todo')
    def test_get_winner_is_correct(self):
        pass
