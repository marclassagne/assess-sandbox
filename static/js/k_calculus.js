////////////////////////////////////////////////////////////////////////////////////////////////////////
///			javascript Function for k_calculus
////////////////////////////////////////////////////////////////////////////////////////////////////////

/// Function to calculate the number of active attributes (minimum 2 attributes are needed)
function number_attributes_checked(){
	var assess_session = JSON.parse(localStorage.getItem("assess_session")),
		counter=0;
		
	for (var i=0; i < assess_session.attributes.length; i++){
		if(assess_session.attributes[i].checked){
			counter++;
		};
	};
	return counter;
};

/// Function that manages the influence of the "button_method" buttons (multiplicative/multilinear)
function update_method_button(type){
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));
	
	for(var i=0; i<assess_session.k_calculus.length; i++){
		if(assess_session.k_calculus[i].method==type){
			assess_session.k_calculus[i].active=true;
			
			// we also change the look of the button of the current page
			$("#button_"+assess_session.k_calculus[i].method).removeClass('btn-default');
			$("#button_"+assess_session.k_calculus[i].method).addClass('btn-primary');
		} else {
			assess_session.k_calculus[i].active=false;
			
			// we also change the look of the button of the current page
			$("#button_"+assess_session.k_calculus[i].method).removeClass('btn-primary');
			$("#button_"+assess_session.k_calculus[i].method).addClass('btn-default');

		}
	}
	//we update the assess_session storage
	localStorage.setItem("assess_session", JSON.stringify(assess_session));
}

///  Action from Update button
$(function() {
	$("#not_enough_attributes").hide();
	$('#utility_function').hide();
	$('#button_generate_list').show();
	$('#k_list').show();
	
	update_method_button("multiplicative"); //update the active methode for k_kalculus
	update_k_list(0);
	show_list();
	$("#K_computation").show();
	$('#table_attributes').html("");
	ki_calculated();
	
	var counter = number_attributes_checked();
	
	if (counter < 2) {
		$("#page-content").hide();
		$("#not_enough_attributes").show();
	};

	$("#update").click(function () {
		var assess_session = JSON.parse(localStorage.getItem("assess_session"));
		$('#k_list').hide;
		// we delete the general utility functions
		assess_session.k_calculus[0].GU=null;
		assess_session.k_calculus[1].GU=null;
		localStorage.setItem("assess_session", JSON.stringify(assess_session)); //we update the assess_session storage

		$('#table_attributes').html(""); // we erase the table

		create_multiplicative_k();
		create_multilinear_k();
		
		update_method_button("multiplicative"); // we show the multiplicative button ON first
		update_k_list(0);
		show_list();
		ki_calculated();
		window.location.reload();
		
	});

	
		
		var NAttri = number_attributes_checked(),
			assess_session = JSON.parse(localStorage.getItem("assess_session")),
			NK = assess_session.k_calculus[0].k.length;
			
		
			$("#update_box").show("slow");
			
		// 	  <span id="update_attributes_number"></span>
		//    <span id="update_attributes_plurial">attributes are activated</span> but 
		//    <span id="update_k_number"></span> 
		//    <span id="update_k_number_plurial">are</span> used for the computation of the K<sub>i</sub> [...]

			$("#message_box").append(NAttri);
			$("#update_attributes_plurial").html((NAttri>1 ? "attributes are activated" : "attribute is activated"));
			
		
	
});

/// Action from multiplicative/multilinear button
$(function() {
	///  ACTION FROM BUTTON MULTIPLICATIVE
	$("#button_multiplicative").click(function () {
		
		update_method_button("multiplicative"); //update the active methode for k_kalculus
		update_k_list(0);
		show_list();
		$("#K_computation").show();
		$('#table_attributes').html("");
		ki_calculated();
	});

	///  ACTION FROM BUTTON MULTILINEAR
	$("#button_multilinear").click(function () {
		//update the active methode for k_kalculus
		update_method_button("multilinear");
		update_k_list(1);
		show_list();
		$("#K_computation").hide();
		$('#table_attributes').html("");
		ki_calculated();
	});
});

/// Initializing a MULTIPLICATIVE environment
function create_multiplicative_k() {
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));
	
	//first we delete the array of k for multiplicative and the GK
	assess_session.k_calculus[0].k=[];
	assess_session.k_calculus[0].GK=null;
	
	var counter=1;
	//then we initialize the environment with only the checked attributes
	for (var i=0; i < assess_session.attributes.length; i++){
		if(assess_session.attributes[i].checked) {
			assess_session.k_calculus[0].k.push({
				"ID":counter, 
				"ID_attribute":i, 
				"attribute":assess_session.attributes[i].name, 
				"type":assess_session.attributes[i].type,
				"value":null
			});
			counter++;
		};
	};
	//we update the assess_session storage
	localStorage.setItem("assess_session", JSON.stringify(assess_session));
};

/// Initializing a MULTILINEAR environment
function generer_list_lvl_0(n){
	var maList=[];
	
	for(var l=1; l<=n; l++) {
		maList.push([l]);
	};
	return maList;
};

