from django.core.exceptions import ValidationError

from .test_base import MainAppTestBase


class MatchModelTest(MainAppTestBase):
    def setUp(self) -> None:
        self.match = self.make_match()
        return super().setUp()

    def test_match_level_raises_error_if_level_not_valid(self):
        self.match.level = "11"

        with self.assertRaises(ValidationError):
            self.match.full_clean()
