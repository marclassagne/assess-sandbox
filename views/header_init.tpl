<!DOCTYPE html>
<html lang="en">

    %include('js.tpl')

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">

        <title>ASSESS</title>

        <!-- Bootstrap Core CSS -->
        <link href="{{ get_url('static', path='css/bootstrap.min.css') }}" rel="stylesheet">

        <!-- Our Custom CSS -->
        <link href="{{ get_url('static', path='css/style5.css') }}" rel="stylesheet">
        
        <!-- Custom Fonts -->
        <link href="{{ get_url('static', path='font-awesome-4.1.0/css/font-awesome.min.css') }}" rel="stylesheet" type="text/css">

        <!-- Favicon -->
	    <link href="{{ get_url('static', path='img/favicon.ico') }}" rel="icon"/>

        <!-- Scrollbar Custom CSS -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.css">
        

    </head>
    <body>

        <div class="wrapper">
            <!-- Sidebar Holder -->
            <nav id="sidebar">
                <div class="sidebar-header">
                    <a href="{{ get_url('/attributes') }}"><h3>ASSESS</h3></a>
                </div>

                <ul class="list-unstyled components">
                <li class="import">
                        <a href="{{ get_url('/import') }}"><i class="fa fa-fw fa-download"></i>Import assessment</a></li>
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
                    <li class="settings">
                        <a href="{{ get_url('/settings') }}"><i class="fa fa-fw fa-cogs"></i>Settings</a>
                    </li>
                    <li class="credits">
                        <a href="{{ get_url('/credits') }}"><i class="fa fa-fw fa-users"></i>Credits</a>
                    </li>
                </ul>

                <ul class="list-unstyled CTAs">
                    <script src="{{ get_url('static', path='js/export.js') }}"></script>
                    <li class="export"><button type = "button" id='export_xls' class= "button2 btn btn-dark"><i class="fa fa-fw fa-upload "></i>Export all to Excel</button></li>
                </ul>
            </nav>

            <!-- Page Content Holder -->
            <div id="content">

                <nav class="navbar navbar-default">
                    <div class="container-fluid">

                        <div class="navbar-header">
                        
                            <button type="button" id="sidebarCollapse" class="navbar-btn">
                                <span></span>
                                <span></span>
                                <span></span>
                            </button>
                        </div>

                        <!-- Page Heading -->
                        <div class="row navbar-collapse" id="navbarSupportedContent">
                            <div class="col-lg-12">
                                <h1 class="page-header nav-item" style="text-align:center;">
                                    {{ heading }}           
                                </h1>
                            </div>
                        </div>
                        <!-- /.row -->
                    </div>
                </nav>

                <div id="page-wrapper">


                        





            