function generer_list_1(i,n){
	var maList=[];
	
	for(var l=i; l<=n; l++) {
		maList.push(l);
	};
	return maList;
};

function generer_list(list_inf, n, lvl){
	if(lvl>=n){
		return [];
	};

	var nouvelle_list = [];
	
	for(var i=0; i<list_inf.length; i++) {
		var list_1=generer_list_1(list_inf[i][list_inf[i].length-1]+1,n);
		
		for(var l=0; l<list_1.length; l++) {
			nouvelle_list.push(list_inf[i].concat(list_1[l]));
		};
	};
	return list_inf.concat(generer_list(nouvelle_list, n, lvl+1));
};

function create_multilinear_k() {
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));
	assess_session.k_calculus[1].k=[];
	assess_session.k_calculus[1].GK=null;

	var checkedAttributeList=[];
	for (var i=0; i < assess_session.attributes.length; i++){
		if(assess_session.attributes[i].checked)
			checkedAttributeList.push(i);
	};

	var maListeCombinaison=generer_list(generer_list_lvl_0(checkedAttributeList.length),checkedAttributeList.length, 0);

	for (var i=0; i < maListeCombinaison.length; i++){
		var id_attribute=[],
			attribute=[];
			
		for(var j=0; j<maListeCombinaison[i].length; j++) {
			id_attribute.push(checkedAttributeList[maListeCombinaison[i][j]-1]);
			attribute.push(assess_session.attributes[checkedAttributeList[maListeCombinaison[i][j]-1]].name);
		};
		assess_session.k_calculus[1].k.push({
			"ID":maListeCombinaison[i].join(), 
			"ID_attribute":id_attribute, 
			"attribute":attribute, 
			"value":null
		});
	};

	//we update the assess_session storage
	localStorage.setItem("assess_session", JSON.stringify(assess_session));
}


//// COMMON FUNCTION FOR THE 2 METHODS
function update_k_list(number){
	//we delete the entire table
	$('#table_k_attributes').html("");
	var assess_session = JSON.parse(localStorage.getItem("assess_session")),
		ma_list = assess_session.k_calculus[number].k;

	for(var i=0; i<ma_list.length; i++){
		var text = '<tr id="line'+i+'"><td>K<sub>' + String(ma_list[i].ID).replace(/,/g, '') + '</sub></td>';
		
		text += '<td> '+ JSON.stringify(ma_list[i].attribute).replace(/"/g, ' ').replace("[", '').replace("]", '').replace(/,/g, '|'); + '</td>';
		if(ma_list[i].value==null){
			if(number==1 && i==ma_list.length-1){ //In the multilinear case and the last k
				text += '<td id="k_value_' + i + '"><button type="button" class="btn btn-outline-dark btn-xs" id="k_answer_' + i + '">Calculate</button></td>';
			} else {
				text += '<td id="k_value_' + i + '"><button type="button" class="btn btn-outline-dark btn-xs" id="k_answer_' + i + '">Answer</button></td>';
			};
		} else {
			text += '<td>'+ ma_list[i].value +'</td>';
		};

		text+='<td><img id="delete_K'+i+'" src="/static/img/delete.ico" style="width:16px;"/></td></tr>';

		$('#table_k_attributes').append(text);

		if(ma_list[i].value==null){
			(function(_i){
				$('#k_answer_'+_i).click(function(){
					$('#k_answer_'+_i).hide();
					if(number==0) {//multiplicative
						k_multiplicative_answer(_i);
					} else if(number==1){ //multilinear
						if (_i == ma_list.length - 1) {
							k_multilinear_calculate_last_one(_i);
							
						} else {
							k_multilinear_answer(_i);
						};
					}
				});
			})(i);
		};

		(function(_i){
			$('#delete_K'+_i).click(function(){
				if(confirm("All dependencies beetween k will be removed!") == false){return};
				assess_session.k_calculus[number].k[_i].value=null;
				assess_session.k_calculus[number].GK=null;

				if(number==1){ //in the case we are in multilinear we need to erase dependencies
					var indices=String(assess_session.k_calculus[number].k[_i].ID).split(",");

					for (var l=0; l<assess_session.k_calculus[number].k.length; l++){
						var number_in_it=0;
						for(var m=0; m<indices.length; m++) {
							if (assess_session.k_calculus[number].k[l].ID.indexOf(indices[m]) != -1)
								number_in_it++;
						};
						if(number_in_it==indices.length){//if we have all indices containing into an other one, we delete the parent
							assess_session.k_calculus[number].k[l].value = null;
						}
					}
				}

				//we also erase data of global utility function
				assess_session.k_calculus[get_Active_Method()].GU=null;
				localStorage.setItem("assess_session", JSON.stringify(assess_session));

				// backup local
				localStorage.setItem("assess_session", JSON.stringify(assess_session));
				//refresh the list
				update_k_list(number);
			});
		})(i);
	};
	//then we show the message if the number of ki calculated is sufficient
	ki_calculated();
	if(number==1)
		update_active_button_multilinear();
};

function show_list(){
	$("#k_list").fadeIn(500);
};

function get_Active_Method(){
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));
	return ((assess_session.k_calculus[0].active) ? 0 : 1);
};

