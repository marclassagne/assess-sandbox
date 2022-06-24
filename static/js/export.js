



var data_export_option={'attributes':[], 'k_calculus':[]};

///  ACTION FROM BUTTON UPDATE
$(function() {

	$('li.export').addClass("active");
	$('#export_json').click(function() {
		var data_2_export = localStorage['assess_session'];
		var button  = $('#export_json');
		button.attr('href', 'data:attachment/json,' + data_2_export);
		button.attr('target', '_blank');
		button.attr('download', 'myFile.json');
	});

	$('#export_xls').click(function() {

		var data_2_export = localStorage['assess_session'];
		$.post('ajax', '{"type":"export_xlsx", "data":'+data_2_export+'}', function(data) {
			document.location = "export_download/"+data;
		});
	});

	$("#excel0").click(function() {
		var data_2_export = localStorage['assess_session'];
		$.post('ajax', '{"type":"export_xlsx", "data":'+data_2_export+'}', function(data) {
			document.location = "export_download/"+data;
		});
	});

	$('#export_xls_option').click(function() {
		var data_2_export = JSON.stringify(data_export_option);
		$.post('ajax', '{"type":"export_xlsx_option", "data":'+data_2_export+'}', function(data) {
			document.location = "export_download/"+data;
		});
	});

	$('#checkbox_multiplicative').click(function() {
		checkbox_multiplicative();
	});
	$('#checkbox_multilinear').click(function(){
		checkbox_multilinear();
	});

	$('#generate_list').click(function(){ list(); });

});


function reduce(nombre){return Math.round(nombre*1000000)/1000000;}
function signe(nombre){if(nombre>=0){return "+"+nombre}else{return nombre}};

function list()
{
	var assess_session = JSON.parse(localStorage.getItem("assess_session"));

	// We fill the table
	for (var i=0; i < assess_session.attributes.length; i++){

		var text = '<tr><td>' + assess_session.attributes[i].name + '</td>';
		text+='<td>'+ assess_session.attributes[i].unit + '</td>';
		text+='<td id="charts_'+i+'"></td>';
		text+='<td id="functions_'+i+'"></td>';
		text+='</tr>';

		$('#table_attributes').append(text);

		(function(_i) {
			var json_2_send = {"type": "calc_util", "points":[]};
			var obj = assess_session.attributes[_i].questionnaire.points;
			var points = Object.keys(obj).map(function(key) {return [key, obj[key]];});
			var mode = assess_session.attributes[_i].mode;
			var val_max=assess_session.attributes[_i].val_max;
			var val_min=assess_session.attributes[_i].val_min;
			if (points.length > 0 && assess_session.attributes[i].checked) {
			if (mode=="Normal") {
				points.push([String(val_max), 1]);
				points.push([String(val_min), 0]);
			}
			else {
				points.push([String(val_max), 0]);
				points.push([String(val_min), 1]);
			}
			json_2_send["points"] = points;
				$.post('ajax', JSON.stringify(json_2_send), function (data) {
					$.post('ajax', JSON.stringify({
						"type": "svg",
						"data": data,
						"min": val_min,
						"max": val_max,
						"liste_cord": points,
                                                "width": 3,
                                                "liste": []
					}), function (data2) {

						$('#charts_' + _i).append('<div>' + data2 + '</div>');
						for (var key in data) {

							var functions = "";
							if (key == 'exp') {
								functions= '<label style="color:#401539"><input type="checkbox" id="checkbox_'+_i+'_exp"> Exponential (' + Math.round(data[key]['r2'] * 100) / 100 + ')</label><br/>';
								$('#functions_' + _i).append(functions);
								data[key]['type']='exp';
								(function(_data){$('#checkbox_'+_i+'_exp').click(function(){update_data_export_option(_i, "exp", _data)});})(data[key]);

							}
							else if (key == 'log'){
								functions='<label style="color:#D9585A"><input type="checkbox" id="checkbox_'+_i+'_log"> Logarithmic (' + Math.round(data[key]['r2'] * 100) / 100 + ')</label><br/>';
								$('#functions_' + _i).append(functions);
								data[key]['type']='log';
								(function(_data){$('#checkbox_'+_i+'_log').click(function(){update_data_export_option(_i, "log", _data)});})(data[key]);
							}
							else if (key == 'pow'){
								functions='<label style="color:#6DA63C"><input type="checkbox" id="checkbox_'+_i+'_pow"> Power (' + Math.round(data[key]['r2'] * 100) / 100 + ')</label><br/>';
								$('#functions_' + _i).append(functions);
								data[key]['type']='pow';
								(function(_data){$('#checkbox_'+_i+'_pow').click(function(){update_data_export_option(_i, "pow", _data)});})(data[key]);
							}
							else if (key == 'quad'){
								functions='<label style="color:#458C8C"><input type="checkbox" id="checkbox_'+_i+'_quad"> Quadratic (' + Math.round(data[key]['r2'] * 100) / 100 + ')</label><br/>';
								$('#functions_' + _i).append(functions);
								data[key]['type']='quad';
								(function(_data){$('#checkbox_'+_i+'_quad').click(function(){update_data_export_option(_i, "quad", _data)});})(data[key]);
							}
							else if (key == 'lin'){
								functions='<label style="color:#D9B504"><input type="checkbox" id="checkbox_'+_i+'_lin"> Linear (' + Math.round(data[key]['r2'] * 100) / 100 + ')</label><br/>';
								$('#functions_' + _i).append(functions);
								data[key]['type']='lin';
								(function(_data){$('#checkbox_'+_i+'_lin').click(function(){update_data_export_option(_i, "lin", _data)});})(data[key]);
							}

						}

					})
				});
			}
			else
			{
				if(points.length == 0 && assess_session.attributes[i].checked)
				$('#charts_' + _i).append("Please answer questionnaire");
				else if(!assess_session.attributes[i].checked)
				$('#charts_' + _i).append("The attribute is inactive");

				$('#functions_' + _i).append('<input type="checkbox" id="checkbox_'+_i+'_0"> Add just the attribute');
				$('#checkbox_'+_i+'_0').click(function(){update_data_export_option(_i, "0", null)});
			}
		})(i);



	}
}

