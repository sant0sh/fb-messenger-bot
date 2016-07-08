def get_events(request, response):
    ctx = request.get('context', {})
    ctx['event_list'] = ['event_1', 'event_2']
    return ctx


def get_problems(request, response):
    ctx = request.get('context', {})
    ctx['problem_list'] = ['problem_1', 'problem_2']
    return ctx


def recommend_event(request, response):
    ctx = request.get('context', {})
    ctx['recommended_event'] = ['event_1', 'event_2'] 
    return ctx


def recommend_problem(request, response):
    ctx = request.get('context', {})
    return ctx


def get_all_event_types(request, response):
    ctx = request.get('context', {})
    ctx['event_types'] = [
            'hiring'
            'college',
            'hiring',
            'nonhiring',
            'hackathon',
            ]
    return ctx

    ctx = request.get('context', {})

def get_all_problem_tracks(request, response):
    ctx = request.get('context', {})
    ctx['tracks'] = [
            'maths',
            'data strutures',
            'algorithms',
            'basic programming',
            ]
    return ctx


topics = {}
topics['maths'] = ['number theory', 'counting',]
topics['algorithms'] = ['greedy', 'sorting', 'searching', 'dp']


def get_all_topics(request):
    ctx = request.get('context', {})
    entities = request.get('entities', {})
    if len(entities) >0:
        return topics
    return topics


def say(session, ctx, message):
    return message


def get_welcome_message(request, response):
    welcome_messages = [
            'Hi',
            'Hello',
            'Hi there!',
            'Hola!',
            'Hi, I am HE bot',
            'Hi, what can I help you with today?',
            'Hello World!',
            'Hello User',
            'Hey There!',
            ]
    import random
    print request
    ctx = request.get('contex', {})
    ctx['welcome_message'] =welcome_messages[random.randint(0,len(welcome_messages)-1)]
    return ctx