function update_active_button_multilinear(){
	var assess_session = JSON.parse(localStorage.getItem("assess_session")),
		ma_list=assess_session.k_calculus[1].k,
		last_entered=1;
		
	for(var i=0; i<ma_list.length; i++) {
		if(ma_list[i].value==null) {
			last_entered=ma_list[i]["ID_attribute"].length;
			break;
		}
	}
	
	for(var i=0; i<ma_list.length; i++) {
		$("#k_answer_"+i).prop('disabled', (ma_list[i]["ID_attribute"].length<=last_entered ? false : true));
	}
}

/// Function to test if an object (obj) appears in the list (list_to_test)
function isInList(obj, list_to_test) {
	if (list_to_test.indexOf(obj) != -1){
		return true;
	} else {
		return false;
	};
};

//// Définition de la fonction qui va calculer K en MULTILINEAIRE 
function k_multilinear_answer(i){
	var assess_session = JSON.parse(localStorage.getItem("assess_session")),
		method = 'PE',
		settings = assess_session.settings,
		mon_k = assess_session.k_calculus[1].k[i],
		ID_att = mon_k.ID_attribute,
		name = mon_k.attribute;
		
		
	// we delete the slect div
	$('#k_calculus_info').hide();
	
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		///////////////////////////////////////////////////////////////// PE METHOD ////////////////////////////////////////////////////////////////
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	if (method == 'PE') {
		(function(){
			var probability = 0.75, //random_proba(0.25, 0.75);
				min_interval = 0,
				max_interval = 1;

			// VARIABLES
			var gain_certain = gain_haut = gain_bas = "",
				len = assess_session.attributes.length; // nombre d'attributs total
			
			for (var l = 0; l < len; l++){
				if(!assess_session.attributes[l].checked){continue} //if not checked we don't put it
				
				var attrib = assess_session.attributes[l],
					attrib_favorite = (attrib.mode=="Normal"? attrib.val_max : attrib.val_min),
					attrib_other = (attrib.mode=="Normal"? attrib.val_min : attrib.val_max);
					
				if (isInList(l, ID_att)) { // Si l'attribut étudié fait partie de ceux que l'on calcule pour le cas MULTILINEAIRE 
					gain_certain += String(attrib.name).toUpperCase() + ' : ' + attrib_favorite + ' ' + attrib.unit + (l==len-1?'':'<br/>');
				} else {
					gain_certain += String(attrib.name).toLowerCase() + ' : ' + attrib_other + ' ' + attrib.unit + (l==len-1?'':'<br/>');
				};
				
				gain_haut += String(attrib.name).toUpperCase() + ' : ' + attrib_favorite + ' ' + attrib.unit + (l==len-1?'':'<br/>');
				gain_bas += String(attrib.name).toLowerCase() + ' : ' + attrib_other + ' ' + attrib.unit + (l==len-1?'':'<br/>');
			};


			// INTERFACE
			//on cache le bouton
			$("#k_value_"+i).hide();
			$("#k_value_"+i).append("<br/><br/>");
			var arbre_gauche = new Arbre('pe', "#k_value_"+i, settings.display, "PE");

			// SETUP ARBRE GAUCHE
			arbre_gauche.questions_proba_haut = probability;
			arbre_gauche.questions_val_max = gain_haut;
			arbre_gauche.questions_val_min = gain_bas;
			//arbre_gauche.questions_val_max = gain_haut;
			//arbre_gauche.questions_val_min = gain_bas;
			arbre_gauche.questions_val_mean = gain_certain;
			arbre_gauche.display();
			arbre_gauche.update();
			
			
			$("#k_value_"+i).append('<br/><br/><br/><br/><div class=choice style="text-align: center;"><p>Which option do you prefer?</p><button type="button" class="btn btn-outline-dark gain">Certain gain</button><button type="button" class="btn btn-outline-dark lottery">Lottery</button></div><br/><br/><div ></div>');
			//on affiche l'arbre avec un petit effet !

			$("#k_value_"+i).show("fast");

			function treat_answer(data){
				min_interval = data.interval[0];
				max_interval = data.interval[1];
				probability = parseFloat(data.proba).toFixed(2);

				if (max_interval - min_interval <= 0.05){
					arbre_gauche.questions_proba_haut = probability;
					arbre_gauche.update();
					ask_final_value(Math.round((max_interval + min_interval)*100/2)/100);
				} else {
					arbre_gauche.questions_proba_haut = probability;
					arbre_gauche.update();
				}
			}

			function ask_final_value(val){
				// we delete the choice div
				$('.choice').hide();
				$("#k_value_"+i).append(
					'<br/><br/><br/><br/><div id= "final_value" style="text-align: center;margin-top:90px;"><br /><br /><p>We are almost done. Please enter the value that makes you indifferent between the two situations above. Your previous choices indicate that it should be between ' + min_interval + ' and ' + max_interval + ' but you are not constrained to that range <br /> '+ min_interval +'\
					 <= <input type="text" class="form-control" id="final_proba" placeholder="Probability" value="'+val+'" style="width: 100px; display: inline-block"> <= '+ max_interval +'</p><button type="button" class="btn btn-outline-dark final_validation">Validate</button></div>'
				);

				// when the user validates
				$('.final_validation').click(function(){
					//here we are in multilinearity we must calculate K with dependencies
					var final_proba = parseFloat($('#final_proba').val());
					var indices=String(assess_session.k_calculus[1].k[i].ID).split(",");
					var KASoustraire=[];

					for(var l=0; l<assess_session.k_calculus[1].k.length; l++) {
						var nombreIndice=0;
						for (var m = 0; m < indices.length; m++) {
							if (assess_session.k_calculus[1].k[l].ID.indexOf(indices[m]) != -1 && assess_session.k_calculus[1].k[l].ID_attribute.length<indices.length){
								nombreIndice++;
							};
						}

						if(nombreIndice==assess_session.k_calculus[1].k[l].ID_attribute.length) {
							KASoustraire.push(assess_session.k_calculus[1].k[l])
						};
					}
					var final_k=final_proba;
					for(var m=0; m<KASoustraire.length; m++) {
						final_k-=KASoustraire[m].value;
					}
					final_k=Math.round(final_k*1000)/1000;

					assess_session.k_calculus[1].k[i].value=final_k; // We put the k value for the MULTILINEAR
					
					if (i <assess_session.k_calculus[0].k.length) { // Because it's the same question
						if (assess_session.k_calculus[0].k[i].value == null){ // (if you have not answered it yet)
							assess_session.k_calculus[0].k[i].value=final_k; // We put the k value for the MULTIPLICATIVE as well
						}
					};
					
					
					// backup local
					localStorage.setItem("assess_session", JSON.stringify(assess_session));
					// we reload the list
					$("#k_value_"+i).hide( "fast",function(){
						update_k_list(1);
						show_list();
					});

				});
			}

			// HANDLE USERS ACTIONS
			$('.gain').click(function() {
				$.post('ajax', '{"type":"question", "method": "PE", "proba": '+ String(probability) + ', "min_interval": '+ min_interval+ ', "max_interval": '+ max_interval+' ,"choice": "0", "mode": "normal"}', function(data) {
					treat_answer(data);
				});
			});

			$('.lottery').click(function() {
				$.post('ajax', '{"type":"question","method": "PE", "proba": '+ String(probability) + ', "min_interval": '+ min_interval+ ', "max_interval": '+ max_interval+' ,"choice": "1" , "mode": "normal"}', function(data) {
					treat_answer(data);
				});
			});
		})()
	}
}

