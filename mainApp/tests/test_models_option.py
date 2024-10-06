from django.core.exceptions import ValidationError

from mainApp.models import Option

from .test_base import MainAppTestBase


class OptionModelTest(MainAppTestBase):
    def setUp(self) -> None:
        self.option = self.make_option()
        return super().setUp()

    def test_option_text_raises_error_if_it_has_more_than_200_characters(
        self,
    ):
        self.option.text = 'a' * 201

        with self.assertRaises(ValidationError):
            self.option.full_clean()

    def test_answer_field_is_false_by_default(self):
        question = self.make_question()
        option = Option(question=question, text='Test Option')

        self.assertFalse(option.answer)
