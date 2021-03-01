%include('header_init.tpl', heading='Assess utility functions')
<h3 id="attribute_name"></h3>
<div id="select">
	<table class="table">
		<thead>
			<tr>
				<th>Attribute</th>
				<th>Type</th>
				<th>Method</th>
				<th>Utility function</th>
				<th>Assess another point</th>
				<th>Display utility function</th>
				<th>Reset assessements</th>
			</tr>
		</thead>
		<tbody id="table_attributes">
		</tbody>
	</table>
</div>
<div id="trees"></div>
<div id="charts">
	<h2>Select the utility function you want to use</h2>
</div>



<div id= "attribute_name"></div>
<div id ="nouveaubloc"></div>

<div id="choix_fonction">
	<table class="table">
		<thead>
			<tr>
				
				<th>Your choice</th>
				<th>Update your choice</th>
			</tr>
		</thead>
		<tbody id="tableau_fct">
			
					<tr>
						
						<td id="ton_choix"></td>
						<td><button type="button" class="btn btn-default comeback" id = "update">Update</button> </td>
					</tr>
						
		</tbody>
	</table>
</div>
<div id="main_graph" class="col-lg-5"></div>
<div id="functions" class="col-lg-7"></div>
%include('header_end.tpl')
%include('js.tpl')
<script>
	var tree_image = '{{ get_url("static", path="img/tree_choice.png") }}';
