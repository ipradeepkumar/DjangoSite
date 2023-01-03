
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
        $('#txtFromDate').datepicker();
        $('#txtToDate').datepicker();
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
            var val = event.target.value;
            if (val.split('^')[0] != "--Select Station--"){
                $('.form > div').removeClass('hideCss');
                $('#btnSubmit').show();

                $('#spnPlatform').html(val.split('^')[0]);
                setEmonEventCounters();
            }
            else{
                $('.form > div:not(#id_Stations)').addClass('hideCss');
                $('#btnSubmit').hide();
            }

       });
   
       $('#tblTasks thead tr:first')
       .before('<tr><th>Filters:</th><th></th><th id="thUser">User</th><th id="thSystem_Under_Test">System Under Test</th><th><p></p></th><th id="thTool">Tool</th><th><p></p></th><th id="thPlatform">Platform</th><th><p></p></th><th id="thStatus">Status</th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th></tr>');
        
       var tasksTable = $('#tblTasks').DataTable({
            scrollX: false,
            "autoWidth": true,
            "order": [[8, 'desc']],
            columnDefs:[
                {
                    title: '<input type=\'checkbox\' id=\'chkSelectAll\' class=\'chkall\' />',
                    target: 0,
                    orderable: false
                },
                {
                    title: 'Action',
                    target: 1,
                    orderable: false
                },
                {
                    title: 'User',
                    target: 2
                },
                {
                    title: 'System Under Test',
                    target: 3
                },
                {
                    title: 'Regression Name',
                    target: 4
                },
                {
                    title: 'Tool',
                    target: 5
                },
                {
                    title: 'Total Iterations',
                    target: 6
                },
                {
                    title: 'Platform',
                    target: 7
                },
                {
                    title: 'Created Date',
                    target: 8
                },
                {
                    title: 'Status',
                    target: 9
                },
                {
                    title: 'Modified Date',
                    target: 10
                },
                {
                    title: 'Eowyn Execution Status',
                    target: 11
                },
            ],
            'rowCallback': function(row, data, index){
                if(data[9].toUpperCase() == "PENDING"){
                    $(row).find('td:eq(9)').css('background-color', 'orange');
                    $(row).find('td:eq(9)').css('color', 'black');
                }
                if(data[9].toUpperCase() == 'IN-PROGRESS'){
                    $(row).find('td:eq(9)').css('background-color', 'yellow');
                    $(row).find('td:eq(9)').css('color', 'black');
                }
                if(data[9].toUpperCase() == 'COMPLETE' || data[9].toUpperCase() == 'COMPLETED' || data[9].toUpperCase() == 'STARTING'){
                    $(row).find('td:eq(9)').css('color', 'white');
                    $(row).find('td:eq(9)').css('background-color', 'green');
                }
                if(data[9].toUpperCase() == 'ERROR' || data[9].toUpperCase() == 'STOPPING' || data[9].toUpperCase() == 'STOPPED'){
                    $(row).find('td:eq(9)').css('color', 'white');
                    $(row).find('td:eq(9)').css('background-color', 'red');
                }
              },
              initComplete: function () {
                this.api()
                    .columns()
                    .every(function () {
                        var column = this;
                        if ($(column.header()).html() == 'System Under Test' || $(column.header()).html() == 'Tool' || 
                                        $(column.header()).html() == 'Platform' || $(column.header()).html() == 'Status' || $(column.header()).html() == 'User'){
                         
                        var select = $('<select style="border-radius:5px;border:1px solid #ced4da" data-size="3"><option value="">--Select All--</option></select>')
                        .appendTo($('#tblTasks #th' + $(column.header()).html().replaceAll(' ','_')).empty())
                        .on('change', function () {
                            var val = $.fn.dataTable.util.escapeRegex($(this).val());
                            column.search(val ? '^' + val + '$' : '', true, false).draw();
                            
                        });
                        if ($(column.header()).html() == 'User'){
                            var users = $('#users').html().trim().split(',');
                            var loggedinUser = $('#loggedInUser').html();
                            for(var i=0; i < users.length; i++){
                                if (users[i].trim() != '' )
                                    select.append('<option value="' + users[i].trim() + '"' + (loggedinUser == users[i].trim() ?  'selected' : '') +'>' + users[i].trim() + '</option>');
                            }
                            column.search('^' + loggedinUser + '$', true, false).draw();
                        }
                        else{
                            column
                                .data()
                                .unique()
                                .sort()
                                .each(function (d, j) {
                                        if (d != '')
                                            select.append('<option value="' + d + '">' + d + '</option>');
                                });

                            }
                        
                        }
                    });
                    //$("#thUser select option[value='']").remove();
                    $('#thUser select').selectpicker({
                        liveSearch: true,
                        maxOptions: 3,
                        liveSearchStyle: 'contains'
                    });
                    $('#thSystem_Under_Test select').selectpicker({
                        liveSearch: true,
                        maxOptions: 3,
                        liveSearchStyle: 'contains'
                    });
                    $('#thTool select').selectpicker({
                        liveSearch: true,
                        maxOptions: 3,
                        liveSearchStyle: 'contains'
                    });
                    $('#thPlatform select').selectpicker({
                        liveSearch: true,
                        maxOptions: 3,
                        liveSearchStyle: 'contains'
                    });
                    $('#thStatus select').selectpicker({
                        liveSearch: true,
                        maxOptions: 3,
                        liveSearchStyle: 'contains'
                    });
            }
        });

        tasksTable.order([8, 'desc']).draw();

        $('#btnClear').on('click', function(){
            $('#thUser select').val('').selectpicker('refresh');
            $('#thSystem_Under_Test select').val('').selectpicker('refresh');
            $('#thTool select').val('').selectpicker('refresh');
            $('#thStatus select').val('').selectpicker('refresh');
            $('#thPlatform select').val('').selectpicker('refresh');
            $('#thUser select').trigger('change');
            $('#thSystem_Under_Test select').trigger('change');
            $('#thTool select').val('').trigger('change');
            $('#thStatus select').val('').trigger('change');
            $('#thPlatform select').val('').trigger('change');
            $('#txtFromDate').val('');
            $('#txtToDate').val('');
            tasksTable.draw();
            $('#tblTasks_filter').find("input")[0].value = '';
            $('#tblTasks input:checkbox').prop('checked', false);

            
        });

        $('#chkSelectAll').on('click', function(){
            if (this.checked){
                $('#tblTasks input:checkbox').prop('checked', true);
            }
            else{
                $('#tblTasks input:checkbox').prop('checked', false);
            }
        });

        $('.chk').on('click', function(){
            if ($('#tblTasks input:checked').length - 1 == $('#tblTasks input:checkbox').length - 1){
                $('#chkSelectAll').prop('checked', true);
            }
            else{
                $('#chkSelectAll').prop('checked', false);
            }

            if ($('.chk:checkbox:checked').length == $('#tblTasks .chk').length)
                $('#chkSelectAll').prop('checked', true);



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
    if (confirm('Are you sure, you want to ' +  status +' the process?')){
        if (GUID === '') return;
        
        $.ajax({  
            type: "GET",  
            url: "startprocess/" + GUID + "/" + uExecution + "/" + eExecution,  
            contentType: "application/json; charset=utf-8",  
            dataType: "json",  
            success: function (data) {  
                location.reload();
                if (data.responseText == 'success'){
                    console.log('success');
                }
                else if(data.status == '404'){
                    alert(data.responseText);
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


function setEmonEventCounters(){
    $.ajax({  
        type: "GET",  
        url: "/api/event/" + 'cpx',//$('#ddlStation').find(":selected").val(),  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            //isPlatformChanged = true;
            $('#ddlEmonEvents').find('option').remove();
            emonEvents = data;
            $.each(emonEvents, function(key, item){
                $('#ddlEmonEvents')
                            .append($("<option></option>")
                            .attr("value", item.fields['EmonEventID'])
                            .text(item.fields['Name']));  
                });
                $('#ddlEmonEvents').multiselect(
                    {
                        maxHeight: 200,
                        includeSelectAllOption: true,
                        selectAllText: 'Select all',
                        enableFiltering: true,
                        enableCaseInsensitiveFiltering: true,
                        onChange: function(element, checked){
                            console.log(element.val());
                            if (checked)
                                $("#ddlEmonEvents").multiselect('select', element.val());
                            else
                                $("#ddlEmonEvents").multiselect('deselect', element.val());
                            setEmonCounters($("#ddlEmonEvents").val());
                            return false;
                        },
                        onSelectAll: function(){
                            setEmonCounters($("#ddlEmonEvents").val());
                        },
                        onDeselectAll: function(){
                            setEmonCounters($("#ddlEmonEvents").val());
                        },
            
                    }
                );
                $('#ddlEmonEvents').multiselect('rebuild');
                setEmonCounters();
                BuildEmonCounter();
        }, //End of AJAX Success function  
        failure: function (data) {  
            console.log(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            console.log(data.responseText);  
        }
    }); 
}

function deleteRecord(){
    var checkBoxes = $('#tblTasks').find('input[type="checkbox"]:checked');
    if(checkBoxes.length == 0){
        alert('Please select a row to delete.');
        return;
    }
    if (confirm('Are you sure, you want to delete?')){
        guids = [];
        for(i = 0; i < checkBoxes.length; i++){
            guids.push(checkBoxes[i].value);
        }

            $.ajax({  
                type: "POST",  
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                url: "deleteTask/" + guids,  
                contentType: "application/json; charset=utf-8",  
                data: {'guids': guids},
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
}

function filterData(){
   var fromDate = $('#txtFromDate').val();
   var toDate = $('#txtToDate').val();
    if(fromDate == '' && toDate == ''){
        alert('Please enter either from date or to date to filter.');
        return;
    }
            $.ajax({  
                type: "POST",  
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                url: "filterData/",  
                contentType: "application/json; charset=utf-8",  
                data: {'fromDate': guids, 'toDate': toDate},
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

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