function k_multilinear_calculate_last_one(i){
	var assess_session = JSON.parse(localStorage.getItem("assess_session")),
		indices=String(assess_session.k_calculus[1].k[i].ID).split(","),
		KASoustraire=[];

	for(var l=0; l<assess_session.k_calculus[1].k.length; l++) {
		var nombreIndice=0;
		for (var m = 0; m < indices.length; m++) {
			if (assess_session.k_calculus[1].k[l].ID.indexOf(indices[m]) != -1 && assess_session.k_calculus[1].k[l].ID_attribute.length<indices.length){
				nombreIndice++;
			};
		}

		if(nombreIndice==assess_session.k_calculus[1].k[l].ID_attribute.length) {
			KASoustraire.push(assess_session.k_calculus[1].k[l]);
		};
	}

	var final_k=1;
	for(var m=0; m<KASoustraire.length; m++){
		final_k-=KASoustraire[m].value;
	}
	final_k=Math.round(final_k*1000)/1000;

	assess_session.k_calculus[1].k[i].value=final_k;
	// backup local
	localStorage.setItem("assess_session", JSON.stringify(assess_session));
	// we reload the list
	$("#k_value_"+i).hide( "fast",function(){
		update_k_list(1);
		show_list();
		
	});
}

//// Définition de la fonction qui va calculer K en MULTIPLICATIF 
function k_multiplicative_answer(i) {
	 	var assess_session = JSON.parse(localStorage.getItem("assess_session")),
			method = 'PE',
			settings = assess_session.settings,
			mon_k = assess_session.k_calculus[0].k[i],
			type = mon_k.type,
			name = mon_k.attribute;
		
		for (var j = 0; j < assess_session.attributes.length; j++) {
			if (assess_session.attributes[j].name == name) {
				var mon_attribut = assess_session.attributes[j];
			}
		}
		var mode = mon_attribut.mode;

		// we delete the slect div
		$('#k_calculus_info').hide();


		function random_proba(proba1, proba2) {
			var coin = Math.round(Math.random());
			if (coin == 1) {
				return proba1;
			}
			else {
				return proba2;
			}
		}

		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		///////////////////////////////////////////////////////////////// PE METHOD ////////////////////////////////////////////////////////////////
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		if (method == 'PE') {
			(function(){

				var probability = 0.75, //random_proba(0.25, 0.75),
					min_interval = 0,
					max_interval = 1;

				// VARIABLES
				var gain_certain = gain_haut = gain_bas = '',
					len = assess_session.k_calculus[0].k.length; // nombre d'attributs avec lesquels on compute le K

				for (var l=0; l < len; l++) {
					var attrib = assess_session.attributes[assess_session.k_calculus[0].k[l].ID_attribute]
						attrib_favorite = (attrib.mode=="Normal"? attrib.val_max : attrib.val_min),
						attrib_other = (attrib.mode=="Normal"? attrib.val_min : attrib.val_max);
						
					if (attrib.name == name) {
						gain_certain += String(attrib.name).toUpperCase() + ' : ' + attrib_favorite + ' ' + attrib.unit + (l==len-1?'':'<br/>');
					} else {
						gain_certain += String(attrib.name).toLowerCase() + ' : ' + attrib_other + ' ' + attrib.unit + (l==len-1?'':'<br/>');
					};
					
					gain_haut += String(attrib.name).toUpperCase() + ' : ' + attrib_favorite + ' ' + attrib.unit + (l==len-1?'':'<br/>');
					gain_bas += String(attrib.name).toLowerCase() + ' : ' + attrib_other + ' ' + attrib.unit + (l==len-1?'':'<br/>');
						
				}

				// INTERFACE
				//on cache le bouton
				$("#k_value_"+i).hide();
				$("#k_value_"+i).append("<br/><br/>");
				var arbre_gauche = new Arbre('pe', "#k_value_"+i, settings.display, "PE");

				// SETUP ARBRE GAUCHE
				arbre_gauche.questions_proba_haut = probability;
				// if(mode=="normal")
				// {arbre_gauche.questions_val_max = gain_haut;
				// arbre_gauche.questions_val_min = gain_bas;}
				// else
					// arbre_gauche.questions_val_max = gain_bas;
					// arbre_gauche.questions_val_min = gain_haut;
				arbre_gauche.questions_val_max = gain_haut;
				arbre_gauche.questions_val_min = gain_bas;
				arbre_gauche.questions_val_mean = gain_certain;
				arbre_gauche.display();
				arbre_gauche.update();

				$("#k_value_"+i).append('<br/><br/><br/><br/><div class=choice style="text-align: center;"><p>Which option do you prefer?</p><button type="button" class="btn btn-outline-dark gain">Certain gain</button><button type="button" class="btn btn-outline-dark lottery">Lottery</button></div><br/><br/><div ></div>');
				//on affiche l'arbre avec un petit effet !

				$("#k_value_"+i).show("fast");

				function treat_answer(data){
					min_interval = data.interval[0];
					max_interval = data.interval[1];
					probability = parseFloat(data.proba).toFixed(2);

					if (max_interval - min_interval <= 0.05){
						arbre_gauche.questions_proba_haut = probability;
						arbre_gauche.update();
						ask_final_value(Math.round((max_interval + min_interval)*100/2)/100);
					}
					else {
						arbre_gauche.questions_proba_haut = probability;
						arbre_gauche.update();
					}
				}

				function ask_final_value(val){
					// we delete the choice div
					$('.choice').hide();
					$("#k_value_"+i).append(
						'<br/><br/><br/><br/><div id= "final_value" style="text-align: center;margin-top:90px;"><br /><br /><p>We are almost done. Please enter the value that makes you indifferent between the two situations above. Your previous choices indicate that it should be between ' + min_interval + ' and ' + max_interval + ' but you are not constrained to that range <br /> '+ min_interval +'\
						 <= <input type="text" class="form-control" id="final_proba" placeholder="Probability" value="'+val+'" style="width: 100px; display: inline-block"> <= '+ max_interval +'</p><button type="button" class="btn btn-outline-dark final_validation">Validate</button></div>'
					);

					// when the user validates
					$('.final_validation').click(function(){
						var final_proba = parseFloat($('#final_proba').val());

						if (final_proba <= 1 && final_proba >= 0) {

							// we save it
							assess_session.k_calculus[0].k[i].value = final_proba; // We put the k value for the MULTIPLICATIVE first
							
							if (assess_session.k_calculus[1].k[i].value == null){ // (if you have not answered it yet)
								assess_session.k_calculus[1].k[i].value = final_proba; // We put the k value for the MULTILINEAR as well
							}
							// backup local
							localStorage.setItem("assess_session", JSON.stringify(assess_session));
							// we reload the list
							$("#k_value_" + i).hide("fast", function () {
								update_k_list(0);
								show_list();
								
							});

						}
					});
				}

				// HANDLE USERS ACTIONS
				$('.gain').click(function() {
					$.post('ajax', '{"type":"question", "method": "PE", "proba": '+ String(probability) + ', "min_interval": '+ min_interval+ ', "max_interval": '+ max_interval+' ,"choice": "0", "mode": "'+"normal"+'"}', function(data) {
						treat_answer(data);
					});
				});

				$('.lottery').click(function() {
					$.post('ajax', '{"type":"question","method": "PE", "proba": '+ String(probability) + ', "min_interval": '+ min_interval+ ', "max_interval": '+ max_interval+' ,"choice": "1" , "mode": "'+"normal"+'"}', function(data) {
						treat_answer(data);
					});
				});
			})()
		}

}

