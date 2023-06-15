from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import random
from django.utils import timezone

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
class Match(models.Model):
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name="users_match")
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_winner", null=True, blank=True)
    level = models.CharField("Nível das perguntas", max_length=1, choices=LEVEL_CHOICES)
    categories = models.ManyToManyField(Category)
    questions = models.ManyToManyField(Question, blank=True)

    class Meta:
        verbose_name_plural = "matches"
    
    def get_play_url(self):
        return f"{reverse_lazy('mainapp:answer_question')}?match={self.pk}"
    
    @property
    def n_questions(self):
        # Retorna a quantidade de questões da partida
        return self.questions.count()
    
    def get_user_score(self, user):
        # Retorna a quantidade de perguntas que o usuário acertou na partida
        return UserAnswer.objects.filter(match_answer=self, user=user, option__answer=True).distinct("question").count()
    
    def get_user_questions_answered(self, user):
        # Retorna a quantidade de perguntas que o usuário respondeu na partida
        return UserAnswer.objects.filter(match_answer=self, user=user).distinct("question").count()
    
    @property
    def is_ready_to_finish(self):
        # Verifica se a partida pode ser finalizada (todos os jogadores já responderam suas perguntas)
        for user in self.users.all():
            if self.get_user_questions_answered(user) < self.n_questions:
                return False
        return True
    
    @property
    def is_finished(self):
        return (self.end_date is not None) and (self.winner is not None)

    def get_score(self):
        # Retorna a pontuação de cada usuário na partida
        score = []
        for user in self.users.all():
            score.append((user, self.get_user_score(user)))
        score.sort(reverse=True, key=lambda e: e[1])
        return score
    
    def get_winner(self):
        # Retorna o vencedor da partida, e sua pontuação
        # Falta tratar o caso de acertarem a mesma quantidade (usar tempo?)
        return self.get_score()[0]

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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField("Pontuação do usuário")

    def __str__(self):
        return str(self.user.first_name)

@receiver(post_save, sender=Match)
def match_post_save(sender, instance, **kwargs):
    # Gera uma quantidade específica de questões aleatórias para uma partida, assim que a partida é criada.
    if instance.questions.count() == 0:
        questions = Question.objects.filter(level=instance.level)
        questions_pks = list(questions.values_list('pk', flat=True))
        random_pks = random.sample(questions_pks, k=3)
        questions = questions.filter(pk__in=random_pks)
        instance.questions.set(questions)
        Match.objects.filter(pk=instance.pk).update()

@receiver(post_save, sender=UserAnswer)
def user_answer_post_save(sender, instance, **kwargs):
    # Caso seja a última resposta salva na partida, salva os dados de finalização (hora e vencedor)
    match = instance.match_answer
    if match.is_ready_to_finish and not match.end_date and not match.winner:
        Match.objects.filter(pk=match.pk).update(end_date = timezone.now(), winner = match.get_winner()[0])