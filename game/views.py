from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from random import choice

WORDS = ['CACHORRO','GATO','COMPUTADOR','PYTHON','DESENVOLVIMENTO','DJANGO']
MAX_ERRORS = 6

def start_game(session):
    word = choice(WORDS)
    session['word'] = word
    session['correct'] = []
    session['wrong'] = []
    session['finished'] = False

def index(request):
    if 'word' not in request.session:
        start_game(request.session)
    return render(request, 'game/index.html')

def state(request):
    word = request.session.get('word', '')
    correct = request.session.get('correct', [])
    wrong = request.session.get('wrong', [])
    masked = ''.join([c if c in correct else '_' for c in word])
    return JsonResponse({
        'word': word,
        'masked': masked,
        'correct': correct,
        'wrong': wrong,
        'errors': len(wrong),
        'max_errors': MAX_ERRORS,
        'finished': request.session.get('finished', False)
    })

@csrf_exempt
def guess(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'msg':'Método inválido'})
    if request.session.get('finished', False):
        return JsonResponse({'ok': False, 'msg':'Jogo já finalizado'})

    import json
    data = json.loads(request.body)
    letter = (data.get('letter') or '').upper()
    if not letter.isalpha() or len(letter) != 1:
        return JsonResponse({'ok': False, 'msg':'Letra inválida'})

    word = request.session.get('word', '')
    correct = set(request.session.get('correct', []))
    wrong = set(request.session.get('wrong', []))

    if letter in correct or letter in wrong:
        return JsonResponse({'ok': False, 'msg':'Letra já tentada'})

    if letter in word:
        correct.add(letter)
        request.session['correct'] = list(correct)
    else:
        wrong.add(letter)
        request.session['wrong'] = list(wrong)

    if all(c in correct for c in word):
        request.session['finished'] = True
        return JsonResponse({'ok': True, 'win': True, 'masked': word, 'errors': len(wrong)})

    if len(wrong) >= MAX_ERRORS:
        request.session['finished'] = True
        return JsonResponse({'ok': True, 'lose': True, 'word': word, 'errors': len(wrong)})

    masked = ''.join([c if c in correct else '_' for c in word])
    return JsonResponse({'ok': True, 'masked': masked, 'errors': len(wrong)})

@csrf_exempt
def reset(request):
    start_game(request.session)
    return JsonResponse({'ok': True})
