from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext


def home(request):
    
    data = []
    for i in range(16):
        tmp = []
        for j in range(16):
            tmp.append('')
        data.append(tmp)
        
    data[5][6] = '!!!'
    data[0][0] = '..'
    data[11][11] = 'plot1.png'
        
    return render_to_response('page_choixconcept.html', {'title':'Phase 2', 
    'data':data
    },
    context_instance=RequestContext(request))