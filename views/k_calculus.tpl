%include('header_init.tpl', heading='Scaling constants')

<!---------------------- Alert for minimum number of attributes ---------------------->
<div id="not_enough_attributes" class="alert alert-danger" role="alert">You need at least 2 active attributes to calculate multi-attributes utility function.</div>
<div id="page-content">

	<!---------------------- Scaling K_i coefficients ---------------------->
	<div class="page-header">
	  <h3>Scaling K<sub>i</sub> coefficients</h3>
	</div>

	<div class="alert alert-info" role="alert" id="update_box" >
	  <button type="button" class="btn btn-info" id="update"><span class="glyphicon glyphicon-refresh" aria-hidden="true"></span></button>
	  <span id="update_attributes_number"></span> <span id="update_attributes_plurial">attributes are activated</span> but <span id="update_k_number"></span> <span id="update_k_number_plurial">are</span> used for the computation of the K<sub>i</sub>. You need to refresh the list of the K<sub>i</sub>. All the scaling constants’ values will be reset.
	</div>

	<div id="error_message"></div>
	<div id="message"></div>

	<div id="button_method" style="text-align:center;">
		<button type="button" class="btn btn-default btn-lg" id="button_multiplicative">Multiplicative</button>
		<button type="button" class="btn btn-default btn-lg" id="button_multilinear">Multilinear</button>
	</div>

	<div id="k_list" style="display:none">
		<table class="table">
			<thead>
				<tr>
					<th>K</th>
					<th>Relative Attribute</th>
					<th>Value</th>
					<th><img src="/static/img/delete.ico" style="width:16px;"/></th>
				</tr>
			</thead>
			<tbody id="table_k_attributes"></tbody>
		</table>
	</div>

	<div id="k_calculus_info"></div>
	<div id="trees"></div>
	<br/>

	<!---------------------- K computation ---------------------->
	<div id="K_computation">
		<div class="page-header">
		  <h3>K computation</h3>
		</div>

		<div class="alert alert-info" role="alert" id="calculatek_box_multiplicative" >
		  You need to calculate all k<sub>i</sub> in order to calculate K.
		</div>

		<div class="alert alert-info" role="alert" id="calculatek_box_multilinear" >
		  There is no need to calculate K in multilinear.
		</div>

		<div style="text-align:center;" id="GK">
			<span class="h4">K = <span id="GK_value"></span> </span><button type="button" class="btn btn-default btn-lg" id="button_calculate_k" style="text-align:center">Compute</button>
			<br/>
		</div>
		<br/>
	</div>

	<!---------------------- Choose utility function for each attributes ---------------------->
	<div class="page-header">
	  <h3>Choose utility function for each attributes</h3>
	</div>

	<div id="attribute" >
		<table class="table">
			<thead>
				<tr>
					<th>K</th>
					<th>Attribute</th>
					<th>Graph</th>
					<th>Utility function</th>
				</tr>
			</thead>
			<tbody id="table_attributes"></tbody>
		</table>
	</div>

	<div style="text-align:center;" >
		<button type="button" class="btn btn-default btn-lg" id="button_generate_list" style="text-align:center">Generate graph</button>
		<br/>
	</div>

	<!---------------------- Determine the multi-attribute utility function ---------------------->
	<div class="page-header">
	  <h3>Determine the multi-attribute utility function</h3>
	</div>

	<div style="text-align:center;" id="button_generate_list">
		<button type="button" class="btn btn-default btn-lg" id="button_calculate_utility" style="text-align:center">Compute multi-attribute utility function</button>
		<br/><br/>
		<span id="utility_function"></span>
	</div>
</div>

%include('header_end.tpl')
%include('js.tpl')

<script> var tree_image = '{{ get_url("static", path="img/tree_choice.png") }}'; </script>

<!-- Tree object -->
<script src="{{ get_url('static', path='js/tree.js') }}"></script>
<script src="{{ get_url('static', path='js/clipboard.min.js') }}"></script>
<script src="{{ get_url('static', path='js/k_calculus.js') }}"></script>

<script>
$(function() {
	$('li.k').addClass("active");
	var asses_session = JSON.parse(localStorage.getItem("asses_session"));

	function isInArray(value, array) {
		return array.indexOf(value) > -1;
	}

	//we toggle the button we used
	for(var i=0; i<asses_session.k_calculus.length; i++) {
		if(asses_session.k_calculus[i].active==true) {
			$("#button_"+asses_session.k_calculus[i].method).removeClass('btn-default');
			$("#button_"+asses_session.k_calculus[i].method).addClass('btn-primary');
			update_k_list(i);
			show_list();
		} else {
			$("#button_"+asses_session.k_calculus[i].method).removeClass('btn-primary');
			$("#button_"+asses_session.k_calculus[i].method).addClass('btn-default');
		}
	}
});
</script>

</body>

</html>
