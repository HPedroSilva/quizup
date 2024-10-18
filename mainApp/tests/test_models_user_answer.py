from .test_base import MainAppTestBase


class UserAnswerModelTest(MainAppTestBase):
    def setUp(self) -> None:
        return super().setUp()

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