//#######################################################################################
//#######################              CALCULATE K             ##########################
//#######################################################################################

function ki_calculated() {
	var kiNumber = $("#table_k_attributes tr").length,
		kiNumberCalculated = 0,
		assess_session = JSON.parse(localStorage.getItem("assess_session"))
		method = ((assess_session.k_calculus[0].active) ? 0 : 1),
		ma_list = assess_session.k_calculus[method].k;
		
	for (var i = 0; i < kiNumber; i++) {
		if (ma_list[i].value != null){ //if we have calculated this value!
			kiNumberCalculated++;
		};
	}

	if (kiNumber != kiNumberCalculated) { // If the user hasn't calculated all k_i values yet
		if (get_Active_Method() == 0) { //if we're working with multiplicative
			$("#calculatek_box_multiplicative").fadeIn("fast");
			$("#calculatek_box_multilinear").fadeOut("fast");
		}
		else{
			$("#calculatek_box_multilinear").fadeIn("fast");
			$("#calculatek_box_multiplicative").fadeOut("fast");
		}

		$("#GK").hide();
		//we delete the K we have in memory
		assess_session.k_calculus[get_Active_Method()].GK=null;
	}
	else {
		$("#calculatek_box_multiplicative").fadeOut("fast");
		$("#GK").show();
		if (assess_session.k_calculus[get_Active_Method()].GK != null) {
			$("#GK_value").html(assess_session.k_calculus[get_Active_Method()].GK);
			$("#button_calculate_k").hide();
			$("#calculatek_box_multilinear").fadeOut("fast");
		}
		else {
			if(get_Active_Method()==0)//in multiplicative method
			{
				$("#GK_value").html("");
				$("#button_calculate_k").fadeIn("fast");
				$("#calculatek_box_multilinear").fadeOut("fast");
			}
			else //but in multilineaire
			{
				$("#calculatek_box_multiplicative").fadeOut("fast");
				$("#GK").hide();
				$("#calculatek_box_multilinear").fadeIn("fast");
			}
		}
	}
	$("#button_generate_list").show();
	GK_calculated();
	
	

}

