from django.test import TestCase
from Quiz.models import Tournement, Question, Score
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User

class TournementModelTest(TestCase):
  
    @classmethod
    def setUpTestData(cls):
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        Tournement.objects.create(
          name='testTournement',
          difficulty='Medium',
          category='General Knowledge',
          start_time=now,
          end_time=tomorrow
          )

    def test_name(self):
        tournement = Tournement.objects.get(id=1)
        self.assertEqual(tournement.name, 'testTournement')

    def test_category(self):
        tournement = Tournement.objects.get(id=1)
        self.assertEqual(tournement.category, 'General Knowledge')


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        t = Tournement.objects.create(
          name='testTournement',
          difficulty='Medium',
          category='General Knowledge',
          start_time=now,
          end_time=tomorrow
          )
        Question.objects.create(
          tournement_id=t,
          question_text='Question',
          correct_answer='correct',
          incorrect_one='inOne',
          incorrect_two='inTwo',
          incorrect_three='inThree'
        )

    def test_question_text(self):
          q = Question.objects.get(id=1)
          self.assertEqual(q.question_text, 'Question')

class ScoreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Bob", password="bobpassword")

        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        t = Tournement.objects.create(
          name='testTournement',
          difficulty='Medium',
          category='General Knowledge',
          start_time=now,
          end_time=tomorrow
          )

        Score.objects.create(
          player_id = user,
          tournement_id=t,
          score=10
        )
    def test_score(self):
        s = Score.objects.get(id=1)
        self.assertEqual(s.score, 10)
