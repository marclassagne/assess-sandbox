%include('header_init.tpl', heading='Export Excel file')

<div class="page-header">
    <h3>export all</h3>
</div>

<button type="button" class="btn btn-default" id="export_xls">Click to export Excel</button><br/>

<div class="page-header">
    <h3>Choose your exportation in detail</h3>
</div>

<h4>Choose a specific utility function for each attribute </h4>
<div id="attribute" >
    <table class="table">
    <thead>
    <tr>
    <th>Attribute</th>
    <th>Unit</th>
    <th>Graph</th>
    <th>Function</th>
    </tr>
    </thead>
    <tbody id="table_attributes">
    </tbody>
    </table>
</div>
<button type="button" class="btn btn-default" id="generate_list">Generate the list</button><br/>


<br/>
<h4>Choose K</h4>

<label><input type="checkbox" id="checkbox_multilinear"> Multilinear utility function </label><br/>
<label><input type="checkbox" id="checkbox_multiplicative"> Multiplicative utility function </label><br/>
<br/>
<button type="button" class="btn btn-default" id="export_xls_option">Click to export to Excel</button><br/>


%include('header_end.tpl')
%include('js.tpl')
<script src="{{ get_url('static', path='js/export.js') }}"></script>>






</body>


</html>
