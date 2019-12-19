<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
	

    <title>ASSESS</title>

    <!-- Bootstrap Core CSS -->
    <link href="{{ get_url('static', path='css/bootstrap.min.css') }}" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="{{ get_url('static', path='css/sb-admin.css') }}" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="{{ get_url('static', path='font-awesome-4.1.0/css/font-awesome.min.css') }}" rel="stylesheet" type="text/css">

	<!-- Favicon -->
	<link href="{{ get_url('static', path='img/favicon.ico') }}" rel="icon"/>
	
	
    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/attributes">ASSESS</a>
            </div>
            <!-- Top Menu Items -->

            <!-- Sidebar Menu Items - These collapse to the responsive navigation menu on small screens -->
            <div class="collapse navbar-collapse navbar-ex1-collapse">
                <ul class="nav navbar-nav side-nav">
                    <li class="import">
                        <a href="{{ get_url('/import') }}"><i class="fa fa-fw fa-download"></i>Import assessment</a>
                    </li>
                    <li class="manage">
                        <a href="{{ get_url('/attributes') }}"><i class="fa fa-fw fa-pencil"></i>Manage attributes</a>
                    </li>
                    <li class="questions">
                        <a href="{{ get_url('/questions') }}"><i class="fa fa-fw fa-user"></i>Utility assessment</a>
                    </li>
                    <li class="k">
                        <a href="{{ get_url('/k_calculus') }}"><i class="fa fa-fw fa-search"></i>Scaling constants</a>
                    </li>
                    <li class="export">
                        <a href="{{ get_url('/export') }}"><i class="fa fa-fw fa-upload"></i>Export assessment</a>
                    </li>
                    <li class="settings">
                        <a href="{{ get_url('/settings') }}"><i class="fa fa-fw fa-cogs"></i>Settings</a>
                    </li>
                    <li class="credits">
                        <a href="{{ get_url('/credits') }}"><i class="fa fa-fw fa-users"></i>Credits</a>
                    </li>
					
				</ul>
			</div>
            <!-- /.navbar-collapse -->
        </nav>

            <div id="page-wrapper">

        <div class="container-fluid">

            <!-- Page Heading -->
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">
                        {{ heading }}
                    </h1>
                </div>
            </div>
            <!-- /.row -->

			
			
