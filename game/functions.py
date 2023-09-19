from random import randint
from django.db.models import Max, Min
from .models import Questions, CurrentGame


def random_question():
    excluded_ids = list(CurrentGame.objects.values_list('question_id', flat=True))

    min_id = Questions.objects.aggregate(Min('id'))['id__min']
    max_id = Questions.objects.aggregate(Max('id'))['id__max']

    while True:
        random_id = randint(min_id, max_id)
        if random_id not in excluded_ids:
            return random_id