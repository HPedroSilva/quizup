from django.utils import timezone

from .test_base import MainAppTestBase


class UserProfileModelTest(MainAppTestBase):
    def setUp(self) -> None:
        user = self.make_user(username='user_1')
        self.user_profile = user.userprofile
        return super().setUp()

    def test_string_representation_returns_user_first_name(self):
        self.assertEqual(
            str(self.user_profile), self.user_profile.user.first_name
        )

    def test_matches_returns_no_matches_when_no_matches_for_user(self):
        '''
        When a user doesn't have any matches,
        'matches' must return an empty queryset.
        '''
        user_1 = self.user_profile
        user_2 = self.make_user(username='user_2')
        self.make_match(users=[user_2])
        self.assertEqual(len(user_1.matches), 0)

    def test_matches_returns_all_matches_of_an_user(self):
        '''
        When a user have matches, 'matches' must return a queryset
        with all it's matches.
        '''
        user_1 = self.user_profile.user
        user_2 = self.make_user(username='user_2')
        self.make_match(users=[user_1])
        self.make_match(users=[user_1])
        self.make_match(users=[user_2])
        self.assertEqual(len(user_1.userprofile.matches), 2)

    def test_pending_matches_returns_correct_matches(self):
        user = self.user_profile.user
        match_1 = self.make_match(users=[user])
        match_2 = self.make_match(users=[user])
        match_3 = self.make_match(users=[user])
        for question in match_1.questions.all():
            self.make_user_answer(
                user=user, match=match_1, correct=False, question=question
            )

        self.assertEqual(
            set(self.user_profile.pending_matches), set([match_2, match_3])
        )

    def test_pending_matches_returns_queryset_empty_if_no_pending_matches(
        self,
    ):
        user = self.user_profile.user
        match_1 = self.make_match(users=[user])
        for question in match_1.questions.all():
            self.make_user_answer(
                user=user, match=match_1, correct=False, question=question
            )

        self.assertEqual(len(self.user_profile.pending_matches), 0)

    def test_finished_matches_returns_correct_matches(self):
        user = self.user_profile.user
        match_1 = self.make_match(users=[user])
        self.make_match(users=[user])
        for question in match_1.questions.all():
            self.make_user_answer(
                user=user, match=match_1, correct=False, question=question
            )

        self.assertEqual(
            set(self.user_profile.finished_matches), set([match_1])
        )

    def test_finished_matches_returns_empty_queryset_if_no_finished_matches(
        self,
    ):
        user = self.user_profile.user
        match_1 = self.make_match(users=[user])
        self.make_match(users=[user])
        for question in match_1.questions.all()[1:]:
            self.make_user_answer(
                user=user, match=match_1, correct=False, question=question
            )

        self.assertEqual(len(self.user_profile.finished_matches), 0)

    def test_min_position_matches_return_correct_matches(self):
        questions_number = 3
        questions_answers_order = [True, True, False]

        user_1 = self.user_profile.user
        user_2 = self.make_user(username='user_2')
        user_3 = self.make_user(username='user_3')

        match_1 = self.make_match(
            users=[user_1, user_2, user_3], questions_number=questions_number
        )
        match_2 = self.make_match(
            users=[user_1, user_2, user_3], questions_number=questions_number
        )

        # making user_1 stay in position 2 in match_1
        # user_2 answers all questions correctly in match_1
        for question in match_1.questions.all():
            self.make_user_answer(
                user=user_2, match=match_1, correct=True, question=question
            )

        # user_1 answers 2 questions correctly in match_1
        for question, correct in zip(
            match_1.questions.all(), questions_answers_order
        ):
            self.make_user_answer(
                user=user_1, match=match_1, correct=correct, question=question
            )

        match_1.winner = user_2
        match_1.end_date = timezone.now()
        match_1.full_clean()
        match_1.save()

        # making user_1 stay in position 1 in match_2
        # user_1 answers all questions correctly in match_2
        for question in match_2.questions.all():
            self.make_user_answer(
                user=user_1, match=match_2, correct=True, question=question
            )

        # user_2 answers 2 questions correctly in match_2
        for question, correct in zip(
            match_2.questions.all(), questions_answers_order
        ):
            self.make_user_answer(
                user=user_2, match=match_2, correct=correct, question=question
            )

        match_2.winner = user_1
        match_2.end_date = timezone.now()
        match_2.full_clean()
        match_2.save()

        # user_1 was in position 2 in match_1, and position 3 in match_2.
        # He was in at least postion 2 in 2 matches.
        min_matches = self.user_profile.min_position_matches(2)

        self.assertEqual(
            set(min_matches),
            set([match_1, match_2]),
        )
