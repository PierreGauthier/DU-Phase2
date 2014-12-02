function recupPieceInfo() { 
  var titre = document.getElementsByName("titre")[0].value;
  //var prenom = document.getElementsByName("auteur")[0].value; 
  if (titre != "") { 
    $.get( "../saisie/info/piece/"+titre, function( data ) 
        {
					if(data.indexOf("Aucune Piece ne correspond") == -1) {
          	addTopieceModal("La piece que vous etes en train d\'enter correspond-t-elle à l\'une de ces pieces ? Si oui, cliquer sur le lien correpondant : <br/><br/>" + data.replace(/@/g,"'"));
						document.getElementById("azpiece").innerHTML="<div class='alert alert-info'>Nous avons trouvé des pieces similaires sur Theaville.org <button class='btn btn-info' onclick='lauchPieceModal();''>Voir</button></div>";
					}
        });
     }
}         

function lauchPieceModal() {
	tooglepieceModal();
	document.getElementById('azpiece').innerHTML='';
}

function parsePieceInfo(id,titre,auteurs,date_premiere) {                 
    setValue('titre',titre);  
		setValue('auteurs',auteurs);                                                            
    setValue('date_premiere',date_premiere);              
    setValue('uri_theaville','http://theaville.org/index.php?r=pieces/auteurs/details.php&amp;id='+id);
    tooglepieceModal();
}

function addPersonneFromPiece() {
	$('input[name=other_information]').attr('value', $('#pieceForm').serialize());
  $('#myTab a[href="#Personne"]').tab('show');	
} 

$(function() {
	var button = '<button class="btn" type="button" onclick="addPersonneFromPiece()" data-toggle="tooltip" data-placement="right" title="" data-original-title="La personne que vous rechercher n\'est pas listé ?" style="vertical-align:bottom	;">+ Personne</button>';
	$("[name=auteurs]").parent().append(button);
});