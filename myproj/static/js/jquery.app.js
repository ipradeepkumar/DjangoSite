
// common scripts

(function() {
    "use strict";

   // Sidebar toggle

   jQuery('.menu-list > a').click(function() {
      
      var parent = jQuery(this).parent();
      var sub = parent.find('> ul');
      
      if(!jQuery('body').hasClass('sidebar-collapsed')) {
         if(sub.is(':visible')) {
            sub.slideUp(300, function(){
               parent.removeClass('nav-active');
               jQuery('.body-content').css({height: ''});
               adjustMainContentHeight();
            });
         } else {
            visibleSubMenuClose();
            parent.addClass('nav-active');
            sub.slideDown(300, function(){
                adjustMainContentHeight();
            });
         }
      }
      return false;
   });

   function visibleSubMenuClose() {

      jQuery('.menu-list').each(function() {
         var t = jQuery(this);
         if(t.hasClass('nav-active')) {
            t.find('> ul').slideUp(300, function(){
               t.removeClass('nav-active');
            });
         }
      });
   }

   function adjustMainContentHeight() {

      // Adjust main content height
      var docHeight = jQuery(document).height();
      if(docHeight > jQuery('.body-content').height())
         jQuery('.body-content').height(docHeight);
   }

   // add class mouse hover

   jQuery('.side-navigation > li').hover(function(){
      jQuery(this).addClass('nav-hover');
   }, function(){
      jQuery(this).removeClass('nav-hover');
   });

   


   // Toggle Menu

   jQuery('.toggle-btn').click(function(){

      var body = jQuery('body');
      var bodyposition = body.css('position');

      if(bodyposition != 'relative') {

         if(!body.hasClass('sidebar-collapsed')) {
            body.addClass('sidebar-collapsed');
            jQuery('.side-navigation ul').attr('style','');

         } else {
            body.removeClass('sidebar-collapsed chat-view');
            jQuery('.side-navigation li.active ul').css({display: 'block'});

         }
      } else {

         if(body.hasClass('sidebar-open'))
            body.removeClass('sidebar-open');
         else
            body.addClass('sidebar-open');

         adjustMainContentHeight();
      }

       //var owl = $("#news-feed").data("owlCarousel");
       //owl.reinit();

   });





    // right slidebar

    $(function(){
        $.slidebars();
        $('#id_Counters').multiselect(
            {
                includeSelectAllOption: true,
                selectAllText: 'Select all',
                enableFiltering: true,
                enableCaseInsensitiveFiltering: true
            }
        );

        $('#id_Events').multiselect(
            {
                includeSelectAllOption: true,
                selectAllText: 'Select all',
                enableFiltering: true,
                enableCaseInsensitiveFiltering: true
            }
        );
       
       $('#ddlStation').on('change', function(event){
            if (event.target.value != "--Select Station--"){
                $('.form > div').removeClass('hideCss');
                $('#btnSubmit').show();
            }
            else{
                $('.form > div:not(#id_Stations)').addClass('hideCss');
                $('#btnSubmit').hide();
            }
       });
        
        $('#tblTasks').DataTable({
            scrollX: false,
            "autoWidth": true,
            "order": [[6, 'desc']],
            columnDefs:[
                {
                    title: 'Action',
                    target: 0
                },
                {
                    title: 'Station',
                    target: 1
                },
                {
                    title: 'Regression Name',
                    target: 2
                },
                {
                    title: 'Tool',
                    target: 3
                },
                {
                    title: 'Total Iterations',
                    target: 4
                },
                {
                    title: 'Platform',
                    target: 5
                },
                {
                    title: 'Created Date',
                    type: 'date',
                    target: 6
                },
                {
                    title: 'Status',
                    target: 7
                },
                {
                    title: 'Modified Date',
                    target: 8
                },
                {
                    title: 'Error',
                    target: 9
                },
            ],
            'rowCallback': function(row, data, index){
                if(data[7].toUpperCase() == "PENDING"){
                    $(row).find('td:eq(7)').css('background-color', 'orange');
                    $(row).find('td:eq(7)').css('color', 'black');
                }
                if(data[7].toUpperCase() == 'IN-PROGRESS'){
                    $(row).find('td:eq(7)').css('background-color', 'yellow');
                    $(row).find('td:eq(7)').css('color', 'black');
                }
                if(data[7].toUpperCase() == 'COMPLETE' || data[7].toUpperCase() == 'COMPLETED' || data[7].toUpperCase() == 'STARTING'){
                    $(row).find('td:eq(7)').css('color', 'white');
                    $(row).find('td:eq(7)').css('background-color', 'green');
                }
                if(data[7].toUpperCase() == 'ERROR' || data[7].toUpperCase() == 'STOPPING' || data[7].toUpperCase() == 'STOPPED'){
                    $(row).find('td:eq(7)').css('color', 'white');
                    $(row).find('td:eq(7)').css('background-color', 'red');
                }
              }
        });
    });


    $(".notification-scroll").slimScroll({
        height: "240px"
    });

    $(".slimscroll").slimScroll({
       height: 'auto',
         position: 'right',
         size: "7px",
         color: '#98a6ad',
         wheelStep: 13
    });





    // collapsible panel

    $('.panel .tools .t-collapse').click(function () {
        var el = $(this).parents(".panel").children(".panel-body");
        if ($(this).hasClass("fa-chevron-down")) {
            $(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
            el.slideUp(200);
        } else {
            $(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
            el.slideDown(200); }
    });


    // close panel
    $('.panel .tools .t-close').click(function () {
        $(this).parents(".panel").parent().remove();
    });


    // side widget close

    $('.side-w-close').on('click', function(ev) {
        ev.preventDefault();
        $(this).parents('.aside-widget').slideUp();
    });
    $('.info .add-people').on('click', function(ev) {
        ev.preventDefault();
        $(this).parents('.tab-pane').children('.aside-widget').slideDown();

    });


    // refresh panel

    $('.box-refresh').on('click', function(br) {
        br.preventDefault();
        $("<div class='refresh-block'><span class='refresh-loader'><i class='fa fa-spinner fa-spin'></i></span></div>").appendTo($(this).parents('.tools').parents('.panel-heading').parents('.panel'));

        setTimeout(function() {
            $('.refresh-block').remove();
        }, 1000);

    });

    $('.btn-animation').on('click', function(br) {
        //adding animation
        $('.modal .modal-dialog').attr('class', 'modal-dialog  ' + $(this).data("animation") + '  animated');
    });


    $(function () {
        $('[data-toggle="popover"]').popover()
    })

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })



    // tool tips

    $('.tooltips').tooltip();

    // popovers

    $('.popovers').popover();


})(jQuery);

