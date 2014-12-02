#-*- coding: utf-8 -*-
 
import re
import requests
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse     
 
def searchPersonne(request, nom, prenom):          
	payload = {'fct': 'list', 'search': nom + ' ' + prenom}
	r = requests.get("http://www.cesar.org.uk/cesar2/search/index.php", params=payload 
	   ,proxies= 
	   {
	     "http": "http://cache.wifi.univ-nantes.fr:3128",
	     "https": "http://cache.wifi.univ-nantes.fr:3128",
	   }
	)
	page = r.text
#	page = getPage1()
	page = page[page.index("<H1>People</H1>"):page.index("function listPersonClicked")]
	if not '0 records matched your query' in page :   
		page = page[page.index("<TR"):page.index("</TABLE")]
		page = page.replace(u'<TR><TD ID=\'keywordColumn\'><A HREF=\'../people/people.php?fct=edit&person_UOID=',u'<TR style="cursor:pointer;" onclick="parsePersonneInfo(')
		pattern = '\'>....\w*</A>'
		pattern = re.compile(pattern, flags=re.IGNORECASE|re.DOTALL|re.UNICODE)
		page = pattern.sub(u")\"><td><span class='glyphicon glyphicon-user'></span>",page)
		return HttpResponse("<div style='overflow:auto; height:30em;'><table class='table table-striped'>" + page+ "</table></div>", content_type="text/plain")
	else:
		return HttpResponse('Aucune Personne ne correspond à ce nom sur cesar.org.uk', content_type="text/plain")
    
def getInfoPersonne(request, id):
	payload = {'fct': 'edit', 'person_UOID': id }
	r = requests.get("http://www.cesar.org.uk/cesar2/people/people.php", params=payload 
		,proxies= 
		{
		 "http": "http://cache.wifi.univ-nantes.fr:3128",
		 "https": "http://cache.wifi.univ-nantes.fr:3128",
		}
	)
	page = r.text
	# page = getPage2()

	page = page[page.index("<H1>People</H1>"):page.index("<H2>Notes</H2>")] 
	infos = ''

	for i in range(1,10):
		page = page[page.index('keyColumn')+1:]
		if i == 8 :
			infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-23]
		elif (i == 7) or (i == 6) : #si c'est une date
			infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-29]			
		else:
			infos = infos + ';' + page[page.index('valueColumn')+19:page.index('keyColumn')-29]
	
	page = page[page.index('keyColumn')+1:]		
	infos = infos + ';' + page[page.index('valueColumn')+19:page.index('</TR>')-5]

	return HttpResponse(infos, content_type="text/plain")    

