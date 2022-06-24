%include('header_init.tpl', heading='Manage your qualitative attributes')

<h2>List of current attributes:</h2>
<table class="table table-striped">
    <thead>
        <tr>
            <th style='width:50px;'>State</th>
			<th>Type</th>
            <th>Attribute name</th>
			<th>Unit</th>
            <th>Values</th>
            <th>Method</th>
			<th>Mode</th>
            <th>Edit</th>
            <th><button type="button" class="btn btn-danger del_simu"><img src='/static/img/delete.ico' style='width:16px;'/></button></th>
        </tr>
    </thead>
    <tbody id="table_attributes">
    </tbody>
</table>

<br />
<br />

<div id="add_attribute" style="width:50%;margin-left:25%;margin-bottom:50px;">
    <h2> Add a new qualitative attribute: </h2>

    <div class="form-group">
        <label for="att_name">Name :</label>
        <input type="text" class="form-control" id="att_name" placeholder="Name">
    </div>
	
	<h3> Please rank the values by order of preference: </h3>

    <div class="form-group">
        <label for="att_value_worst">Least preferred value:</label>
        <input type="text" class="form-control" id="att_value_worst" placeholder="Worst value">
    </div>
	
	<div class="form-group">
        <label for="att_value_med">Intermediary value(s):</label>
			<input type="button" class="btn btn-outline-dark" id="add_value_med" value="Add an item"/>   
			<input type="button" class="btn btn-outline-dark" id="del_value_med" value="Delete last item"/>
			<ol id="list_med_values_quali">
				<li class="col-auto"><input type="text" class="form-control col-auto" id="att_value_med_1" placeholder='Intermediary Value 1'/></li>
			</ol>
    </div>
	
    <div class="form-group">
        <label for="att_value_best">Most preferred value:</label>
        <input type="text" class="form-control" id="att_value_best" placeholder="Best value">
    </div>
		
    <button type="submit" class="btn btn-outline-dark" id="submit">Submit</button>

</div>

%include('header_end.tpl')
%include('js.tpl')




<script>

// Fonctions pour ajouter/supprimer des zones de texte pour les valeurs intermédiaires
var list_med_values = document.getElementById('list_med_values_quali'),
	lists = list_med_values.getElementsByTagName('li'),
	add_value_med = document.getElementById('add_value_med'),
	del_value_med = document.getElementById('del_value_med');

/// Defines what happens when clicking on the "Add an item" button
add_value_med.addEventListener('click', function() {
	var longueur = lists.length;
	var new_item = document.createElement('li');
	new_item.innerHTML = "<input type='text' class='form-control' id='att_value_med_"+ String(longueur+1) +"' placeholder='Intermediary Value " + String(longueur+1) +"'/>";
	lists[longueur-1].parentNode.appendChild(new_item);
});

/// Defines what happens when clicking on the "Delete last item" button
del_value_med.addEventListener('click', function() {
	var longueur = lists.length;
	if (longueur!=1){
		lists[longueur-1].parentNode.removeChild(lists[longueur-1]);
	} else {
		alert("Please put at least one medium value for the attribute "+$('#att_name').val());
	};
});


