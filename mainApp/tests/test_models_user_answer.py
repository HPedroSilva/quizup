from .test_base import MainAppTestBase


class UserAnswerModelTest(MainAppTestBase):

    def test_is_expired_is_false_by_default(self):
        user_answer = self.make_user_answer()
        self.assertFalse(user_answer.is_expired)

    def test_judgment_is_false_when_answer_is_incorrect(self):
        match = self.make_match()
        user = match.users.first()
        question = match.questions.first()
        user_answer = self.make_user_answer(
            user=user, match=match, correct=False, question=question
        )

        self.assertFalse(user_answer.judgment)

    def test_judgment_is_true_when_answer_is_correct(self):
        match = self.make_match()
        user = match.users.first()
        question = match.questions.first()
        user_answer = self.make_user_answer(
            user=user, match=match, correct=True, question=question
        )

        self.assertTrue(user_answer.judgment)

    def test_is_done_is_true_when_answered_in_time(self):
        user_answer = self.make_user_answer(
            is_expired=False,
        )
        self.assertTrue(user_answer.is_done)

    def test_is_done_is_false_when_answered_out_of_time(self):
        user_answer = self.make_user_answer(
            is_expired=True,
        )
        self.assertFalse(user_answer.is_done)

    def test_is_done_is_false_when_not_answered_and_not_expired(self):
        user_answer = self.make_user_answer(
            is_expired=False,
        )
        user_answer.option = None
        user_answer.save()

        self.assertFalse(user_answer.is_done)

    def test_is_done_is_false_when_not_answered_and_expired(self):
        user_answer = self.make_user_answer(
            is_expired=True,
        )
        user_answer.option = None
        user_answer.save()

        self.assertFalse(user_answer.is_done)