$(function(){
	$("#button_calculate_k").click(function() {
		if (get_Active_Method() == 0){
			
			
			K_Calculate_Multiplicative();
			

		}
	});
});

function K_Calculate_Multiplicative() {
	var kiNumber = $("#table_k_attributes tr").length;

	//k value
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));
	var ma_list = assess_session.k_calculus[get_Active_Method()].k;

	var mesK={};
	if(kiNumber==2)
	{
		mesK['k1']=ma_list[0].value;
		mesK['k2']=ma_list[1].value;
	}
	else if(kiNumber==3)
	{
		mesK['k1']=ma_list[0].value;
		mesK['k2']=ma_list[1].value;
		mesK['k3']=ma_list[2].value;
	}
	else if(kiNumber==4)
	{
		mesK['k1']=ma_list[0].value;
		mesK['k2']=ma_list[1].value;
		mesK['k3']=ma_list[2].value;
		mesK['k4']=ma_list[3].value;
	}
	else if(kiNumber==5)
	{
		mesK['k1']=ma_list[0].value;
		mesK['k2']=ma_list[1].value;
		mesK['k3']=ma_list[2].value;
		mesK['k4']=ma_list[3].value;
		mesK['k5']=ma_list[4].value;
	}
	else if(kiNumber==6)
	{
		mesK['k1']=ma_list[0].value;
		mesK['k2']=ma_list[1].value;
		mesK['k3']=ma_list[2].value;
		mesK['k4']=ma_list[3].value;
		mesK['k5']=ma_list[4].value;
		mesK['k6']=ma_list[5].value;
	}


	$.post('ajax', '{"type":"k_calculus", "number":'+kiNumber+', "k":'+JSON.stringify(mesK)+'}', function(data) {

		assess_session.k_calculus[get_Active_Method()].GK=data.k;
		localStorage.setItem("assess_session", JSON.stringify(assess_session));
		//we update the view
		ki_calculated();
	});
}









//#######################################################################################
//###########   Choose utility function corresponding to attribute     ##################
//#######################################################################################



