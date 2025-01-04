from django.shortcuts import render, HttpResponse
topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ....'},
    {'id':2, 'title':'view', 'body':'View is ....'},
    {'id':3, 'title':'model', 'body':'Model is ....'}
]

def html_template(article_tag):
    global topics
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
        <a href=""></a>
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
        print(type(topic['id']), type(id))
        if topic["id"]== int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(html_template(article))

def create(request):
    return HttpResponse('Create')



