%include('header_init.tpl', heading='Import Excel file')

<div class="alert alert-success" role="alert" id="import_ok" >
  File sucessfully imported
</div>

<div class="alert alert-danger" role="alert" id="import_fail" >
  Error during importation <br/>
  {{data_fail}}
</div>


<form action="/upload" method="post" enctype="multipart/form-data">
  <div class="form-group">
    <label for="exampleInputFile">File input</label>
    <input type="file" name="upload">
    <p class="help-block">Only xlsx files are supporter. Files must have the datas must have the same position as when we export xlsx files (position of attributes, points, ...).</p>
  </div>
  <button type="submit" class="btn btn-default">Submit</button>
</form>



%include('header_end.tpl')

%include('js.tpl')

<script type="text/javascript">
  $(function() {
  $("#import_ok").hide();
  $("#import_fail").hide();

  var success={{success}}
  if(success==true)
  {
    var data='{{!data}}';
    console.log("test");
    console.log(JSON.parse(data));
    $("#import_ok").show();
    localStorage.setItem("assess_session", data);
  }
  else
  {
    $("#import_fail").show();
  }

  });
</script>


</body>

</html>
