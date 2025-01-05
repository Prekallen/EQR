from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ....'},
    {'id':2, 'title':'view', 'body':'View is ....'},
    {'id':3, 'title':'model', 'body':'Model is ....'}
]
nextId = len(topics)+1

def html_template(article_tag, id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
             <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value="{id}">
                    <input type="submit" value="delete">
                </form>   
            </li>
            <li><a href="/update/{id}">update</a></li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return HttpResponse(f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ol>
            {ol}
        </ol>
        {article_tag}
        <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}
        </ul>
    </body>
    </html>
    ''')

def index(request):
    article ='''
    <h2>Welcome!</h2>
    Hello, Django
    '''
    return HttpResponse(html_template(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic["id"]== int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(html_template(article, id))

@csrf_exempt
def create(request):
    global nextId
    if request.method == 'GET':
        articles = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(html_template(articles))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        new_topic =  {"id":nextId, "title":title, "body":body}
        topics.append(new_topic)
        url = '/read/'+str(nextId)
        nextId += 1
        return redirect(url)

@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selected_topic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value={selected_topic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selected_topic["body"]}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(html_template(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect('/read/'+str(id))


@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic["id"] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')