def getPage1() :
  return '''
  Search</TITLE><LINK REL="stylesheet" TYPE="text/css" HREF="../inc/cesar.css">
  </HEAD>
  <BODY bgcolor="#FAF0E6" link="#000000" vlink="#000000" alink="#000000"><FORM name="topsearch" action="../search/index.php">
  <INPUT type="hidden" name="fct" value="list"><TABLE width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#FAF0E6"><TR><TD>
  <IMG SRC="../images/cesar.gif" width="400" height="100"></TD></TR><!--<TR>
  <TD width="100%" height="1" bgcolor="#CCCCCC"><IMG SRC="../images/2x2.gif" width="1" height="1"></TD></TR>--><TR>
  <TD width="100%" height="1" bgcolor="#E4E4E4">   <TABLE width="100%" bgcolor="#CCCCCC" border="0" cellspacing="0" cellpadding="1">
  <TR><TD>   <TABLE width="100%" bgcolor="#E4E4E4" border="0" cellspacing="0" cellpadding="0">   <TR><TD id="topRightMenu" width="100%">&nbsp;
  </TD><TD id="topRightMenu">Search</TD><TD id="topRightMenu">&nbsp;</TD><TD id="topRightMenu">
  <INPUT type="text" name="search" value="" size="15" maxlength="20"></TD><TD id="topRightMenu">&nbsp;</TD><TD id="topRightMenu">
  <A href="javascript:document.topsearch.submit();" id="topRightMenu">GO</A></TD><TD id="topRightMenu">&nbsp;|&nbsp;</TD>
  <TD id="topRightMenu"><A href="../index.php" id="topRightMenu">Home</A></TD><TD id="topRightMenu">&nbsp;|&nbsp;</TD>
  <TD id="topRightMenu"><A href="#" onClick="javascript:open_dialog(\'../help/anon_reg_priv.php\',\'help\',500,500)" id="topRightMenu">Help</A>
  </TD><TD id="topRightMenu">&nbsp;|&nbsp;</TD><TD id="topRightMenu"><A href="../login.php?lang=" id="topRightMenu">Login</A>
  </TD><TD id="topRightMenu">&nbsp;|&nbsp;</TD>   </TR>   </TABLE>   </TD></TR>   </TABLE></TD></TR><!--<TR>
  <TD width="100%" height="1" bgcolor="#CCCCCC"><IMG SRC="../images/2x2.gif" width="1" height="1"></TD></TR>--></TABLE>
  </FORM><TABLE width="100%" border="0" cellspacing="4" cellpadding="4" bgcolor="#FAF0E6"><TR><!-- LEFT MENU CELL START -->
  <TD width="0%" bgcolor="#FAF0E6" valign="top"><TABLE border="0" cellspacing="2" cellpadding="2" bgcolor="#FAF0E6"><TR>
  <TD valign="top" align="center"><IMG border="0" src="../images/menuHeaderGeneric.jpg" width="86" height="96"><BR></TD></TR><TR>
  <TD><TABLE width=\'100%\' bgcolor=\'#CCCCCC\' cellspacing=\'0\' cellpadding=\'1\' border=\'0\'><TR><TD>
  <TABLE width=\'100%\' bgcolor=\'#E4E4E4\' cellspacing=\'0\' cellpadding=\'4\' border=\'0\'><TR><TD>
  <A href=\'../people/index.php\'><B>People</B></A><BR><A href=\'../troupes/index.php\'><B>Troupes</B></A><BR>
  <A href=\'../places/index.php\'><B>Places</B></A><BR><A href=\'../titles/index.php\'><B>Titles</B></A><BR>
  <A href=\'../dates/index.php\'><B>Dates</B></A><BR><A href=\'../publications/index.php\'><B>Publications</B></A><BR>
  <A href=\'../publishers/index.php\'><B>Publishers</B></A><BR><A href=\'../libraries/index.php\'><B>Libraries</B></A><BR>
  <A href=\'../imgs/index.php\'><B>Images</B></A><BR></TD></TR></TABLE></TD></TR></TABLE></TD></TR><TR><TD>
  <TABLE width=\'100%\' bgcolor=\'#CCCCCC\' cellspacing=\'0\' cellpadding=\'1\' border=\'0\'><TR><TD>
  <TABLE width=\'100%\' bgcolor=\'#E4E4E4\' cellspacing=\'0\' cellpadding=\'4\' border=\'0\'><TR><TD><A href=\'../books/index.php\'>
  <B>Books</B></A><BR><A href=\'../conferences/index.php\'><B>Conferences</B></A><BR><A href=\'../press/index.php\'><B>Press</B></A><BR>
  <A href=\'../treatises/index.php\'><B>Treatises</B></A><BR><A href=\'../policereports/index.php\'><B>Police reports</B></A><BR>
  <A href=\'../help/references.php\'><B>References</B></A><BR></TD></TR></TABLE></TD></TR></TABLE></TD></TR><TR>
  <TD valign=\'middle\' align=\'left\'><P>profile : anon</P></TD></TR><TR><TD>&nbsp;</TD></TR></TABLE></TD>
  <!-- LEFT MENU CELL END --><!-- MAIN CELL START --><TD width=\'100%\' bgcolor=\'#FAF0E6\' valign="top"><H1></H1>
  <H1>Search : Testard Marie</H1><H1>People</H1><FORM name="the_form" action="../people/people.php" method="GET">
  <INPUT type="hidden" name="fct" value=""><INPUT type="hidden" name="person_UOID" value=""><INPUT type="hidden" name="letter" value="">
  <INPUT type="hidden" name="women_only" value=""><INPUT type="hidden" name="non_french" value="">
  <INPUT type="hidden" name="search" value="Testard Marie"><INPUT type="hidden" name="offset" value="">
  <INPUT type="hidden" name="listMaxRows" value="100"></FORM><!--Array(   
  [312485] => Array (            [0] => 1        ))--><P><I>1 records matched your query</I></P><P>
  <TABLE CELLPADDING=2 CELLSPACING=2 BORDER=0><TR><TD ID=\'keywordColumn\'><A HREF=\'../people/people.php?fct=edit&person_UOID=317922\'>
  Testard</A></TD><TD ID=\'summaryColumn\'>Mlle <B>Marie-Anne-Xavier  Mathieu2 </B> <B><I>dite Testard</I></B> (1746 - )  </TD></TR><TR><TD ID=\'keywordColumn\'><A HREF=\'../people/people.php?fct=edit&person_UOID=317922\'>
  Testard</A></TD><TD ID=\'summaryColumn\'>Mlle <B>Marie-Anne-Xavier  Mathieu </B> <B><I>dite Testard</I></B> (1746 - )  </TD></TR>
  </TABLE><SCRIPT language="JavaScript">function listPersonClicked(person_UOID){   var href="../people/people.php";   
  href += "?fct=edit";   href += "&person_UOID="+person_UOID;   document.location.href=href;}function peopleChangeOffset(offset)
  {   var href="../people/people.php";   href += "?fct=list";   href += "&letter=";   href += "&search=Testard Marie";   
  href += "&women_only=";   href += "&non_french=";   href += "&listMaxRows=100";   href += "&offset="+offset;   document.location.href=href;}
  </SCRIPT><H1>Troupes</H1> <FORM NAME="the_form" ACTION="troupes.php" METHOD="GET"><INPUT type="hidden" name="fct" value="">
  <INPUT type="hidden" name="company_UOID" value=""><INPUT type="hidden" name="letter" value="">
  <INPUT type="hidden" name="search" value="Testard Marie"><INPUT type="hidden" name="offset" value=""></FORM><!--Array(    [312485] => Array
  (            [1] => 1        )    [317377] => Array        (            [1] => 1        )    [102863] => Array        (         
  [1] => 1        )    [342163] =>  Array        (            [1] => 1        )    [200162] => Array        (            [0] => 1    
  ))--><P><I>0 records matched your query</I></P><P><TABLE CELLPADDING=2 CELLSPACING=2 BORDER=0></TABLE><SCRIPT language="JavaScript">
  function listCompanyClicked(company_UOID) {   var href="../troupes/troupes.php";   href += "?fct=edit";   
  href += "&company_UOID="+company_UOID;   document.location.href=href;}function changeOffset(offset){  
  var href="../troupes/troupes.php";   href += "?fct=list";   href += "&letter=";   href += "&search=Testard Marie";  
  href += "&listMaxRows=100";   href += "&offset="+offset;   document.location.href=href;}</SCRIPT><H1>Places</H1>
  <FORM NAME="the_form" ACTION="../places/places.php" METHOD="GET"><INPUT type="hidden" name="fct" value="">
  <INPUT type="hidden" name="location_UOID" value=""><INPUT type="hidden" name="letter" value="">
  <INPUT type="hidden" name="restriction" value=""><INPUT type="hidden" name="search" value="Testard Marie">
  <INPUT type="hidden" name="offset" value=""></FORM><!--Array(    [keywords] =>  Array        (            [1] => 1        )    
  [157578] => Array        (            [1] => 1        )    [317011] => Array        (            [1] => 1        )    [326259] => Array   
  (            [1] => 1        )    [103469] => Array        (            [1] => 1        )    [207722] => Array        (        
  [1] => 1        )    [142990] => Array        (            [1] => 1        )    [142993] => Array        (            [1] => 1        )  
  [200162] => Array        (            [0] => 1        ))--><P><I>0 records matched your query</I></P>
  <TABLE CELLPADDING=\'2\' CELLSPACING=\'2\' BORDER=\'0\'></TABLE><P><I>0 records matched your query</I></P>
  <SCRIPT language="JavaScript">function placesChangeOffset(offset){   var href="../places/places.php";   href += "?fct=list";  
  href += "&letter=";   href += "&search=Testard Marie";   href += "&restriction=";   href += "&offset="+offset;   
  document.location.href=href;}</SCRIPT><H1>Titles</H1> <FORM NAME="the_form" ACTION="../titles/titles.php" METHOD="GET">
  <INPUT type="hidden" name="fct" value=""><INPUT type="hidden" name="script_UOID" value=""><INPUT type="hidden" name="letter"
  value=""><INPUT type="hidden" name="search" value="Testard Marie"><INPUT type="hidden" name="offset" value=""></FORM><!--Array(  
  [312485] => Array        (            [1] => 1        )    [317377] => Array        (            [1] => 1        )    [102863] => Array   
  (            [1] => 1        )    [342163] => s Array        (            [1] => 1        )    [142990] => Array        (         
  [1] => 1        )    [142993] => Array        (            [1] => 1        )    [200162] => Array        (            [0] => 1    
  ))--><P><I>0 records matched your query</I></P><P><TABLE CELLPADDING=2 CELLSPACING=2 BORDER=0></TABLE><SCRIPT language="JavaScript">
  function listTitleClicked(script_UOID){   var href="../titles/titles.php";   href += "?fct=edit";   href += "&script_UOID="+script_UOID;   document.location.href=href;}function 
  titlesChangeOffset(offset){   var href="../titles/titles.php";   href += "?fct=list";   href += "&letter=";   href += "&search=Testard Marie";   href += "&offset="+offset;   document.location.href=href;}</SCRIPT><H1>Publishers</H1> <FORM NAME="the_form"
  ACTION="../publishers/publishers.php" METHOD="GET"><INPUT type="hidden" name="fct" value=""><INPUT type="hidden" name="publisher_UOID" value=""><INPUT type="hidden" name="letter" value="">
  <INPUT type="hidden" name="search" value="Testard Marie"><INPUT type="hidden" name="offset" value="">
  </FORM><!--Array(    [312485] => Array        (            [1] => 1        )    [317377] =>  Array        (            [1] => 1        )    [200162] => Array        (            [0] => 1        ))--><P><I>0 records matched your query</I></P><P><TABLE CELLPADDING=2 
  CELLSPACING=2 BORDER=0></TABLE><SCRIPT language="JavaScript">function listPublisherClicked(publisher_UOID){   var href="../publishers/publishers.php";   href += "?fct=edit";   href += "&publisher_UOID="+publisher_UOID; 
  document.location.href=href;}function publishersChangeOffset(offset){   var href="../publishers/publishers.php";   href += "?fct=list"; 
  href += "&letter=";   href += "&search=Testard Marie";   href += "&offset="+offset;   
  document.location.href=href;}</SCRIPT><H1>Books</H1><P><I>0 records matched your query</I></P></TD><!-- MAIN CELL END --></TR></TABLE><P><TABLE width="100%" height="0%" border="0" cellspacing="0" cellpadding="0" bgcolor="#FAF0E6"><TR>
  <TD width="100%" height="1" bgcolor="#CCCCCC" COLSPAN="2"><IMG src="../images/2x2.gif" width="1" height="1"></TD></TR><TR>   <TD width="0%" height="1">      &nbsp;   </TD>   <TD width="100%" height="1">
  <CENTER><A href="mailto:editors@cesar.org.uk">editors@cesar.org.uk</A></CENTER>   </TD></TR></TABLE></BODY></HTML><!-- page was generated in 2.1007931232452 seconds --><!-- INSERT INTO tsar_access(userid, page, HTTP_GET_VARS, HTTP_POST_VARS, duration, HTTP_USER_AGENT, REMOTE_ADDR)VALUES("","/cesar2/search/index.php?fct=list&search=Testard+Marie","a:2:{s:3:\"fct\";s:4:\"list\";s:6:\"search\";s:13:\"Testard Marie\";}"
  ,"a:0:{}","2.1007931232452","Python-urllib/2.7","109.211.148.101") -->"'''

def getPage2() :
  return '''

<H1>People</H1>

 
 
<TABLE WIDTH='100%' CELLPADDING=2 CELLSPACING=2 BORDER=0>
<TR><TD ID='objectSummary'>Mlle Marie-Anne-Xavier <B> Mathieu </B><I>dite Testard </I>(1746 - )</TD></TR>
</TABLE>
<P>
<TABLE WIDTH='100%' CELLPADDING='0' CELLSPACING='2' BORDER='0'>
<TR><TD ID='keyColumn'>&nbsp;Titre&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Mlle&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Prénom&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Marie-Anne-Xavier&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Particule&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Nom de famille&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Mathieu&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Date de naissance&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;1746&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Date de décès&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Pseudonyme&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Testard&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Sexe&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;female</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Nationalité&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;French&nbsp;</TD></TR>
<TR><TD ID='keyColumn'>&nbsp;Compétences&nbsp;</TD>
<TD ID='valueColumn'>&nbsp;Danseur(euse)</TD></TR>
</TABLE>

<P><HR><H2>Notes</H2><P>
<H3>Campardon</H3><UL>
L'Académie royale de musique au XVIIIe siècle, 1884, t. II, p. 304 : 
"danseuse, née à Rouen, vers 1746. Avant d'appartenir à l'Académie royale de musique, où elle figura pendant les années 1769 et 1770, elle avait été attachée aux corps de ballet de l'Opéra-Comique et de la Comédie-Française (…)" [AS]

</UL>
</P>

'''
