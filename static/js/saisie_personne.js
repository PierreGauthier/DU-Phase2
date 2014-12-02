
function recupPersonneInfo() { 
  var nom = $('[name="nom"]').first().val();
	var prenom = $('[name="prenom"]').first().val();
	
	progress_bar  = '<div class="progress progress-striped active">';
  progress_bar += '<div class="progress-bar progress-bar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%">';
  progress_bar += '<span class="sr-only">45% Complete</span></div></div>';
	$('#azpersonne').html(progress_bar);
	
	$.get( "/saisie/info/personne/"+nom+"/"+prenom, function( data ) 
  	{
			if(data.indexOf("Aucune Personne ne correspond") == -1) {
				
				addTopersonneModal("La personne que vous etes en train d\'enter correspond-t-elle à l\'une de ces personnes ? Si oui, cliquer sur le lien correpondant : <br/><br/>" + data);
				
				alert  = '<div class="alert alert-info">';
				alert += 'Nous avons trouvé des personnes similaires sur Cesar.org.uk ';
				alert += '<button class="btn btn-info" onclick="lauchPersonneModal();">Voir</button>';
				alert += '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button></div>';				
				$('#azpersonne').html(alert);
			}
			else {
				$('#azpersonne').html(' ');
			}
		});    
}

function lauchPersonneModal() {
	tooglepersonneModal();
	$('#azpersonne').html('');
}

function parsePersonneInfo(id) {
  $.get( "/saisie/info/personne/"+id, function( data ) 
  {
      var values = data.split(';');                   
      setValue('titre_personne',values[1]);                                      
      setValue('prenom',values[2]);                                                        
      setValue('nom',values[4]);                                     
      setValue('date_de_naissance',values[5]);                                     
      setValue('date_de_deces',values[6]);                                               
      setValue('pseudonyme',values[7]);
      if(values[8] == 'male') setValue('genre','M');
      else if(values[8] == 'female') setValue('genre','F'); 
      if(values[9] == 'French') setValue('nationalite', 'fr');
      else if(values[9] == 'Italian') setValue('nationalite', 'it');
      else if(values[9] == 'Deutsch') setValue('nationalite', 'de');
      else if(values[9] == 'English') setValue('nationalite', 'en');
      else setValue('nationalite', '-');
      if (values[10] != 'undefined') setValue('plus_dinfo', values[10]);
      setValue('uri_cesar','http://cesar.org.uk/cesar2/people/people.php?fct=edit&person_UOID='+id);
  });
  tooglepersonneModal();
}