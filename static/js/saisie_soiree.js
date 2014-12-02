

function addPersonne() {
	$('input[name=other_information]').attr('value', $('#soireeForm').serialize());
  $('#myTab a[href="#Personne"]').tab('show');	
}         

function addPiece() {
	$('input[name=other_information]').attr('value', $('#soireeForm').serialize());
  $('#myTab a[href="#Piece"]').tab('show');	
}

function updateRepresentationSelect(e) {
	$(e).html('');
	$('#formitemdivrepresentation tr').each(function(){
		var newoptText = "";
		var newoptValue = "";
    $(this).find('td').each(function(){
      $(this).find('div').each(function(){
				//alert($(this).children().prop('nodeName'));
				if ($(this).children().prop('nodeName') == "SELECT") 
					newoptText += $(this).find('option:selected').text();
				else {
					newoptText += $(this).children().val() + " - ";
					newoptValue = $(this).children().val();
				}
    	})
    })		
		var o = new Option(newoptText, newoptValue);
		$(o).html(newoptText);
		$(e).append(o);
	});
	$select.selectmenu("refresh", true);
}

function newSoireeVide() {
	document.location.href="/saisie/new/soireeVide/" + $("[name=date]").val();
}