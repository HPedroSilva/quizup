from django.contrib import admin

from mainApp.models import (
    Category,
    Match,
    Option,
    Question,
    UserAnswer,
    UserProfile,
)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass
