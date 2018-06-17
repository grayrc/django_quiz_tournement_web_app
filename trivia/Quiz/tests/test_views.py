from django.test import TestCase
import Quiz.views as views
from Quiz.models import Tournement, Question
from datetime import datetime
from datetime import timedelta

class FunctionTesta(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        next_day = now + timedelta(days=2)
        t1 = Tournement.objects.create(
          name='testTournement',
          difficulty='Medium',
          category='General Knowledge',
          start_time=now,
          end_time=tomorrow
          )
        t1.save()
        t2 = Tournement.objects.create(
          name='testTournementTwo',
          difficulty='Medium',
          category='General Knowledge',
          start_time=tomorrow,
          end_time=next_day
          )
        t2.save()
        Question.objects.create(
          tournement_id=t1,
          question_text='Question',
          correct_answer='correct',
          incorrect_one='inOne',
          incorrect_two='inTwo',
          incorrect_three='inThree'
        )
        Question.objects.create(
          tournement_id=t1,
          question_text='Question2',
          correct_answer='correct',
          incorrect_one='inOne',
          incorrect_two='inTwo',
          incorrect_three='inThree'
        )
    
    def test_category_names(self):
        category_names = views.getCatagories()
        self.assertEqual(category_names[0], 'General Knowledge')

    def test_get_current(self):
        tournements = views.getCurrent()
        self.assertEqual(tournements[0].name, 'testTournement')

    def test_get_future(self):
        tournements = views.getFuture()
        self.assertEqual(tournements[0].name, 'testTournementTwo')

