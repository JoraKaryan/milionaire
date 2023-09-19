from django.db.models import Case, Value, F, When, Q, CharField, Sum
from django.shortcuts import render
from .functions import random_question
from .models import Questions, Answer, CurrentGame


def ChooseQuestion(request):
    # Choose a random question id
    random_id = random_question()

    question = Questions.objects.get(pk=random_id)
    question_title = question.title
    answers = Answer.objects.filter(question_id=question).values('answer', 'ans')

    ans1 = answers[0]['answer']
    ans2 = answers[1]['answer']
    ans3 = answers[2]['answer']
    ans4 = answers[3]['answer']

    state = ''
    right_one = ''
    score = 0
    finished = ''
    CurrentGame.objects.create(question_id=random_id, score=question.score)

    current = CurrentGame.objects.all().order_by('-id')

    if len(current) > 0:
        previous = current[1].question_id
        correct_ans = Answer.objects.filter(question_id=previous, correct=True).values('ans', 'answer', 'question_id',
                                                                                       'correct')

    if request.method == 'POST':
        selected_button = request.POST.get('selected_button', None)
        first = CurrentGame.objects.first()
        score = CurrentGame.objects.exclude(id=first.id).aggregate(score=Sum('score'))['score']

        if selected_button == 'new_game':
            first_row = CurrentGame.objects.first()
            CurrentGame.objects.exclude(id=first_row.id).delete()
            score = 0
            state = ''
            right_one = ''
            # question_title = ''

        elif selected_button == correct_ans[0]['ans']:
            state = 'Right'
            right_one = ''
            score = CurrentGame.objects.exclude(Q(id=first.id) | Q(score=0)).aggregate(score=Sum('score'))['score']
        else:
            state = 'Wrong'
            right_one = correct_ans[0]['answer']
            zero = CurrentGame.objects.order_by('-id').first()
            CurrentGame.objects.filter(id=zero.id).update(score=0)
        if CurrentGame.objects.count() == 6:
            finished = f"THE END -- SCORES [{score}]"
            first_row = CurrentGame.objects.first()
            CurrentGame.objects.exclude(id=first_row.id).delete()

    context = {'ans1': ans1,
               'ans2': ans2,
               'ans3': ans3,
               'ans4': ans4,
               'question': question_title,
               'state': state,
               'right_one': right_one,
               'score': score,
               'finished': finished
               }
    return render(request, 'main.html', context)