$(function(){
	var k_utility_multiplicative=[];
	var k_utility_multilinear=[];
	list();
	
	
});
function list(){
var assess_session = JSON.parse(localStorage.getItem("assess_session"));

	 k_utility_multilinear=[];
	 k_utility_multiplicative=[];

	//list of K with corresponding attribute:

	var maList=assess_session.k_calculus[get_Active_Method()].k;
	
	for(var i=0; i<assess_session.k_calculus[0].k.length; i++) {
		k_utility_multiplicative.push(null);
		k_utility_multilinear.push(null);
	}

	
	
	for (var i=0; i < maList.length; i++){

		var monAttribut=assess_session.attributes[maList[i].ID_attribute];
			
		
		(function(_i) {
		
		
				
				var name = monAttribut.name;
				
				if (monAttribut.type == "Qualitative"){
					
					var val_min = monAttribut.val_min,
						val_max = monAttribut.val_max,
						val_med = monAttribut.val_med,
						list_names = [].concat(val_min, val_med, val_max),
						points = monAttribut.questionnaire.points,
						list_points = [];
					
					if (monAttribut.checked){
						points[val_min] = 0; 
						points[val_max] = 1; 
						for (var ii=0; ii<list_names.length; ii++) {
							list_points.push(points[list_names[ii]]);
						};
					
						for (var k = 0; k < list_points.length; k++){
				
				
				
													
							
				
							var nvxdico = { "type" :'quali', "a": list_points[k], "name" : name };
				
							update_utility(_i, nvxdico);
						};
					};
				};
			
			if (monAttribut.type == "Quantitative"){
			var json_2_send = {"type": "calc_util_multi", "points":[]},
				val_max=monAttribut.val_max,
				val_min=monAttribut.val_min,
				mode = monAttribut.mode,
				points_dict = monAttribut.questionnaire.points,
				points=[],
			    	choice= monAttribut.fonction,
				num=monAttribut.numero;
				
			for (key in points_dict) {
				points.push([parseFloat(key), parseFloat(points_dict[key])]);
			};
			
			if (points.length > 0 && monAttribut.checked) {
				points.push([val_min, (mode == "Normal" ? 0 : 1)]);
				points.push([val_max, (mode == "Normal" ? 1 : 0)]);
				
				
				if (val_min<0) {
					for (j in points) {
						points[j][0]-=val_min;
						
					};
				}
				
				json_2_send["points"] = points;
				
				$.post('ajax', JSON.stringify(json_2_send), function (data) {
					$.post('ajax', JSON.stringify({
						"type": "svgg",
						"data": data['data'][num],
						"min": val_min,
						"max": val_max,
						"liste_cord": data['data'][num]['coord'],
						"width": 3,
						"choice":choice
					}), function (data2) {
						
						
						
						for (var key in data['data'][num]) {
							
							
							if (key == 'exp') {
								if (choice == 'exponential') {
								
								data['data'][num][key]['type']='exp';
								data['data'][num][key]['name']= name ;
								update_utility(_i,data['data'][num][key]);

							}}
							else if (key == 'log'){
								if (choice == 'logarithmic') {
							
								data['data'][num][key]['type']='log';
								data['data'][num][key]['name']= name ;
								update_utility(_i,data['data'][num][key]);
								
							}}
							else if (key == 'pow'){
								if (choice == 'power') {
								
								data['data'][num][key]['type']='pow';
								data['data'][num][key]['name']= name ;
								update_utility(_i,data['data'][num][key]);
							}}
							else if (key == 'quad'){
								if (choice == 'quadratic') {
								
								data['data'][num][key]['type']='quad';
								data['data'][num][key]['name']= name ;
								update_utility(_i,data['data'][num][key]);
							}}
							else if (key == 'lin'){
								if (choice == 'linear') {
								
								data['data'][num][key]['type']='lin';
								data['data'][num][key]['name']= name ;
								update_utility(_i,data['data'][num][key]);
							}}
							else if (key == 'expo-power'){
								if (choice == 'exponential-power') {
								
								data['data'][num][key]['type']='expo-power';
								data['data'][num][key]['name']= name ;
								update_utility(_i,data['data'][num][key]);
							}}
						};
					});
				});
			
			 };
		};
		})(i);
	};
		
};	
		


function update_utility(i, data){
	
		k_utility_multiplicative[i]=data;
	
		k_utility_multilinear[i]=data;
	
}

function addTextForm(div, copie, excel, latex) {

	// if (settings.language=="french") {
	// 	excel=excel.replace(/\./gi,",");
	// }

	var copy_button_dpl = $('<button class="btn functions_text_form" id="btn_dpl" data-clipboard-text="' + copie + '" title="Click to copy me.">Copy to clipboard (DPL format)</button>');
	var copy_button_excel = $('<button class="btn functions_text_form" id= "btn_excel" data-clipboard-text="' + excel + '" title="Click to copy me.">Copy to clipboard (Excel format)</button>');
	var copy_button_latex = $('<button class="btn functions_text_form" id= "btn_latex" data-clipboard-text="' + latex + '" title="Click to copy me.">Copy to clipboard (LaTeX format)</button>');

	div.html('')
	div.append("<div><pre>"+copie+"</pre></div>"); // we write the formula. AT THIS POINT, THE TEXT IS UGLY, LET'S TRY TO WRITE IT BETTER
	
	div.append(copy_button_dpl);
	div.append("<br /><br /><br /><br />");
	//div.append("<div><pre>"+excel+"</pre></div>")
	div.append(copy_button_excel);
	div.append("<br /><br /><br /><br />");
	// div.append("<div><pre>"+latex+"</pre></div>")
	div.append(copy_button_latex);


	var client = new Clipboard("#btn_dpl");
	client.on("success", function(event) {
		copy_button_dpl.text("Done !");
		setTimeout(function() {
			copy_button_dpl.text("Copy to clipboard (DPL format)");
		}, 2000);
	});

	var client = new Clipboard("#btn_excel");
	client.on("success", function(event) {
		copy_button_excel.text("Done !");
		setTimeout(function() {
			copy_button_excel.text("Copy to clipboard (Excel format)");
		}, 2000);
	});

	var client = new Clipboard("#btn_latex");
	client.on("success", function(event) {
		copy_button_latex.text("Done !");
		setTimeout(function() {
			copy_button_latex.text("Copy to clipboard (LaTeX format)");
		}, 2000);
	});
}

