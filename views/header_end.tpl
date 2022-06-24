                </div>
                <!-- /.container-fluid -->
                    <div class="container" style="margin-top:100px;">
                    <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
                        <div class="col-md-4 d-flex align-items-center">
                        <span class="text-muted">&copy; 2022 ASSESS, Inc</span>
                        </div>

                    </footer>
                    </div>

            </div>
            <!-- /#page-wrapper -->
            
            
    </div>
    <!-- /#Content -->

</div>

<div class="b-example-divider"></div>



<!-- /#wrapper -->
<!-- jQuery CDN -->
         <script src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
         <!-- Bootstrap Js CDN -->
         <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

         <script type="text/javascript">
             $(document).ready(function () {
                 $('#sidebarCollapse').on('click', function () {
                     $('#sidebar, #content').toggleClass('active');
                     $(this).toggleClass('active');
                     $('.collapse.in').toggleClass('in');
                     $('a[aria-expanded=true]').attr('aria-expanded', 'false');
                 });
                 $("#sidebar").mCustomScrollbar({
                    theme: "minimal"
                });
             });

         </script>

         <!-- jQuery Custom Scroller CDN -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.concat.min.js"></script>
