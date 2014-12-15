from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext


def home(request):
    
    data1 = []
    data2 = []
    data3 = []
    
    x=1366
        
    # (x,y,id,fichier svg,scale (%), rotation (deg), popup info, color, "left|right|middle", "content",perspective)
    
    data1.append((2,0,'1store1','store.svg',0.3,0,'<b>Commerces environnants</b>','#ff8d2a','modal ', '1store1.html'))
    data1.append((5,9,'1worker1','people_worker2.svg',0.065,0,'<b>Professionnels du chantier</b>','#ff8d2a','large modal ', '1worker1.html'))
    data1.append((5,10,'1indawo1','indawo3d.svg',0.15,0,'<b>La borne Indawo</b>','#ff8d2a','modal ', '1indawo1.html'))
    data1.append((3,12,'1people1','people_man2.svg',0.17,0,'<b>Passants et riverains</b>','#ff8d2a','modal ', '1man1.html'))

    data2.append((2,4,'2car1','cartop.svg',0.2,60,'Automobilistes','#ff8d2a','modal ', '2car1.html'))
    data2.append((8,7,'2appia1','appia3d.svg',0.05,0,'La borne Appia','#ff8d2a','modal ', '2appia1.html'))
    data2.append((6,6,'2worker1','people_worker2.svg',0.075,0,'Les ouvrier du chantier','#ff8d2a','modal ', '2worker1.html'))
    data2.append((2,9,'2man1','people_woman3.svg',0.05,0,'Les pietons, cycliste, ...','#ff8d2a','modal ', '2man1.html'))
    data2.append((6,5,'2dust1','dust.svg',0.1,0,'Les facteurs environnementaux','#ff8d2a','modal ', '2dust1.html'))
    
    data3.append((0,9,'3store1','store2.svg',0.3,0,'Commerces environnants','#ff8d2a','modal ', '3store1.html'))
    data3.append((5,2,'3conect1','conect3d.svg',0.08,0,'CoNect','#63cdff','modal', '3conect1.html'))
    data3.append((4,5,'3noise1','people_worker1.svg',0.1,0,'Les facteurs environnementaux','#556233','modal', '3noise1.html'))
    data3.append((3,7,'3worker1','people_worker2.svg',0.1,0,'Les entreprises de travaux publics','#556233','modal ', '3worker1.html'))
    data3.append((2,11,'3man1','people_woman2.svg',0.2,0,'Les passants','#ff8d2a','modal ', '3man1.html'))
    
    
    return render_to_response('page_choixconcept.html', {'title':'Phase 2', 
    'data1':data1, 'bg1':'street1.jpg',
    'data2':data2, 'bg2':'street2.jpg',
    'data3':data3, 'bg3':'street3.jpg',
    'x':x,'xdiv2':x/2
    },
    context_instance=RequestContext(request))