</script>
<!-- Tree object -->
<script src="{{ get_url('static', path='js/tree.js') }}"></script>
<script>
	$(function() {
		$('li.questions').addClass("active");
		$('#attribute_name').hide();
		$('#charts').hide();
		$('#main_graph').hide();
		$('#functions').hide();
		$('#nouveaubloc').hide();
		$('#choix_fonction').hide();
		$('#attribute_name').hide();
		
		
		
		var assess_session = JSON.parse(localStorage.getItem("assess_session")),
			settings = assess_session.settings;
		// We fill the table of the existing attributes and assessments
		for (var i = 0; i < assess_session.attributes.length; i++) {
			if (!assess_session.attributes[i].checked) //if this attribute is not activated
				continue; //we skip this attribute and go to the next one
			
			
			
			
			var attribute = assess_session.attributes[i],
				text_table = '<tr><td>' + attribute.name + '</td>'+
							 '<td>' + attribute.type + '</td>'+
							 '<td>' + attribute.method + '</td>'+
							 '<td id="graph_choisi'+i+'" ></td>';
							 
							 
		
		
			text_table += '<td><table style="width:100%"><tr><td>' + attribute.val_min + '</td><td> : </td><td>'+(attribute.mode=="Normal"?0:1)+'</td></tr>';
			
			if (attribute.method == "PE" || attribute.method == "LE"){
				for (var ii=0, len=attribute.val_med.length; ii<len; ii++){
					text_table += '<tr><td>' + attribute.val_med[ii] + '</td><td> : </td>';
					if(attribute.questionnaire.points[attribute.val_med[ii]]){
						text_table += '<td>' + attribute.questionnaire.points[attribute.val_med[ii]] + '</td>';
					} else {
						text_table += '<td><button type="button" class="btn btn-default btn-xs answer_quest_'+(attribute.type=="Qualitative"?"quali":"quanti")+'" id="q_' + attribute.name + '_' + attribute.val_med[ii] + '_' + ii + '">Assess</button>' + '</td></tr>';
					};
				};
			} else {
				for (var key in attribute.questionnaire.points){
					text_table += '<tr><td>' + key + '</td><td> : </td>'+
								  '<td>' + attribute.questionnaire.points[key] + '</td></tr>';
				};
				
				for (var ii=Object.keys(attribute.questionnaire.points).length; ii<3; ii++){
					text_table += '<tr><td>-</td><td> : </td>'+
								  '<td><button type="button" class="btn btn-default btn-xs answer_quest_'+(attribute.type=="Qualitative"?"quali":"quanti")+'" id="q_' + attribute.name + '_' + ii + '_' + ii + '">Assess</button>' + '</td></tr>';
				};
			}; 
			
			text_table += '<tr><td>' + attribute.val_max + '</td><td> : </td><td>'+(attribute.mode=="Normal"?1:0)+'</td></tr></table></td>';
			if (attribute.type=="Quantitative") {
				if ( attribute.questionnaire.number > 0) {
					if (attribute.val_med.length == attribute.questionnaire.number){
						text_table += '<td><button type="button" class="btn btn-default btn-xs calc_util_quanti" id="u_' + attribute.name + '">Utility function</button>';
						text_table += '<button type="button" class="btn btn-default btn-xs" id="excel_' + i + '">export to Excel</button></td>';
					}
					else {
						text_table += '<td><button type="button" class="btn btn-default btn-xs calc_util_quanti" id="u_' + attribute.name + '">Utility function</button>';
					};
				} else {
					text_table += '<td>No assessment yet ';
				};
			} else {
				if (attribute.questionnaire.number === attribute.val_med.length) {
					text_table += '<td>';
				} else {
					text_table += '<td>Please assess all the medium values ';
				};
			};
			
			
			text_table += '<td><button type="button" id="deleteK' + i + '" class="btn btn-default btn-xs">Reset</button></td>';
			$('#table_attributes').append(text_table);
			(function(_i) {
				$('#deleteK' + _i).click(function() {
					if (confirm("Are you sure you want to delete all the assessments for "+assess_session.attributes[_i].name+"?") == false) {
							return
					};
					assess_session.attributes[_i].numero=10000;
					assess_session.attributes[_i].fonction='';
					assess_session.attributes[_i].questionnaire = {
							'number': 0,
							'points': {},
							'utility': {}
					};
					// backup local
					localStorage.setItem("assess_session", JSON.stringify(assess_session));
					//refresh the page
					window.location.reload();
				});
			})(i);
			(function(_i) {
				$('#excel_' + _i).click(function() {
					var data_2_export = JSON.stringify({"attributes":[assess_session.attributes[_i]], "k_calculus":[]})
					$.post('ajax', '{"type":"export_xlsx", "data":'+ data_2_export+'}', function(data) {
						document.location = "export_download/"+data;
					});
				});
			})(i);
			
		};
		
		
		for (var i = 0; i < assess_session.attributes.length; i++) {
		
		(function(_i) {
			if (assess_session.attributes[_i].type == "Quantitative"){
				if (assess_session.attributes[_i].checked){
					var monAttribut = assess_session.attributes[_i]
					
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
				
					if (points.length == 5){
					if (val_min<0) {
						for (j in points) {
							points[j][0]-=val_min;
						
						};
					}
				
					json_2_send["points"] = points;
					
					if (choice != ''){
					$.post('ajax', JSON.stringify(json_2_send), function (data) {
						$.post('ajax', JSON.stringify({
								"type": "svgg",
								"data": data['data'][num],
								"min": val_min,
								"max": val_max,
								"liste_cord": data['data'][num]['coord'],
								"width": 2.5,
								"choice":choice
							}), function (data2) {
								$('#graph_choisi' + _i).append('<div>You chose ' +choice+ '</div>');
								$('#graph_choisi'+ _i).append(data2);
								
							
							
					
							});
						});
						};
					}; };
				};
			};
			})(i);
		};
	
		
		
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		///////////////////////////////////////////////////////////////// CLICK ON THE ANSWER BUTTON ////////////////////////////////////////////////////////////////
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		/// When you click on a QUANTITATIVE attribute for assessment
		$('.answer_quest_quanti').click(function() {
			// we store the name, value, and index of the attribute
			var question_id = $(this).attr('id').slice(2).split('_'),
				question_name = question_id[0],
				question_val = question_id[1],
				question_index = question_id[2];
				
			// we delete the slect div
			$('#select').hide();
			$('#attribute_name').show().html(question_name.toUpperCase());
			// which index is it ?
			var indice;
			for (var j = 0; j < assess_session.attributes.length; j++) {
				if (assess_session.attributes[j].name == question_name) {
					indice = j;
				}
			}
			var val_min = assess_session.attributes[indice].val_min,
				val_max = assess_session.attributes[indice].val_max,
				unit = assess_session.attributes[indice].unit,
				method = assess_session.attributes[indice].method,
				mode = assess_session.attributes[indice].mode;
			function random_proba(proba1, proba2) {
				var coin = Math.round(Math.random());
				if (coin == 1) {
					return proba1;
				} else {
					return proba2;
				}
			}
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			///////////////////////////////////////////////////////////////// PE METHOD ////////////////////////////////////////////////////////////////
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			if (method == 'PE') {
				(function() {
					// VARIABLES
					var probability = 0.75,
						min_interval = 0,
						max_interval = 1,
						gain_certain = parseFloat(question_val);
					// INTERFACE
					var arbre_pe = new Arbre('pe', '#trees', settings.display, "PE");
					
					// SETUP ARBRE GAUCHE
					arbre_pe.questions_proba_haut = probability;
					arbre_pe.questions_val_max = (mode=="Normal"? val_max : val_min) + ' ' + unit;
					arbre_pe.questions_val_min = (mode=="Normal"? val_min : val_max) + ' ' + unit;
					arbre_pe.questions_val_mean = gain_certain + ' ' + unit;
					
					arbre_pe.display();
					arbre_pe.update();
					$('#trees').append('</div><div class=choice style="text-align: center;"><p>Which option do you prefer?</p><button type="button" class="btn btn-default" id="gain">Certain gain</button><button type="button" class="btn btn-default" id="lottery">Lottery</button></div>');
					// FUNCTIONS
					function sync_values() {
						arbre_pe.questions_proba_haut = probability;
						arbre_pe.update();
					}
					function treat_answer(data) {
						min_interval = data.interval[0];
						max_interval = data.interval[1];
						probability = parseFloat(data.proba).toFixed(2);
						if (max_interval - min_interval <= 0.05) {
							sync_values();
							ask_final_value(Math.round((max_interval + min_interval) * 100 / 2) / 100);
						} else {
							sync_values();
						}
					}
					function ask_final_value(val) {
						// we delete the choice div
						$('.choice').hide();
						$('.container-fluid').append(
							'<div id= "final_value" style="text-align: center;"><br /><br /><p>We are almost done. Please enter the probability that makes you indifferent between the two situations above. Your previous choices indicate that it should be between ' + min_interval + ' and ' + max_interval + ' but you are not constrained to that range <br /> ' + min_interval +
							'\
						 <= <input type="text" class="form-control" id="final_proba" placeholder="Probability" value="' + val + '" style="width: 100px; display: inline-block"> <= ' + max_interval +
							'</p><button type="button" class="btn btn-default final_validation">Validate</button></div>'
						);
						// when the user validate
						$('.final_validation').click(function() {
							var final_proba = parseFloat($('#final_proba').val());
							if (final_proba <= 1 && final_proba >= 0) {
								// we save it
								assess_session.attributes[indice].questionnaire.points[String(gain_certain)]=final_proba;
								assess_session.attributes[indice].questionnaire.number += 1;
								// backup local
								localStorage.setItem("assess_session", JSON.stringify(assess_session));
								// we reload the page
								window.location.reload();
							}
						});
					}
					sync_values();
					// HANDLE USERS ACTIONS
					$('#gain').click(function() {
						$.post('ajax', '{"type":"question", "method": "PE", "proba": ' + String(probability) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "0", "mode": "' + 'normal' + '"}', function(data) {
							treat_answer(data);
							console.log(data);
						});
					});
					$('#lottery').click(function() {
						$.post('ajax', '{"type":"question","method": "PE", "proba": ' + String(probability) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "1" , "mode": "' + 'normal' + '"}', function(data) {
							treat_answer(data);
							console.log(data);
						});
					});
				})()
			}
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			///////////////////////////////////////////////////////////////// LE METHOD ////////////////////////////////////////////////////////////////
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			else if (method == 'LE') {
				(function() {
					// VARIABLES
					var probability = random_proba(0.38, 0.13);
					var min_interval = 0;
					var max_interval = 0.5;
					// INTERFACE
					var arbre_le = new Arbre('gauche', '#trees', settings.display, "LE_left");
					var arbre_droite = new Arbre('droite', '#trees', settings.display, "LE_right");
					// SETUP ARBRE GAUCHE
					arbre_le.questions_proba_haut = probability;
					arbre_le.questions_val_max = val_max + ' ' + unit;
					arbre_le.questions_val_min = val_min + ' ' + unit;
					arbre_le.display();
					arbre_le.update();
					// SETUP ARBRE DROIT
					arbre_droite.questions_proba_haut = settings.proba_le;
					// The certain gain will change whether it is the 1st, 2nd or 3rd questionnaire
					arbre_droite.questions_val_max = parseFloat(question_val) + ' ' + unit;
					arbre_droite.questions_val_min = val_min + ' ' + unit;
					arbre_droite.display();
					arbre_droite.update();
					// we add the choice button
					$('#trees').append('<div class=choice style="text-align: center;"><p>Which option do you prefer?</p><button type="button" class="btn btn-default lottery_a">Lottery A</button><button type="button" class="btn btn-default lottery_b">Lottery B</button></div>')
					function treat_answer(data) {
						min_interval = data.interval[0];
						max_interval = data.interval[1];
						probability = parseFloat(data.proba).toFixed(2);
						if (max_interval - min_interval <= 0.05) {
							arbre_le.questions_proba_haut = probability;
							arbre_le.update();
							ask_final_value(Math.round((max_interval + min_interval) * 100 / 2) / 100);
						} else {
							arbre_le.questions_proba_haut = probability;
							arbre_le.update();
						}
					}
					function ask_final_value(val) {
						$('.choice').hide();
						$('.container-fluid').append(
							'<div id= "final_value" style="text-align: center;"><br /><br /><p>We are almost done. Please enter the probability that makes you indifferent between the two situations above. Your previous choices indicate that it should be between ' + min_interval + ' and ' + max_interval + ' but you are not constrained to that range <br /> ' + min_interval +
							'\
						 <= <input type="text" class="form-control" id="final_proba" placeholder="Probability" value="' + val + '" style="width: 100px; display: inline-block"> <= ' + max_interval +
							'</p><button type="button" class="btn btn-default final_validation">Validate</button></div>'
						);
						// when the user validate
						$('.final_validation').click(function() {
							var final_proba = parseFloat($('#final_proba').val());
							if (final_proba <= 1 && final_proba >= 0) {
								// we save it
								assess_session.attributes[indice].questionnaire.points[question_val] = final_proba*2;
								assess_session.attributes[indice].questionnaire.number += 1;
								// backup local
								localStorage.setItem("assess_session", JSON.stringify(assess_session));
								// we reload the page
								window.location.reload();
							}
						});
					}
					// HANDLE USERS ACTIONS
					$('.lottery_a').click(function() {
						$.post('ajax', '{"type":"question", "method": "LE", "proba": ' + String(probability) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "0" , "mode": "' + String(mode) + '"}', function(data) {
							treat_answer(data);
							console.log(data);
						});
					});
					$('.lottery_b').click(function() {
						$.post('ajax', '{"type":"question","method": "LE", "proba": ' + String(probability) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "1" , "mode": "' + String(mode) + '"}', function(data) {
							treat_answer(data);
							console.log(data);
						});
					});
				})()
			}
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			///////////////////////////////////////////////////////////////// CE METHOD ////////////////////////////////////////////////////////////////
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			else if (method == 'CE_Constant_Prob') {
				(function() {
					// VARIABLES
					var min_interval = (assess_session.attributes[indice].questionnaire.number==2 ? parseFloat(Object.keys(assess_session.attributes[indice].questionnaire.points)[0]) : parseFloat(val_min)),  
					    max_interval = (assess_session.attributes[indice].questionnaire.number==1 ? parseFloat(Object.keys(assess_session.attributes[indice].questionnaire.points)[0]) : parseFloat(val_max)); 
					
					var L = [0.75 * (max_interval - min_interval) + min_interval, 0.25 * (max_interval - min_interval) + min_interval];
					var gain = Math.round(random_proba(L[0], L[1]));
					// INTERFACE
					var arbre_ce = new Arbre('ce', '#trees', settings.display, "CE");
					// SETUP ARBRE GAUCHE
					arbre_ce.questions_proba_haut = settings.proba_ce;
					arbre_ce.questions_val_max = String(max_interval) + ' ' + unit;
					arbre_ce.questions_val_min = String(min_interval) + ' ' + unit;
					arbre_ce.questions_val_mean = String(gain) + ' ' + unit;
					arbre_ce.display();
					arbre_ce.update();
					// we add the choice button
					$('#trees').append('<div class=choice style="text-align: center;"><p>Which option do you prefer?</p><button type="button" class="btn btn-default" id="gain">Certain gain</button><button type="button" class="btn btn-default" id="lottery">Lottery</button></div>')
					function utility_finder(gain) {
						var points = assess_session.attributes[indice].questionnaire.points;
						if (gain == val_min) {
							return (mode == 'Normal' ? 0 : 1);
						} else if (gain == val_max) {
							return (mode == 'Normal' ? 1 : 0);
						} else {
							for (var key in assess_session.attributes[indice].questionnaire.points) {
								if (gain == key) {
									return assess_session.attributes[indice].questionnaire.points[key];
								}
							};
						};
					};
					function treat_answer(data) {
						min_interval = data.interval[0];
						max_interval = data.interval[1];
						gain = data.gain;
						
						if (max_interval - min_interval <= 0.05 * parseFloat(arbre_ce.questions_val_max) - parseFloat(arbre_ce.questions_val_min) || max_interval - min_interval < 2) {
							$('.choice').hide();
							arbre_ce.questions_val_mean = gain + ' ' + unit;
							arbre_ce.update();
							ask_final_value(Math.round((max_interval + min_interval) * 100 / 2) / 100);
						} else {
							arbre_ce.questions_val_mean = gain + ' ' + unit;
							arbre_ce.update();
						}
					}
					function ask_final_value(val) {
						$('.lottery_a').hide();
						$('.lottery_b').hide();
						$('.container-fluid').append(
							'<div id= "final_value" style="text-align: center;"><br /><br /><p><p>We are almost done. Please enter the value that makes you indifferent between the two situations above. Your previous choices indicate that it should be between ' + min_interval + ' and ' + max_interval + ' but you are not constrained to that range <br /> ' + min_interval +
							'\
						 <= <input type="text" class="form-control" id="final_proba" placeholder="Probability" value="' + val + '" style="width: 100px; display: inline-block"> <= ' + max_interval +
							'</p><button type="button" class="btn btn-default final_validation">Validate</button></div>'
						);
			
						// when the user validate
						$('.final_validation').click(function() {
							var final_gain = parseFloat($('#final_proba').val());
							var final_utility = arbre_ce.questions_proba_haut * utility_finder(parseFloat(arbre_ce.questions_val_max)) + (1 - arbre_ce.questions_proba_haut) * utility_finder(parseFloat(arbre_ce.questions_val_min));
							console.log(arbre_ce.questions_proba_haut);
							console.log(utility_finder(parseFloat(arbre_ce.questions_val_max)));
							console.log(utility_finder(parseFloat(arbre_ce.questions_val_min)));
							if (final_gain <= parseFloat(arbre_ce.questions_val_max) && final_gain >= parseFloat(arbre_ce.questions_val_min)) {
								// we save it
								assess_session.attributes[indice].questionnaire.points[String(final_gain)]=parseFloat(final_utility);
								var  point_cepv= Object.keys(assess_session.attributes[indice].questionnaire.points).length-1
								var  number_cepv = assess_session.attributes[indice].questionnaire.number
								console.log( point_cepv)
								console.log( number_cepv)
								if ( point_cepv == number_cepv ){
									assess_session.attributes[indice].questionnaire.number += 1;
								}
								
								// backup local
								localStorage.setItem("assess_session", JSON.stringify(assess_session));
								// we reload the page
								window.location.reload();
							}
						});
					}
					// HANDLE USERS ACTIONS
					$('#lottery').click(function() {
						$.post('ajax', '{"type":"question", "method": "CE_Constant_Prob", "gain": ' + String(gain) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "0" , "mode": "' + String(mode) + '"}', function(data) {
							treat_answer(data);
							console.log(data);
							console.log(String(mode)=="Reversed");
							console.log("lottery");
						});
					});
					$('#gain').click(function() {
						$.post('ajax', '{"type":"question","method": "CE_Constant_Prob", "gain": ' + String(gain) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "1" , "mode": "' + String(mode) + '"}', function(data) {
							treat_answer(data);
							console.log(data);
							console.log(String(mode)=="Reversed");
							console.log("gain");
						});
					});
				})()
			}
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			///////////////////////////////////////////////////////////////// CEPV METHOD ////////////////////////////////////////////////////////////////
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			else if (method == 'CE_Variable_Prob') {
				(function() {
					// VARIABLES
					var min_interval = val_min;
					var max_interval = val_max;
					if (Object.keys(assess_session.attributes[indice].questionnaire.points).length == 0) {
						p = 0.25;
					} else if (Object.keys(assess_session.attributes[indice].questionnaire.points).length == 1) {
						p = 0.5;
					} else if (Object.keys(assess_session.attributes[indice].questionnaire.points).length == 2) {
		                 		p = 0.75;
					}
					var L = [0.75 * (max_interval - min_interval) + min_interval, 0.25 * (max_interval - min_interval) + min_interval];
					var gain = Math.round(random_proba(L[0], L[1]));
                                      
					// INTERFACE
					var arbre_cepv = new Arbre('cepv', '#trees', settings.display, "CE_PV");
					// SETUP ARBRE GAUCHE
					arbre_cepv.questions_proba_haut = p;
					arbre_cepv.questions_val_max = max_interval + ' ' + unit;
					arbre_cepv.questions_val_min = min_interval + ' ' + unit;
					arbre_cepv.questions_val_mean = gain + ' ' + unit;
					arbre_cepv.display();
					arbre_cepv.update();
					// we add the choice button
                                        $('#trees').append('<div class=choice style="text-align: center;"><p>Which option do you prefer?</p><button type="button" class="btn btn-default" id="gain">Certain gain</button><button type="button" class="btn btn-default" id="lottery">Lottery</button></div>')
					
					function utility_finder(gain) {
						var points = assess_session.attributes[indice].questionnaire.points;
						if (gain == val_min) {
							return (mode == 'Normal' ? 0 : 1);
						} else if (gain == val_max) {
							return (mode == 'Normal' ? 1 : 0);
						} else {
							for (var key in assess_session.attributes[indice].questionnaire.points) {
								if (gain == key) {
									return assess_session.attributes[indice].questionnaire.points[key];
								}
							};
						};
						
					}
					function treat_answer(data) {
						min_interval = data.interval[0];
						max_interval = data.interval[1];
						gain = data.gain;
						if (max_interval - min_interval <= 0.05 * parseFloat(arbre_cepv.questions_val_max) - parseFloat(arbre_cepv.questions_val_min) || max_interval - min_interval < 2) {
							$('#gain').hide();
							$('#lottery').hide();
							arbre_cepv.questions_val_mean = gain + ' ' + unit;
							arbre_cepv.update();
							ask_final_value(Math.round((max_interval + min_interval) * 100 / 2) / 100);
						} else {
							arbre_cepv.questions_val_mean = gain + ' ' + unit;
							arbre_cepv.update();
						}
					}
					function ask_final_value(val) {
						$('.lottery_a').hide();
						$('.lottery_b').hide();
						$('.container-fluid').append(
							'<div id= "final_value" style="text-align: center;"><br /><br /><p>We are almost done. Please enter the probability that makes you indifferent between the two situations above. Your previous choices indicate that it should be between ' + min_interval + ' and ' + max_interval + ' but you are not constrained to that range <br /> ' + min_interval +
							'\
						 <= <input type="text" class="form-control" id="final_proba" placeholder="Probability" value="' + val + '" style="width: 100px; display: inline-block"> <= ' + max_interval +
							'</p><button type="button" class="btn btn-default final_validation">Validate</button></div>'
						);
						// when the user validate
						$('.final_validation').click(function() {
							var final_gain = parseFloat($('#final_proba').val());
							var final_utility = arbre_cepv.questions_proba_haut;
							console.log(final_utility)
							console.log(final_gain);
							if (final_gain <= parseFloat(arbre_cepv.questions_val_max) && final_gain >= parseFloat(arbre_cepv.questions_val_min)) {
								// we save it
								assess_session.attributes[indice].questionnaire.points[String(final_gain)]=parseFloat(final_utility);
								console.log(assess_session.attributes[indice].questionnaire.points)
								var  point_cepv= Object.keys(assess_session.attributes[indice].questionnaire.points).length-1
								var  number_cepv = assess_session.attributes[indice].questionnaire.number
								console.log( point_cepv)
								console.log( number_cepv)
								if ( point_cepv == number_cepv ){
									assess_session.attributes[indice].questionnaire.number += 1;
								}
								console.log( point_cepv)
								console.log( assess_session.attributes[indice].questionnaire.number )
								// backup local
								localStorage.setItem("assess_session", JSON.stringify(assess_session));
								// we reload the page
								window.location.reload();
							}
								
						});
						console.log( assess_session.attributes[indice].questionnaire.number )
					}
					// HANDLE USERS ACTIONS
					$('#lottery').click(function() {
						$.post('ajax', '{"type":"question", "method": "CE_Constant_Prob", "gain": ' + String(gain) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "0" , "mode": "' + String(mode) + '"}', function(data) {
							treat_answer(data);
							console.log(data);
						});
					});
					$('#gain').click(function() {
						$.post('ajax', '{"type":"question","method": "CE_Constant_Prob", "gain": ' + String(gain) + ', "min_interval": ' + min_interval + ', "max_interval": ' + max_interval + ' ,"choice": "1" , "mode": "' + String(mode) + '"}', function(data) {
							treat_answer(data);
							console.log(data);
						});
					});
				})()
			}
		});
		/// When you click on a QUALITATIVE attribute for assessment
		$('.answer_quest_quali').click(function() {
			// we store the name of the attribute
			var question_id = $(this).attr('id').slice(2).split('_'),
				question_name = question_id[0],
				question_val = question_id[1],
				question_index = question_id[2];
			
			// we delete the select div
			$('#select').hide();
			$('#attribute_name').show().html(question_name.toUpperCase());
			// which index is it ? / which attribute is it ?
			var indice;
			for (var j = 0; j < assess_session.attributes.length; j++) {
				if (assess_session.attributes[j].name == question_name) {
					indice = j;
				}
			}
			var val_min = assess_session.attributes[indice].val_min,
				val_max = assess_session.attributes[indice].val_max,
				method = assess_session.attributes[indice].method;
		
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			///////////////////////////////////////////////////////////////// PE METHOD ////////////////////////////////////////////////////////////////
			//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			if (method == 'PE') {
				(function() {
					// VARIABLES
					var probability = 0.75,
						min_interval = 0,
						max_interval = 1;
					// INTERFACE
					var arbre_pe = new Arbre('pe', '#trees', settings.display, "PE");
					
					// The certain gain is the clicked med_value					
					arbre_pe.questions_val_mean = question_val;
					
					// SETUP ARBRE GAUCHE
					arbre_pe.questions_proba_haut = probability;
					
					arbre_pe.questions_val_max = val_max;
					arbre_pe.questions_val_min = val_min;
					
					arbre_pe.display();
					arbre_pe.update();
					$('#trees').append('</div><div class=choice style="text-align: center;">'+
										'<p>Which option do you prefer?</p>'+
										'<button type="button" class="btn btn-default" id="gain"> Certain gain </button>'+
										'<button type="button" class="btn btn-default" id="lottery"> Lottery </button></div>');
					// FUNCTIONS
					function sync_values() {
						arbre_pe.questions_proba_haut = probability;
						arbre_pe.update();
					}
					function treat_answer(data) {
						min_interval = data.interval[0];
						max_interval = data.interval[1];
						probability = parseFloat(data.proba).toFixed(2);
						if (max_interval - min_interval <= 0.05) {
							sync_values();
							ask_final_value(Math.round((max_interval + min_interval) * 100 / 2) / 100);
						} else {
							sync_values();
						}
					}
					function ask_final_value(val) {
						// we delete the choice div
						$('.choice').hide();
						$('.container-fluid').append(
							'<div id= "final_value" style="text-align: center;"><br /><br />'+
							'<p>We are almost done. Please enter the probability that makes you indifferent between the two situations above. Your previous choices indicate that it should be between ' + min_interval + ' and ' + max_interval + ' but you are not constrained to that range <br /> ' + min_interval +
							'\
							<= <input type="text" class="form-control" id="final_proba" placeholder="Probability" value="' + val + '" style="width: 100px; display: inline-block"> <= ' + max_interval +
							'</p><button type="button" class="btn btn-default final_validation">Validate</button></div>'
						);
						// when the user validate
						$('.final_validation').click(function() {
							var final_proba = parseFloat($('#final_proba').val());
							if (final_proba <= 1 && final_proba >= 0) {
								// we save it
								assess_session.attributes[indice].questionnaire.points[question_val]=final_proba;
								assess_session.attributes[indice].questionnaire.number += 1;
								
								localStorage.setItem("assess_session", JSON.stringify(assess_session)); // backup local
								window.location.reload(); // we reload the page
							}
						});
					}
					sync_values();
					// HANDLE USERS ACTIONS
					$('#gain').click(function() {
						$.post('ajax', 
							'{"type":"question",'+
							'"method": "PE",'+
							'"proba": ' + String(probability) + ','+
							'"min_interval": ' + min_interval + ','+
							'"max_interval": ' + max_interval + ','+
							'"choice": "0",'+
							'"mode": "normal"}',
							function(data) {
								treat_answer(data);
								console.log("PE 2");
							});
					});
					$('#lottery').click(function() {
						$.post('ajax', 
							'{"type":"question",'+
							'"method": "PE",'+
							'"proba": ' + String(probability) + ','+
							'"min_interval": ' + min_interval + ','+
							'"max_interval": ' + max_interval + ','+
							'"choice": "1",'+
							'"mode": "normal"}',
							function(data) {
								treat_answer(data);
								console.log("PE 2");
							});
					});
				})()
			}
		});
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		///////////////////////////////////////////////////////////////// CLICK ON THE UTILITY BUTTON ////////////////////////////////////////////////////////////////
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		$('.calc_util_quanti').click(function() {
			// we store the name of the attribute
			
			var name = $(this).attr('id').slice(2);
			console.log(name);
			
			
			
			
			// we hide the slect div
			$('#select').hide();
			// which index is it ?
			var indice;
			for (var j = 0; j < assess_session.attributes.length; j++) {
				if (assess_session.attributes[j].name == name) {
					indice = j;
				}
			}
			
			var val_min = assess_session.attributes[indice].val_min,
				val_max = assess_session.attributes[indice].val_max,
				mode = assess_session.attributes[indice].mode,
				points_dict = assess_session.attributes[indice].questionnaire.points,
				points=[];
			
			for (key in points_dict) {
				points.push([parseFloat(key), parseFloat(points_dict[key])]);
			};
			
			points.push([val_min, (mode == "Normal" ? 0 : 1)]);
			points.push([val_max, (mode == "Normal" ? 1 : 0)]);
			
			if (val_min<0) {
				for (i in points) {
					points[i][0]-=val_min;
					console.log(points[i]);
				};
			}
			
			
			
			var json_2_send = {
				"type": "calc_util_multi"
			};
			json_2_send["points"] = points;
			console.log(points);
			function reduce_signe(nombre, dpl=true, signe=true) {
				console.log("Reduce signe");
				if (nombre >= 0 && signe==true) {
					if (dpl==false) {
						if (nombre > 999) {
							return ("+" + nombre.toExponential(settings.decimals_equations)).replace("e+", "\\times10^{")+"}";
						}
						else if (nombre < 0.01) {
							return ("+" + nombre.toExponential(settings.decimals_equations)).replace("e-", "\\times10^{-")+"}";
						}
						else {
							return "+" + nombre.toPrecision(settings.decimals_equations);
						}
					}
					else {
						return "+" + nombre.toPrecision(settings.decimals_dpl);
					}
				} else {
					if (dpl==false) {
						if (Math.abs(nombre) > 999) {
							return String(nombre.toExponential(settings.decimals_equations)).replace("e+","\\times10^{")+"}";
						}
						else if (Math.abs(nombre) < 0.01) {
							return String(nombre.toExponential(settings.decimals_equations)).replace("e-", "\\times10^{-")+"}";
						}
						else {
							return nombre.toPrecision(settings.decimals_equations);
						}
					}
					else {
						return nombre.toPrecision(settings.decimals_dpl);
					}
				}
			};
			function addTextForm(div_function, copie, render, key, excel) {
				console.log("addtextform");
				if (settings.language=="french") {
					excel=excel.replace(/\./gi,",");
				}
				var copy_button_dpl = $('<button class="btn functions_text_form" id="btn_dpl_' + key + '" data-clipboard-text="' + copie + '" title="Click to copy me.">Copy to clipboard (DPL format)</button>');
				var copy_button_excel = $('<button class="btn functions_text_form" id="btn_excel_' + key + '" data-clipboard-text="' + excel + '" title="Click to copy me.">Copy to clipboard (Excel format)</button>');
				var copy_button_latex = $('<button class="btn functions_text_form" id="btn_latex_' + key + '" data-clipboard-text="' + render + '" title="Click to copy me.">Copy to clipboard (LaTeX format)</button>');
				if (settings.language=="french") {
					render=render.replace(/\./gi,",");
				}
				var ajax_render = {
					"type": "latex_render",
					"formula": render
				};
				$.post('ajax', JSON.stringify(ajax_render), function (data) {
					div_function.append("<img src='data:image/png;base64,"+ data +"' alt='"+key+"' />");
					div_function.append("<br /><br />");
					div_function.append(copy_button_dpl);
					div_function.append("<br /><br />");
					div_function.append(copy_button_excel);
					div_function.append("<br /><br />");
					div_function.append(copy_button_latex);
				});
				$('#functions').append(div_function);
				var client = new Clipboard("#btn_dpl_" + key);
				client.on("success", function(event) {
					copy_button_dpl.text("Done !");
					setTimeout(function() {
						copy_button_dpl.text("Copy to clipboard (DPL format)");
					}, 2000);
				});
				var client = new Clipboard("#btn_excel_" + key);
				client.on("success", function(event) {
					copy_button_excel.text("Done !");
					setTimeout(function() {
						copy_button_excel.text("Copy to clipboard (Excel format)");
					}, 2000);
				});
				var client = new Clipboard("#btn_latex_" + key);
				client.on("success", function(event) {
					copy_button_latex.text("Done !");
					setTimeout(function() {
						copy_button_latex.text("Copy to clipboard LaTeX format)");
					}, 2000);
				});
			}
			function addFunctions(i, data, mini,choice) {
				var delta = Math.abs(mini).toString();
				for (var key in data[i]) {
					
					if (mini<0){
						if (key == 'exp'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#401539">Exponential</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*exp(" + reduce_signe(-data[i][key]['b']) + "(x+" + delta +"))" + reduce_signe(data[i][key]['c']);
							var render = reduce_signe(data[i][key]['a'],false, false) + 'e^{' + reduce_signe(-data[i][key]['b'],false) + '(x+' + delta + ')}' + reduce_signe(data[i][key]['c'],false);
							var excel = reduce_signe(data[i][key]['a']) + "*EXP(" + reduce_signe(-data[i][key]['b']) + "*(x+" + delta + "))" + reduce_signe(data[i][key]['c']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'log') {
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#D9585A">Logarithmic</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*log(" + reduce_signe(data[i][key]['b']) + "(x+" + delta+"))" + reduce_signe(data[i][key]['c']) + ")" + reduce_signe(data[i][key]['d']);
							var render = reduce_signe(data[i][key]['a'], false, false) + "\\log(" + reduce_signe(data[i][key]['b'], false, false) + "(x+"+ delta + ")" + reduce_signe(data[i][key]['c'],false) + ")" + reduce_signe(data[i][key]['d'],false);
							var excel = reduce_signe(data[i][key]['a']) + "*LN(" + reduce_signe(data[i][key]['b']) + "(x+"+ delta + ")" + reduce_signe(data[i][key]['c']) + ")" + reduce_signe(data[i][key]['d']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'pow') {
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#6DA63C">Power</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*(pow((x+" + delta + ")," + (1 - data[i][key]['b']) + ")-1)/(" + reduce_signe(1 - data[i][key]['b']) + ")" + reduce_signe(data[i][key]['c']);
							var render = reduce_signe(data[i][key]['a'], false, false) + "\\frac{(x+" + delta + ")^{" + reduce_signe(1 - data[i][key]['b'], false) + "}-1}{" + reduce_signe(1 - data[i][key]['b'], false) + "}" + reduce_signe(data[i][key]['c'], false);
							var excel = reduce_signe(data[i][key]['a']) + "*((x+" + delta + ")^" + (1 - data[i][key]['b']) + "-1)/(" + reduce_signe(1 - data[i][key]['b']) + ")" + reduce_signe(data[i][key]['c']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'quad'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#458C8C">Quadratic</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['c']) + "*(x+"+delta+")" + reduce_signe(-data[i][key]['b']) + "*pow((x+"+delta+"),2)" + reduce_signe(data[i][key]['a']);
							var render = reduce_signe(data[i][key]['c'], false, false) + "(x+"+delta+")" + reduce_signe(-data[i][key]['b'], false) + "(x+"+delta+")^{2}" + reduce_signe(data[i][key]['a'], false);
							var excel = reduce_signe(data[i][key]['c']) + "*(x+" + delta + ")^" + reduce_signe(-data[i][key]['b']) + "*(x+" + delta + ")^2" + reduce_signe(data[i][key]['a']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'lin') {
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#D9B504">Linear</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*(x+" + delta + ")" + reduce_signe(data[i][key]['b']);
							var render = reduce_signe(data[i][key]['a'], false, false) + "(x+" + delta + ")" + reduce_signe(data[i][key]['b'], false);
							var excel = reduce_signe(data[i][key]['a']) + "*(x+" + delta + ")" + reduce_signe(data[i][key]['b']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'expo-powerr'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#26C4EC">Expo-Power</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "+exp(-(" + reduce_signe(data[i][key]['b']) + ")*pow((x+"+delta+")," + reduce_signe(data[i][key]['c']) + "))" ;
							var render = reduce_signe(data[i][key]['a'], false, false) + "+exp(" + reduce_signe(-data[i][key]['b'], false, false) + "*(x+"+delta+")^{" + reduce_signe(data[i][key]['c'], false, false) + "})" ;
							var excel = reduce_signe(data[i][key]['a']) + "+EXP(-(" + reduce_signe(data[i][key]['b']) + ")*(x+"+delta+")^" + reduce_signe(data[i][key]['c']) + ")" ;
							addTextForm(div_function, copie, render, key, excel);
						}
					
					}else{
						if (key == 'exp'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#401539">Exponential</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*exp(" + reduce_signe(-data[i][key]['b']) + "x)" + reduce_signe(data[i][key]['c']);
							var render = reduce_signe(data[i][key]['a'],false, false) + 'e^{' + reduce_signe(-data[i][key]['b'],false) + 'x}' + reduce_signe(data[i][key]['c'],false);
							var excel = reduce_signe(data[i][key]['a']) + "*EXP(" + reduce_signe(-data[i][key]['b']) + "*x)" + reduce_signe(data[i][key]['c']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'log'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#D9585A">Logarithmic</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*log(" + reduce_signe(data[i][key]['b']) + "x" + reduce_signe(data[i][key]['c']) + ")" + reduce_signe(data[i][key]['d']);
							var render = reduce_signe(data[i][key]['a'], false, false) + "\\log(" + reduce_signe(data[i][key]['b'], false, false) + "x" + reduce_signe(data[i][key]['c'],false) + ")" + reduce_signe(data[i][key]['d'],false);
							var excel = reduce_signe(data[i][key]['a']) + "*LN(" + reduce_signe(data[i][key]['b']) + "x" + reduce_signe(data[i][key]['c']) + ")" + reduce_signe(data[i][key]['d']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'pow'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#6DA63C">Power</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*(pow(x," + (1 - data[i][key]['b']) + ")-1)/(" + reduce_signe(1 - data[i][key]['b']) + ")" + reduce_signe(data[i][key]['c']);
							var render = reduce_signe(data[i][key]['a'], false, false) + "\\frac{x^{" + reduce_signe(1 - data[i][key]['b'], false) + "}-1}{" + reduce_signe(1 - data[i][key]['b'], false) + "}" + reduce_signe(data[i][key]['c'], false);
							var excel = reduce_signe(data[i][key]['a']) + "*(x^" + (1 - data[i][key]['b']) + "-1)/(" + reduce_signe(1 - data[i][key]['b']) + ")" + reduce_signe(data[i][key]['c']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'quad'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#458C8C">Quadratic</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['c']) + "*x" + reduce_signe(-data[i][key]['b']) + "*pow(x,2)" + reduce_signe(data[i][key]['a']);
							var render = reduce_signe(data[i][key]['c'], false, false) + "x" + reduce_signe(-data[i][key]['b'], false) + "x^{2}" + reduce_signe(data[i][key]['a'], false);
							var excel = reduce_signe(data[i][key]['c']) + "*x" + reduce_signe(-data[i][key]['b']) + "*x^2" + reduce_signe(data[i][key]['a']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'lin'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#D9B504">Linear</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "*x" + reduce_signe(data[i][key]['b']);
							var render = reduce_signe(data[i][key]['a'], false, false) + "x" + reduce_signe(data[i][key]['b'], false);
							var excel = reduce_signe(data[i][key]['a']) + "*x" + reduce_signe(data[i][key]['b']);
							addTextForm(div_function, copie, render, key, excel);
						} else if (key == 'expo-powerr'){
						
							var div_function = $('<div id="' + key + '" class="functions_graph" style="overflow-x: auto;"><h3 style="color:#26C4EC">Expo-Power</h3><br />Coefficient of determination: ' + Math.round(data[i][key]['r2'] * 100) / 100 + '<br /><br/></div>');
							var copie = reduce_signe(data[i][key]['a']) + "+exp(-(" + reduce_signe(data[i][key]['b']) + ")*pow(x," + reduce_signe(data[i][key]['c']) + "))" ;
							var render = reduce_signe(data[i][key]['a'], false, false) + "+exp(" + reduce_signe(-data[i][key]['b'], false, false) + "*x^{" + reduce_signe(data[i][key]['c'], false, false) + "})" ;
							var excel = reduce_signe(data[i][key]['a']) + "+EXP(-(" + reduce_signe(data[i][key]['b']) + ")*x^" + reduce_signe(data[i][key]['c']) + ")" ;
							addTextForm(div_function, copie, render, key, excel);
						}
					};
				}
			}
			function addGraph(i, data, min, max, choice) {
				console.log("addgraph");
				$.post('ajax', JSON.stringify({
					"type": "svgg",
					"data": data[i],
					"min": min,
					"max": max,
					"liste_cord": data[i]['coord'],
					"width": 4,
					"choice":choice,
				}), function(data2) {
					$('#fonction_choisie').append(data2);
				});
			}
			function addGraph2(i, data, min, max,liste) {
				console.log("addgraph");
				$.post('ajax', JSON.stringify({
					"type": "svg",
					"data": data[i],
					"min": min,
					"max": max,
					"liste_cord": data[i]['coord'],
					"width": 4,
					"liste":liste
					
				}), function(data2) {
					$('#fonctions_choisies').append(data2);
				});
			}
			function addGraph3(i, data, min, max, choice) {
				console.log("addgraph");
				$.post('ajax', JSON.stringify({
					"type": "svgg",
					"data": data[i],
					"min": min,
					"max": max,
					"liste_cord": data[i]['coord'],
					"width": 2.5,
					"choice":choice,
				}), function(data2) {
					$('#graph_choisi' + indice).append('<div>You chose ' +choice+ '</div>');
					$('#graph_choisi' + indice).append('<div>' + data2 + '</div>');
				});
			}
			
			function availableRegressions(data) {
				console.log("availreg");
				var text = '';
				for (var key in data) {
					if (typeof(data[key]['r2']) !== 'undefined') {
						if (key != 'quad') {
							if (key != 'expo-power') {
							text = text + key + ': ' + Math.round(data[key]['r2'] * 10000) / 10000 + ', ';
							}
						}
					}
				};
				for (var key in data) {
					if (typeof(data[key]['r2']) !== 'undefined') {
						if (key != 'lin') {
							if (key != 'expo-power') {
								if (key != 'pow') {
									if (key != 'exp') {
									 	if (key != 'log') {
							
							text = text + key + ': ' + Math.round(data[key]['r2'] * 10000) / 10000 + ', ';
							}}}}}
						
					}
					
				}
				
				
				return text;
			}
			
			function availableRegressions2(data) {
				console.log("availreg");
				var text = '';
				for (var key in data) {
					if (typeof(data[key]['r2']) !== 'undefined') {
						if (key != 'quad') {
							if (key != 'expo-power') {
							text = text + key + ': ' + Math.round(data[key]['r2'] * 10000) / 10000 + ', ';
							}
						}
					}
				}
				return text;
			}
			
			$.post('ajax', JSON.stringify(json_2_send), function(data) {
				$('#charts').show().empty();
				$('#nouveaubloc').show().empty();
				$('#attribute_name').show().empty();
				
			
				
				if (val_min<0){
					for (i in data['data']){
						for (j in data['data'][i]['coord']){
							data['data'][i]['coord'][j][0]+=val_min;
						};
					};
				}
				var assess_session = JSON.parse(localStorage.getItem("assess_session"));
				
				$('#attribute_name').append('<h2>' + assess_session.attributes[indice].name + '</h2>');
				assess_session.attributes[indice].numero = 10000;
				assess_session.attributes[indice].fonction = '';
				
				
				
				localStorage.setItem("assess_session", JSON.stringify(assess_session));
				$('#nouveaubloc').append('<table id="show_function" class="table"><thead><tr><th>Choose a function here</th><th>The utility function you chose</th><th>See the functions here</th><th>The utility functions you want to see</th></tr></thead><tbody><tr><td id ="tableau_des_choix"></td><td id = "fonction_choisie"></td><td id ="tableau_checkbox"></td><td id ="fonctions_choisies"></td></tr></tbody></table>');
				$('#tableau_des_choix').append('<table id="NEWcurves_choice" class="table"><thead><tr><th></th><th> Functions </th></tr></thead></table>');
				$('#tableau_checkbox').append('<table id="checkbox_curves_choice" class="table"><thead><tr><th></th><th> Functions </th></tr></thead></table>');
				LISTE=['logarithmic','exponential','power','linear'];
					if (data['data'][0]['quad'] !== undefined) {
						LISTE = ['logarithmic','exponential','power','linear','quadratic'];
						};
				for (var i = 0; i < LISTE.length; i++) {
					$('#NEWcurves_choice').append('<tr><td><input type="radio" class="ice" name="select2" value=' +LISTE[i]+ '></td><td>' + LISTE[i] + '</td><tr>');
					
				}
				$('#charts').append('<table id="curves_choice" class="table"><thead><tr><th></th><th>Points used</th><th>Available regressions: r2</th></tr></thead></table>');
				if (data['data'][0]['quad'] == undefined) {
					for (var i = 0; i < data['data'].length; i++) {
						regressions_text = availableRegressions2(data['data'][i]);
						$('#curves_choice').append('<tr><td><input type="radio" class="hoice" name="select" value=' + i + '></td><td>' + data['data'][i]['points'] + '</td><td>' + regressions_text + '</td></tr>');
					}
				};
				if (data['data'][0]['quad'] !== undefined) {
				
				for (var i = 0; i < data['data'].length; i++) {
						regressions_text = availableRegressions(data['data'][i]);
						$('#curves_choice').append('<tr><td><input type="radio" class="hoice" name="select" value=' + i + '></td><td>' + data['data'][i]['points'] + '</td><td>' + regressions_text + '</td></tr>');
					}
				};
				$('#checkbox_curves_choice').append('<tr><td><input type="checkbox" class="check_log" id="check_log" name="check_log"></td><td>' + LISTE[0] + '</td><tr>');
				$('#checkbox_curves_choice').append('<tr><td><input type="checkbox" class="check_exp" id="check_exp" name="check_exp"></td><td>' + LISTE[1] + '</td><tr>');
				$('#checkbox_curves_choice').append('<tr><td><input type="checkbox" class="check_pow" id="check_pow" name="check_pow"></td><td>' + LISTE[2] + '</td><tr>');
				$('#checkbox_curves_choice').append('<tr><td><input type="checkbox" class="check_lin" id="check_lin" name="check_lin"></td><td>' + LISTE[3] + '</td><tr>');
				if (LISTE.length==5){
					$('#checkbox_curves_choice').append('<tr><td><input type="checkbox" class="check_quad" id="check_quad" name="check_quad"></td><td>' + LISTE[4] + '</td><tr>');
				};
				
				
				var L=[1,1,1,1,1];
				
				
				$("input[type=checkbox][name=check_log]").change(function() {
								
								var assess_session = JSON.parse(localStorage.getItem("assess_session"));
								var num = assess_session.attributes[indice].numero;
								
								
								
								
							var checked = document.getElementById('check_log').checked;
							if(checked) {
								
								L[0]=1;
								var R=['logarithmic'];
								if (L[1] == 1){
									R.push('exponential');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							if(!checked) {
								L[0]=0;
								var R=[];
								
								if (L[1] == 1){
									R.push('exponential');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							
							localStorage.setItem("assess_session", JSON.stringify(assess_session));
							
								
					});
				
				$("input[type=checkbox][name=check_exp]").change(function() {
								
								var assess_session = JSON.parse(localStorage.getItem("assess_session"));
								var num = assess_session.attributes[indice].numero;
								
								
								
								
							var checked = document.getElementById('check_exp').checked;
							if(checked) {
								
								L[1]=1;
								var R=['exponential'];
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							if(!checked) {
								L[1]=0;
								var R=[];
								
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							
							localStorage.setItem("assess_session", JSON.stringify(assess_session));
							
								
					});
				$("input[type=checkbox][name=check_pow]").change(function() {
								
								var assess_session = JSON.parse(localStorage.getItem("assess_session"));
								var num = assess_session.attributes[indice].numero;
								
								
								
								
							var checked = document.getElementById('check_pow').checked;
							if(checked) {
								
								L[2]=1;
								var R=['power'];
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[1] == 1){
									R.push('exponential');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							if(!checked) {
								L[2]=0;
								var R=[];
								
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[1] == 1){
									R.push('exponential');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							
							localStorage.setItem("assess_session", JSON.stringify(assess_session));
							
								
					});
				$("input[type=checkbox][name=check_lin]").change(function() {
								
								var assess_session = JSON.parse(localStorage.getItem("assess_session"));
								var num = assess_session.attributes[indice].numero;
								
								
								
								
							var checked = document.getElementById('check_lin').checked;
							if(checked) {
								
								L[3]=1;
								var R=['linear'];
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[1] == 1){
									R.push('exponential');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							if(!checked) {
								L[3]=0;
								var R=[];
								
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[1] == 1){
									R.push('exponential');
								};
								if (LISTE.length==5){
									if (L[4] == 1){
										R.push('quadratic');
									};
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							
							localStorage.setItem("assess_session", JSON.stringify(assess_session));
							
								
					});
					
			
				if (LISTE.length==5){
				$("input[type=checkbox][name=check_quad]").change(function() {
					var assess_session = JSON.parse(localStorage.getItem("assess_session"));
					var num = assess_session.attributes[indice].numero;
					var checked = document.getElementById('check_quad').checked;
							if(checked) {
								
								L[4]=1;
								var R=['quadratic'];
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								
								if (L[1] == 1){
									R.push('exponential');
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							if(!checked) {
								L[4]=0;
								var R=[];
								
								if (L[0] == 1){
									R.push('logarithmic');
								};
								if (L[2] == 1){
									R.push('power');
								};
								if (L[3] == 1){
									R.push('linear');
								};
								if (L[1] == 1){
									R.push('exponential');
								};
								
								$('#fonctions_choisies').show().empty();
								addGraph2(num, data['data'], val_min, val_max,R);
								
							};
							
							localStorage.setItem("assess_session", JSON.stringify(assess_session));			
								
							
								
					});
				};
				
				
				$('.ice').on('click', function() {
			
					$('#choix_fonction').show();
					$('#ton_choix').empty();
					
				
					$('#update').hide();
					
					var choice = this.value;
					var assess_session = JSON.parse(localStorage.getItem("assess_session"));
					var num = assess_session.attributes[indice].numero;
					$('#ton_choix').append("You chose " + choice);
					
					
					assess_session.attributes[indice].fonction = choice;
					
					if (num!=10000){
					if (choice == 'quadratic'){
						
						if (data['data'][num]['quad'] == undefined) {
							
							assess_session.attributes[indice].fonction = '';
							$('#fonction_choisie').empty();
							$('#graph_choisi'+ indice).empty();
							$('#graph_choisi'+ indice).hide();
							$('#ton_choix').empty();
							$('#fonction_choisie').append("Quadratic can't be calculated for the points you chose");
							$('#ton_choix').append("Choose another function or other points");
							$('#update').hide();
							$('#functions').hide();
							
							
						};
						if (data['data'][num]['quad'] != undefined) {
								
								$('#functions').show().empty();
								$('#fonction_choisie').show().empty();
					
								$('#graph_choisi'+indice).show().empty();
						
							
								addGraph(num, data['data'], val_min, val_max, choice);
						
								addGraph3(num, data['data'], val_min, val_max, choice);
								addFunctions(num, data['data'],val_min,choice);
								$('#update').show();
							
						
						};
					};
					if (choice != 'quadratic'){
							
					
						
						$('#functions').show().empty();
						$('#fonction_choisie').show().empty();
					
						$('#graph_choisi'+indice).show().empty();
						
						
						addGraph(num, data['data'], val_min, val_max, choice);
						
						addGraph3(num, data['data'], val_min, val_max, choice);
						addFunctions(num, data['data'],val_min,choice);
						$('#update').show();
					};
					};
					localStorage.setItem("assess_session", JSON.stringify(assess_session));
					
					});
					
			
				
				$('.hoice').on('click', function() {
					var assess_session = JSON.parse(localStorage.getItem("assess_session"));
					
					
					var choice = assess_session.attributes[indice].fonction;
					assess_session.attributes[indice].numero = Number(this.value);
					
					
					
					$('#update').hide();
					
					$('#fonctions_choisies').show().empty();
					document.getElementById('check_log').checked = true;
					document.getElementById('check_exp').checked = true;
					document.getElementById('check_pow').checked = true;
					document.getElementById('check_lin').checked = true;
					if (LISTE.length==5){
						document.getElementById('check_quad').checked = true;
					};
					L=[1,1,1,1,1];
					addGraph2(Number(this.value), data['data'], val_min, val_max,LISTE);
					if (choice != ''){
						if (choice == 'quadratic'){
						
							if (data['data'][Number(this.value)]['quad'] == undefined) {
								
								assess_session.attributes[indice].fonction = '';
								$('#fonction_choisie').empty();
								$('#graph_choisi'+ indice).empty();
								$('#graph_choisi'+ indice).hide();
								$('#ton_choix').empty();
								$('#fonction_choisie').append("Quadratic can't be calculated for the points you chose");
								$('#ton_choix').append("Choose another function or other points");
								$('#update').hide();
								$('#functions').hide();
							};
							if (data['data'][Number(this.value)]['quad'] != undefined) {
								
								$('#functions').show().empty();
								$('#fonction_choisie').show().empty();
						
								$('#graph_choisi'+indice).show().empty();
						
								addGraph(Number(this.value), data['data'], val_min, val_max, choice);
						
								addGraph3(Number(this.value), data['data'], val_min, val_max, choice);
								addFunctions(Number(this.value), data['data'],val_min,choice);
								$('#update').show();
							};
						};
						if (choice != 'quadratic'){
							
							$('#functions').show().empty();
							$('#fonction_choisie').show().empty();
						
							$('#graph_choisi'+indice).show().empty();
						
							
						
							addGraph(Number(this.value), data['data'], val_min, val_max, choice);
						
							addGraph3(Number(this.value), data['data'], val_min, val_max, choice);
							addFunctions(Number(this.value), data['data'],val_min,choice);
							$('#update').show();
						};
						};
					localStorage.setItem("assess_session", JSON.stringify(assess_session));
						
					});
					
				$('.comeback').click(function() {
					
					
					$('#attribute_name').hide();
					$('#charts').hide();
					
					$('#functions').hide();
					$('#nouveaubloc').hide();
					$('#tableau_fonctions').hide();
					$('#choix_fonction').hide();
					
					$('#select').show();
					
					$('#fonction_choisie').empty();
					$('#fonctions_choisies').empty();
					
					
					
					
					});
			});
		});
		
		
		
	
	});
</script>
<!-- Library to copy into clipboard -->
<script src="{{ get_url('static', path='js/clipboard.min.js') }}"></script>
<style>
	table {
	  font-family: arial, sans-serif;
	  border-collapse: collapse;
	  width: 100%;
	}
	
	td, th {
	  border: 1px solid #dddddd;
	  text-align: left;
	  padding: 8px;
	}
	
	tr:nth-child(even) {
	  background-color: #e2e2e2;
	}
	</style>
</body>
</html>