//portlets
!function($) {
    "use strict";

    /**
    Portlet Widget
    */
    var Portlet = function() {
        this.$body = $("body"),
        this.$portletIdentifier = ".portlet",
        this.$portletRefresher = '.portlet a[data-toggle="reload"]'
    };

    //on init
    Portlet.prototype.init = function() {
        // Panel closest
        var $this = this;

        // Panel Reload
        $(document).on("click",this.$portletRefresher, function (ev) {
            ev.preventDefault();
            var $portlet = $(this).closest($this.$portletIdentifier);
            // This is just a simulation, nothing is going to be reloaded
            $portlet.append('<div class="panel-disabled"><div class="loader-1"></div></div>');
            var $pd = $portlet.find('.panel-disabled');
            setTimeout(function () {
                $pd.fadeOut('fast', function () {
                    $pd.remove();
                });
            }, 500 + 300 * (Math.random() * 5));
        });
    },
    //
    $.Portlet = new Portlet, $.Portlet.Constructor = Portlet

}(window.jQuery),

/**
 * Components
 */
function($) {
    "use strict";

    var Components = function() {};
    //initilizing
    Components.prototype.init = function() {
        var $this = this;
        //creating portles
        $.Portlet.init();
    },

    $.Components = new Components, $.Components.Constructor = Components

}(window.jQuery),
    //initializing main application module
function($) {
    "use strict";
    $.Components.init();
}(window.jQuery);

function showDetail(id) {
    $.ajax({  
        type: "GET",  
        url: "api/getjobjson/" + id,  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            let jsonObj = JSON.parse(data);
            $('#jsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
            $('#jobJson').modal('show'); 
        }, //End of AJAX Success function  
        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    });   
}

function showIterationDetail(iterationID, taskID) {
    $.ajax({  
        type: "GET",  
        url: "api/getiterationjson/" + iterationID + "/" + taskID,  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            //let jsonObj = JSON.parse(data);
            //$('#iterationjsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
            $('#iterationjsonData')[0].innerHTML = JSON.stringify(data, null, 2);
            $('#iterationJson').modal('show'); 
        }, //End of AJAX Success function  
        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    });   
}


function showIterationDetail(seletObj) {
    if (seletObj.value === '') return;
    iterationID = seletObj.value.split('^')[0];
    taskID = seletObj.value.split('^')[1];
    $.ajax({  
        type: "GET",  
        url: "api/getiterationjson/" + iterationID + "/" + taskID,  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            //let jsonObj = JSON.parse(data);
            //$('#iterationjsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
            $('#iterationjsonData')[0].innerHTML = JSON.stringify(data, null, 2);
            $('#iterationJson').modal('show'); 
        }, //End of AJAX Success function  
        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    });   
}


function refreshJobList(){
    location.reload();
}

function startProcess(GUID, uExecution, eExecution, status) {
    if (confirm('Are you sure, you want to start the process?')){
        if (GUID === '') return;
        
        $.ajax({  
            type: "GET",  
            url: "startprocess/" + GUID + "/" + uExecution + "/" + eExecution,  
            contentType: "application/json; charset=utf-8",  
            dataType: "json",  
            success: function (data) {  
                if (data.responseText == 'success'){
                    console.log('success');
                }
                else{
                    console.log(data.responseText);
                }
            }, //End of AJAX Success function  
            failure: function (data) { 
            }, //End of AJAX failure function  
            error: function (data) {  

            } //End of AJAX error function  

        }).always(function(xhr, status, error){
            refreshJobList();
        });
    }
    else{
        return;
    } 
}