$(function(){
	
	$("#button_calculate_utility").click(function() {
		
		
		
		$('#utility_function').empty().show();
		var assess_session = JSON.parse(localStorage.getItem("assess_session"));
		if(get_Active_Method()==0)//multiplicative
		{
			if(k_utility_multiplicative.length==0)
			{
				alert("You need to choose a utility function for all your attributes in the list above");
				return;
			}
			if(assess_session.k_calculus[get_Active_Method()].GK==null){
				alert("You need to calculate K first");
				return;
			}

			for(var i=0; i<k_utility_multiplicative.length; i++)
			{
				if(k_utility_multiplicative[i]==null)
				{
					alert("You must reset your relative attributes");
					return;
				}
			}

			//then we go here so we can send the ajax request
			var mesK=assess_session.k_calculus[get_Active_Method()].k.slice();
			mesK.push({value:assess_session.k_calculus[get_Active_Method()].GK});
			var requete={"type": "utility_calculus_multiplicative", "k":mesK, "utility":k_utility_multiplicative, "virgule": assess_session.settings.decimals_dpl};
			console.log(requete);

			$.post('ajax', JSON.stringify(requete), function (data) {
				console.log(data);

				addTextForm($('#utility_function'), data.U, data.Uexcel, data.Ulatex);
				//alert(JSON.stringify(data));
				assess_session.k_calculus[get_Active_Method()].GU=data;
				localStorage.setItem("assess_session", JSON.stringify(assess_session));
				$('html, body').animate({
					scrollTop: $("#utility_function").offset().top
				}, 1000);
			});

		}
		
		
		
		else { // multilinear
			if (k_utility_multilinear.length == 0) {
				alert("You need to choose a utility function for all your attributes in the list above");
				return;
			}


			for(var i=0; i<k_utility_multilinear.length; i++)
			{
				if(k_utility_multilinear[i]==null)
				{
					alert("You must reset your relative attributes");
					return;
				}
			}

			var requete={"type": "utility_calculus_multilinear", "k":assess_session.k_calculus[get_Active_Method()].k, "utility":k_utility_multilinear, "virgule": assess_session.settings.decimals_dpl};
			$.post('ajax', JSON.stringify(requete), function (data) {
				console.log(data);
				
				addTextForm($('#utility_function'), data.U, data.Uexcel, data.Ulatex);
				//alert(JSON.stringify(data));
				assess_session.k_calculus[get_Active_Method()].GU=data;
				localStorage.setItem("assess_session", JSON.stringify(assess_session));
				$('html, body').animate({
					scrollTop: $("#utility_function").offset().top
				}, 1000);
			});
		}
		

	});
	
	
});




function GK_calculated() {
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));
	if (assess_session.k_calculus[get_Active_Method()].GU != null) {
		var listk = assess_session.k_calculus[get_Active_Method()].k;



		if(get_Active_Method()==1)
			k_utility_multilinear=assess_session.k_calculus[1].GU.utilities;
		else if(get_Active_Method()==0)
			k_utility_multiplicative=assess_session.k_calculus[0].GU.utilities;

		$('#table_attributes').html("");


		//list of K with corresponding attribute:

		var maList=[];
		var type=get_Active_Method();
		if(type==0)
		{
			maList=listk;
		}
		else {
			for (var i = 0; i < listk.length; i++) {
				if (listk[i].ID_attribute.length == 1) //if we have a k with only 1 index
				{
					maList.push(listk[i]);
				}
			}
		}


		for (var i=0; i < maList.length; i++) {

			var monAttribut = assess_session.attributes[maList[i].ID_attribute];
			var text = '<tr><td>K' + maList[i].ID + '</td>';
			text += '<td>' + monAttribut.name + '</td>';
			text += '<td id="charts_' + i + '"></td>';
			text += '<td id="functions_' + i + '">'+assess_session.k_calculus[get_Active_Method()].GU.utilities[i].type+' (r2='+assess_session.k_calculus[get_Active_Method()].GU.utilities[i].r2+')</td>';
			text += '</tr>';

			$('#table_attributes').append(text);

		}


				//we show the value of the global utility function
		$("#utility_function").html('<div><pre>'+assess_session.k_calculus[get_Active_Method()].GU.U+'</pre></div>')
	}
	else
	{
		$("#utility_function").html('');
	}
}
