from django.core.exceptions import ValidationError

from .test_base import MainAppTestBase


class QuestionModelTest(MainAppTestBase):
    def setUp(self) -> None:
        self.question = self.make_question()
        return super().setUp()

    def test_question_text_raises_error_if_it_has_more_than_400_characters(
        self,
    ):
        self.question.text = 'a' * 401

        with self.assertRaises(ValidationError):
            self.question.full_clean()

    def test_answer_method_returns_the_correct_answer(self):
        self.make_option(question=self.question)
        self.make_option(question=self.question)
        self.make_option(question=self.question)
        option_answer = self.make_option(
            question=self.question, text='Answer', answer=True
        )

        self.assertEqual(self.question.answer, option_answer)
