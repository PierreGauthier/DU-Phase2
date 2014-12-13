from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext


def home(request):
    
    data = []
    x=1366
        
    # (x,y,id,fichier svg,scale (%), rotation (deg), popup info, color, "left|right|middle", "content")
    data.append((1,4,'car1','cartop.svg',0.20,60,'<h3>titre</h3><p>Salut</a>','#63cdff','left sidebar very wide ', 'test'))
    data.append((4,12,'car5','cartop.svg',0.20,170,'<h3>titre</h3><p>Salut</a>','#556233','right sidebar very wide ', 'test'))
    data.append((4,10,'cone1','cone.svg',0.5,0,'<h3>titre</h3><p>Salut</a>','#ff8d2a','modal ', 'test'))
    data.append((4,9,'cone2','cone.svg',0.5,0,'<h3>titre</h3><p>Salut</a>','#ff8d2a','modal ', 'test'))
    data.append((3,8,'cone3','cone.svg',0.5,0,'<h3>titre</h3><p>Salut</a>','#ff8d2a','modal ', 'test'))
    
    return render_to_response('page_choixconcept.html', {'title':'Phase 2', 
    'data1':data, 'bg1':'street1lowres.jpg',
    'x':x,'xdiv2':x/2
    },
    context_instance=RequestContext(request))