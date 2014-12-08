from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext


def home(request):
    
    data = []
    x=1366
        
    # (x,y,id,fichier svg,scale (%), rotation (deg), popup info, color, "left|right|middle", "content")
    data.append((3,4,'car','cartop.svg',0.20,70,'<h3>titre</h3><p>Salut</a>','#63cdff','left sidebar very wide ', 'test'))
    data.append((5,10,'cone','cone.svg',0.50,0,'<h3>plot</h3>','#ff8d2a','left sidebar very wide ', 'test'))
    data.append((5,9,'cone2','cone.svg',0.50,0,'<h3>plot</h3>','#ff8d2a','large modal', '<h1>test<h1>'))
    data.append((4,8,'cone3','cone.svg',0.50,0,'<h3>plot</h3>','#ff8d2a','right sidebar', 'test'))
        
    return render_to_response('page_choixconcept.html', {'title':'Phase 2', 
    'data1':data, 'bg1':'street1lowres.jpg',
    'x':x,'xdiv2':x/2
    },
    context_instance=RequestContext(request))