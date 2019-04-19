from xml import sax
import sys

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.db import connection
from django.core import serializers

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def restict(request):
    return HttpResponse("You're looking at a restricted page. Only a login user should be able to see this.")

def sql(request, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchall()
    return HttpResponse(str(row))

def xml(request):
    return render(request, 'polls/xml.html')

class ContentGenerator(sax.handler.ContentHandler):
    def __init__(self, out = sys.stdout):
        sax.handler.ContentHandler.__init__(self)
        self.out = out

    def startElement(self, name, attrs):
        self.out.write(name)
        for attr_name, value in attrs.items():
            self.out.write(attr_name + ": " + value)

    def characters(self, content):
        self.out.write(content)

def xml_upload(request):
    tmp = open('tmp', 'wt')
    xmlfile = request.FILES['xmlfile']
    parser = sax.make_parser()
    parser.setFeature(sax.handler.feature_external_ges, True)
    parser.setContentHandler(ContentGenerator(tmp))
    parser.parse(xmlfile)
    tmp.close()

    f = open('tmp', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

def xss(request):
    return render(request, 'polls/xss.html')

def xss_upload(request):
    return render(request, 'polls/xss.html', {'input': request.POST['string']})

def serial(request):
    # Serialize all questions and output on webpage.
    all_question = Question.objects.all()
    data = serializers.serialize("xml", all_question)
    data = data.replace('\n', '')
    f = open('serial.xml', 'w')
    f.write(data)
    f.close()
    return render(request, 'polls/serial.html')

def serial_download(request):
    with open('serial.xml', 'rb') as f:
        response = HttpResponse(f.read())
        response['content_type'] = 'application/xml'
        response['Content-Disposition'] = 'attachment;filename=serial.xml'
        return response

def serial_upload(request):
    data = request.POST['input']
    # Do no checking of data.
    # Do stuff with the unverfied data.
    return render(request, 'polls/serial.html', {'result': "Serialized object is accepted."})