function update_data_export_option(i, type, data)
{
	var checked=$('#checkbox_'+i+'_'+type).is(":checked");

	var myAttributI=null;
	//we verify if we are in data_export_option
	for(var l=0; l<data_export_option['attributes'].length; l++)
	{
		if(data_export_option['attributes'][l].indice==i)
		{
			myAttributI=l;
		}
	}

	if(myAttributI!=null) //we have an attribut
	{
		if(checked)//we are going to add this data in utilities
		data_export_option['attributes'][myAttributI].utilities.push(data);
		else //we are goine to remove this type of utilities
		{
			for(var k=0; k<data_export_option['attributes'][myAttributI].utilities.length; k++)
			{
				if(data_export_option['attributes'][myAttributI].utilities[k].type==type)
				{
					//we remove it because we are unchecked
					data_export_option['attributes'][myAttributI].utilities.splice(k);
				}
			}
			//if we have no utilites we also delete the atrtibute
			if(data_export_option['attributes'][myAttributI].utilities.length==0)
				data_export_option['attributes'].splice(myAttributI);
		}
	}
	else //we are going to add the good one.
	{
		var assess_session = JSON.parse(localStorage.getItem("assess_session"));
		myAttribut=assess_session.attributes[i];
		myAttribut.indice=i;
		if (data!=null)
		myAttribut.utilities=[data];
		else
		myAttribut.utilities=[];
		data_export_option['attributes'].push(myAttribut);
	}

}


function checkbox_multiplicative()
{
	var checked=$('#checkbox_multiplicative').is(":checked");
	if(checked)
	{
		var assess_session = JSON.parse(localStorage.getItem("assess_session"));
		data_export_option['k_calculus'].push(assess_session['k_calculus'][0]);
	}
	else {
		for (var l = 0; l < data_export_option['k_calculus'].length; l++) {
			if (data_export_option['k_calculus'][l].method == "multiplicative") {
				data_export_option['k_calculus'].splice(l);
			}
		}
	}

}

function checkbox_multilinear()
{
	var checked=$('#checkbox_multilinear').is(":checked");
	if(checked)
	{
		var assess_session = JSON.parse(localStorage.getItem("assess_session"));
		data_export_option['k_calculus'].push(assess_session['k_calculus'][1]);
	}
	else {
		for (var l = 0; l < data_export_option['k_calculus'].length; l++) {
			if (data_export_option['k_calculus'][l].method == "multilinear") {
				data_export_option['k_calculus'].splice(l);
			}
		}
	}


}