$(function() {
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));
	var edit_mode = false;
	var edited_attribute=0;

	if (!assess_session) {
		assess_session = {
			"attributes": [],
			"k_calculus": [{
				"method": "multiplicative",
				"active": "false",
				"k": [],
				"GK": null,
				"GU": null
			}, {
				"method": "multilinear",
				"active": "false",
				"k": [],
				"GK": null,
				"GU": null
			}],
			"settings": {
				"decimals_equations": 3,
				"decimals_dpl": 8,
				"proba_ce": 0.3,
				"proba_le": 0.3,
				"language": "english",
				"display": "trees"
			}
		};
		localStorage.setItem("assess_session", JSON.stringify(assess_session));
	}

	function isAttribute(name) {
		for (var i = 0; i < assess_session.attributes.length; i++) {
			if (assess_session.attributes[i].name == name) {
				return true;
			}
		}
		return false;
	}
	
	function isOneValueOfTheListEmpty(val_list){
		var list_len = val_list.length;
		for (var i=0; i<list_len; i++) {
			if(val_list[i] == ""){return true}
		};
		return false;
	};
	
	function areAllValuesDifferent(val_list, val_min, val_max){
		var list_len = val_list.length;
		for (var i=0; i<list_len; i++) {
			if (val_list[i] == val_min || val_list[i] == val_max){
				return false;
			};
			for (var j=0; j<list_len; j++) {
				if(val_list[i] == val_list[j] && i!=j){
					return false;
				}
			}
		};
		return true;
	};
	
	function isThereUnderscore(val_list, val_min, val_max){
		var list_len = val_list.length;
		for (var i=0; i<list_len; i++) {
			if (val_list[i].search("_")!=-1){
				return false;
			};
		};
		if (val_min.search("_")!=-1 || val_max.search("_")!=-1){
			return false;
		};
		return true;
	};
	
	

	function checked_button_clicked(element) {
		var checked = $(element).prop("checked");
		var i = $(element).val();

		//we modify the propriety
		var assess_session = JSON.parse(localStorage.getItem("assess_session"));
		assess_session.attributes[i].checked = checked;

		//we update the assess_session storage
		localStorage.setItem("assess_session", JSON.stringify(assess_session));
	}

	function sync_table() {
		$('#table_attributes').empty();
		if (assess_session) {
			for (var i = 0; i < assess_session.attributes.length; i++) {
				var attribute = assess_session.attributes[i];
				
				///
				var text_table = "<tr>";
				text_table += '<td><input type="checkbox" id="checkbox_' + i + '" value="' + i + '" name="' + attribute.name + '" '+(attribute.checked ? "checked" : "")+'></td>'+
							  '<td>' + attribute.type + '</td>' +
							  '<td>' + attribute.name + '</td>' +
							  '<td>' + attribute.unit + '</td>' +
							  '<td><table><tr><td>' + attribute.val_min + '</td></tr>';
							  
				for (var ii=0, len=attribute.val_med.length; ii<len; ii++){
					text_table += '<tr><td>' + attribute.val_med[ii] + '</td></tr>';
				};
					
				text_table += '<tr><td>' + attribute.val_max + '</td></tr></table>'+
							  '<td>' + attribute.method + '</td>' +
							  '<td>' + attribute.mode + '</td>';
							  
				text_table += '<td><button type="button" id="edit_' + i + '" class="btn btn-outline-dark btn-xs">Edit</button></td>'+
							  '<td><button type="button" class="btn btn-outline-dark" id="deleteK'+i+'" ><img src="/static/img/delete.ico" style="width:16px"/></button></td></tr>';

				$('#table_attributes').append(text_table);

				//we will define the action when we click on the check input
				$('#checkbox_' + i).click(function() {
					checked_button_clicked($(this))
				});

				(function(_i) {
					$('#deleteK' + _i).click(function() {
						if (confirm("You are about to delete the attribute "+assess_session.attributes[_i].name+".\nAre you sure ?") == false) {
							return
						};
						assess_session.attributes.splice(_i, 1);
						// backup local
						localStorage.setItem("assess_session", JSON.stringify(assess_session));
						//refresh the page
						window.location.reload();
					});
				})(i);

				(function(_i) {
					$('#edit_' + _i).click(function() {
						edit_mode=true;
						edited_attribute=_i;
						var attribute_edit = assess_session.attributes[_i];
						$('#add_attribute h2').text("Edit attribute "+attribute_edit.name);
						$('#att_name').val(attribute_edit.name);
						$('#att_value_worst').val(attribute_edit.val_min);
						$('#att_value_med_1').val(attribute_edit.val_med[0]);
						
						for (var ii=2, len=attribute_edit.val_med.length; ii<len+1; ii++) {
							var longueur = lists.length;
							var new_item = document.createElement('li');
							new_item.innerHTML = "<input type='text' class='form-control' id='att_value_med_"+ String(longueur+1) +"' placeholder='Value Med " + String(longueur+1) +"'/>";
							lists[longueur-1].parentNode.appendChild(new_item);
							
							$('#att_value_med_'+ii).val(attribute_edit.val_med[ii-1]);
						};
						
						$('#att_value_best').val(attribute_edit.val_max);
					});
				})(i);
			}

		}
	}
	sync_table();

	$('#submit_quali').click(function() {
		var name = $('#att_name_quali').val(),
			val_min = $('#att_value_min_quali').val(),
			nb_med_values = document.getElementById('list_med_values').getElementsByTagName('li').length,
			val_med = [],
			val_max = $('#att_value_best').val();
			
		for (var ii=1; ii<nb_med_values+1; ii++){
			val_med.push($('#att_value_med_'+ii).val());
		};

		var method = "PE";
		
		if (name=="" || val_min=="" || val_max=="") {
			alert('Please fill correctly all the fields');
		}
		else if (isAttribute(name) && (edit_mode == false)) {
			alert ("An attribute with the same name already exists");
		} else if (isOneValueOfTheListEmpty(val_med)) {
			alert("One of your medium values is empty");
		} else if (val_min==val_max) {
			alert("The least preferred and most preferred values are the same");
		} else if (areAllValuesDifferent(val_med, val_min, val_max)==false) {
			alert("At least one of the values is appearing more than once");
		} else if (isThereUnderscore(val_med, val_min, val_max)==false) {
			alert("Please don't write an underscore ( _ ) in your values.\nBut you can put spaces");
		}

		else {
			if (edit_mode==false) {
				assess_session.attributes.push({
					"type": "Qualitative",
					"name": name,
					'unit': '',
					'val_min': val_min,
					'val_med': val_med,
					'val_max': val_max,
					'method': method,
					'mode': 'Normal',
					'completed': 'False',
					'checked': true,
					'questionnaire': {
						'number': 0,
						'points': {},
						'utility': {}
					}
				});
			} else {
				if (confirm("Are you sure you want to edit this attribute? All assessements will be deleted") == true) {
					assess_session.attributes[edited_attribute]={
						"type": "Qualitative",
						"name": name,
						'unit': '',
						'val_min': val_min,
						'val_med': val_med,
						'val_max': val_max,
						'method': method,
						'mode': 'Normal',
						'completed': 'False',
						'checked': true,
						'questionnaire': {
							'number': 0,
							'points': {},
							'utility': {}
						}
					};
				}
				edit_mode=false;
				$('#add_attribute h2').text("Add a new attribute");
			}
			
			sync_table();
			localStorage.setItem("assess_session", JSON.stringify(assess_session));
			
			/// On vide les zones de texte
			$('#att_name').val("");
			$('#att_value_worst').val("");
			$('#att_value_med_1').val("");
			$('#att_value_best').val("");
			
			/// On ramène le nombre d'éléments intermédiaires à 1
			for (var ii=val_med.length; ii>1; ii--) {
				var longueur = document.getElementById('list_med_values').getElementsByTagName('li').length;
				lists[longueur-1].parentNode.removeChild(lists[longueur-1]);
			};
		}
	});
});

</script>

</body>

</html>
