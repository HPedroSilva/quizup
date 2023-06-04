from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
from django.contrib.auth.models import User

LEVEL_CHOICES = (
        ("1", "Fácil"),
        ("2", "Médio"),
        ("3", "Difícil")
    )

class Category(models.Model):
    name = models.CharField("Nome da categoria", max_length=25)
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return str(self.name)

class Question(models.Model):
    text = models.CharField("Texto da pergunta", max_length=400)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoria da pergunta")
    level = models.CharField("Nível da pergunta", max_length=1, choices=LEVEL_CHOICES)
    active = models.BooleanField("Pergunta está ativa?", default=True) # Define se a questão está ou não ativa para ser utilizada
    
    @property
    def answer(self):
        return self.option_set.all().filter(answer = True).first()

    def __str__(self):
        return str(self.text)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Pergunta")
    text = models.CharField("Texto da opção de resposta", max_length=200)
    answer = models.BooleanField("Resposta correta?", default=False) # Define se a pergunta é a resposta da questão
    
    def __str__(self):
        return str(self.text)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField("Pontuação do usuário")

    def __str__(self):
        return str(self.user.first_name)

class Match(models.Model):
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name="users_match")
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_winner", null=True, blank=True)
    level = models.CharField("Nível das perguntas", max_length=1, choices=LEVEL_CHOICES)
    categories = models.ManyToManyField(Category)
    questions = models.ManyToManyField(Question, blank=True)

    class Meta:
        verbose_name_plural = "matches"
        
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    match_answer = models.ForeignKey(Match, on_delete=models.CASCADE)

    @property
    def judgment(self):
        # Returna True se a resposta da perguta estiver correta e False caso contrário
        return self.option == self.question.answer

@receiver(post_save, sender=Match)
def match_post_save(sender, instance, **kwargs):
    questions = Question.objects.filter(level=instance.level)
    questions_pks = list(questions.values_list('pk', flat=True))
    random_pks = random.choices(questions_pks, k=3)
    questions = questions.filter(pk__in=random_pks)
    instance.questions.set(questions)
    Match.objects.filter(pk=instance.pk).update()