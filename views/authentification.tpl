%include('header_init.tpl', heading='Authentification')


<div class="alert alert-danger" role="alert" id="info" >
      Bad password !
</div>

<div class="alert alert-success" role="alert" id="success" >
      Welcome to Assess2
</div>

<div class="alert alert-success" role="alert" id="success_admin" >
      Welcome to Assess2 password administration panel
</div>


<div class="form-inline">
  <div class="form-group">
    <input type="text" class="form-control" id="password" placeholder="Password">
  </div>
  <button id="connect" class="btn btn-outline-dark">Connect</button>


</div>
<br/><br/>
<div class="alert alert-info" role="alert" id="info_admin" >
      Let the input box blank in order to delete the password
</div>

<div id="admin" >
   <div class="col-sm-5">
    <div id="admin_mdps">

    </div>
    <br/>
    <button id="add" class="btn btn-outline-dark"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>Add password</button>
    <br/><br/>
    <button id="save" class="btn btn-outline-dark">Save</button>
    <br/><br/>
    <div class="alert alert-success" role="alert" id="success_save" >
          Passwords have been saved !
    </div>
    <div class="alert alert-danger" role="alert" id="fail_save" >
              Passwords have not been saved ! You are not administrator. Please check your password !
        </div>
   </div>


</div>



%include('header_end.tpl')

%include('js.tpl')


<script>

$(function(){
$("#info").hide();
$("#info_admin").hide();
$("#success").hide();
$("#success_save").hide();
$("#success_admin").hide();
$("#admin").hide();
$("#fail_save").hide();

$("#connect").click(function(){
    $.post('auth', JSON.stringify({"type":"authentification","mdp":$("#password").val()}), function (data) {
        retour(data);
    });
});

$("#password").keypress(function(event){
	if (event.which == 13) {
		$.post('auth', JSON.stringify({"type":"authentification","mdp":$("#password").val()}), function (data) {
			retour(data);
		});
	};
});

var mdps=[];
function retour(data)
{
    $("#admin_mdps").html("")
        if(data.success=="admin")
        {
            $("#success_admin").fadeIn(500);
            $("#info_admin").fadeIn(500);
            $("#admin").show(400);
            mdps=data.mdp;
            for(var i=0; i<data.mdp.length; i++)
            {
            $("#admin_mdps").append('<br/><input type="text" class="form-control" id="mdp'+i+'" placeholder="blank - this passwd will be deleted" value="'+data.mdp[i]+'">');
            }
        }
        else if(data.success)
        {
            $("#success").fadeIn(500);
            setTimeout(function(){location.reload();}, 1500);

        }
        else
        {
            $("#info").show(200);
        }
}

$("#save").click(function(){
    //we update the list
    for(var i=0; i<mdps.length; i++)
    {
        mdps[i]=$("#mdp"+i).val()
    }
    //now we can delete those who are empty
    for(var i=0; i<mdps.length; i++)
    {
        if(mdps[i]=="")
        {
            mdps.splice(i,1);
        }
    }

   $.post('auth', JSON.stringify({"type":"admin","mdp":$("#password").val(), "newmdp":mdps}), function (data) {
           if(data.success)
           {
                $("#success_save").show(300);
                $.post('auth', JSON.stringify({"type":"words","mdp":$("#password").val()}), function (data) {
                        retour(data);
                    });
           }
           else
           {
                $("#fail_save").show(300);
           }
       });
});

$("#add").click(function(){
    $("#admin_mdps").html("")
    mdps.push("new passwd");
    for(var i=0; i<mdps.length; i++)
    {
        $("#admin_mdps").append('<br/><input type="text" class="form-control" id="mdp'+i+'" placeholder="blank - this password will be deleted" value="'+mdps[i]+'">');
    }
});


});


</script>


</body>

</html>
