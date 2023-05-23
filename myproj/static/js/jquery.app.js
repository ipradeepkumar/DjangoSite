
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
                setEmonEventCounters(val.split('^')[1]);
                setToolNames(val.split('^')[1]);
            }
            else{
                $('.form > div:not(#id_Stations)').addClass('hideCss');
                $('#btnSubmit').hide();
            }

       });

       $('#ddlToolName').on('change', function(event){
            var val = event.target.value;
            if (val == "") { $('#lnkPlaceHolder').html(''); return;}
            $.ajax({  
                type: "GET",  
                url: "/api/toolJson/" + val,  
                contentType: "application/json; charset=utf-8",  
                dataType: "json",  
                success: function (data) {  
                    $('#ToolName').val(val);
                    $('#StationName').val(data[0].fields.StationName);
                    $('#lnkPlaceHolder').html('<span style="text-decoration:underline;cursor:pointer;color:blue" onclick="showToolJsonData(\'' + btoa(data[0].fields.JsonFile) + '\')" >Tool Json</span>');
                }, //End of AJAX Success function  
                failure: function (data) {  
                    console.log(data.responseText);  
                }, //End of AJAX failure function  
                error: function (data) {  
                    console.log(data.responseText);  
                }
            });
     });
     $('#btnFilter').on('click',function(){
        let fromDate = $('#txtFromDate').val();
        let toDate = $('#txtToDate').val();
        if(fromDate == '' && toDate == ''){
            alert('Please enter either from date or to date to filter.');
            return;
        }
        else if (toDate == ''){
            toDate = fromDate;
        }
        else if (fromDate == '')
        {
            fromDate = toDate;
        }
        tasksTableNew.ajax.url('filterDataNew/' + fromDate.replace(/\//g,'-') + '/' + toDate.replace(/\//g,'-')).load(function(e){
            console.log(e);
        }, false);
     });
     $('#btnDelete').on('click',function(){
        let guids = [];
        var checkBoxes = $('#tblTasksNew').find('input[type="checkbox"]:checked');
        if(checkBoxes.length == 0){
            alert('Please select a row to delete.');
            return;
        }
        if (confirm('Are you sure, you want to delete?')){
            
            for(let i = 0; i < checkBoxes.length; i++){
                if (checkBoxes[i].value != 'on')
                    guids.push(checkBoxes[i].value);
            }
            
            tasksTableNew.ajax.url('deleteTaskNew/' + guids).load(function(e){
                    console.log(e);
                }, false);
        }
     });
     /*******************************************************************************************************************/
     $('#tblTasksNew thead tr:first')
       .before('<tr><th>Filters:</th><th></th><th id="thUser">User</th><th id="thSystem_Under_Test">System Under Test</th><th><p></p></th><th id="thTool">Tool</th><th><p></p></th><th id="thPlatform">Platform</th><th><p></p></th><th id="thStatus">Status</th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th><th><p></p></th></tr>');
        
       var tasksTableNew = $('#tblTasksNew').DataTable({
            scrollX: false,
            processing: false,
            ajax: {
                url: 'jobhistorynew',
            },
            "autoWidth": true,
            "order": [[8, 'desc']],
            columns:[
                {   data: 'TaskID', 
                    render: function(data, type, row, meta){
                        if (row.Status == 'COMPLETE' || row.Status == 'COMPLETED' || row.Status == 'ERROR' || row.Status == 'PENDING' || row.Status == 'STOPPED')
                            return "<input type='checkbox' value='" + row.GUID +"' class='chknew'></input>"
                        else
                            return "";
                    }
                },
                { data: 'TaskID',
                  render: function(data, type, row, meta){

                    if (row.Status == 'COMPLETE' || row.Status == 'COMPLETED' || row.Status == 'ERROR' || row.Status == 'PENDING' || row.Status == 'STOPPED')
                        return "<a href='#' onclick=\"startProcess('" + row.GUID + "', 1, 1, 'start')\" class='ti-control-play'>&nbsp;Start</a>";
                    else if (row.Status == 'IN-PROGRESS')
                        return "<a href='#' onclick=\"startProcess('" + row.GUID + "', 0, 1, 'stop')\" class='ti-control-stop'>&nbsp;Stop</a>";
                    else if (row.Status == 'STARTING')
                        return "<span style='font-weight:bold;color:green'>Starting...</span>";
                    else if(row.Status == 'STOPPING')
                            return "<span style='font-weight:bold;color:red'>Stopping...</span>";
                  }
                },
                { data: 'CreatedBy'
                },
                { data: 'Station'
                },
                { data: 'RegressionName',
                  render: function(data, type, row, meta){
                    return "<a href='#' onclick='showDetail(" + row.TaskID + ")'><p style='text-decoration:underline'>" + row.RegressionName + "</p></a>";
                  }
                },
                { data: 'Tool'
                },
                { data: 'TotalIterations',
                  render:function(data, type, row, meta){
                    return "<span>" + row.CurrentIteration + " / " + row.TotalIterations + "</span>";
                  }
                },
                { data: 'Platform'
                },
                { data: 'CreatedDate'
                },
                { data: 'Status'
                },
                { data: 'ModifiedDate'
                },
                { data: 'ErrorCode'
                },
                { data: 'IterationResult',
                  render: function(data, type, row, meta){
                    let optionStr = '';
                    $.each(row.TaskIterations, function(index, value){
                        if (value.GUID == row.GUID){
                            optionStr += "<option value='" + value.Iteration + "^" + value.TaskID +"'>" + value.Iteration + "</option>";
                        }
                    });
                    return "<select class='form-control sm-2 w-75' style='font-size:14px;' name='iteration' id='iteration' onchange='showIterationDetail(this)>" +
                                    "<option value=''></option>" +
                                   optionStr 
                            "</select>";
                  }
                },
                { data: 'IterationResult'
                },
                { data: 'TestResults'
                },
                { data: 'AxonLog'
                },
                { data: 'AzureLink'
                }
            ],
            columnDefs:[

            ],
            'rowCallback': function(row, data, index){
                if(data.Status.toUpperCase() == "PENDING"){
                    $(row).find('td:eq(9)').css('background-color', 'orange');
                    $(row).find('td:eq(9)').css('color', 'black');
                }
                if(data.Status.toUpperCase() == 'IN-PROGRESS'){
                    $(row).find('td:eq(9)').css('background-color', 'yellow');
                    $(row).find('td:eq(9)').css('color', 'black');
                }
                if(data.Status.toUpperCase() == 'COMPLETE' || data.Status.toUpperCase() == 'COMPLETED' || data.Status.toUpperCase() == 'STARTING'){
                    $(row).find('td:eq(9)').css('color', 'white');
                    $(row).find('td:eq(9)').css('background-color', 'green');
                }
                if(data.Status.toUpperCase() == 'ERROR' || data.Status.toUpperCase() == 'STOPPING' || data.Status.toUpperCase() == 'STOPPED'){
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
                        .appendTo($('#tblTasksNew #th' + $(column.header()).html().replaceAll(' ','_')).empty())
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

       

        tasksTableNew.on( 'xhr', function () {
            var json = tasksTableNew.ajax.json();
            tasksTableNew.order([8, 'desc']).draw();
            console.log( json );
        } );

        $('#refreshGrid').on('click', function(){
            tasksTableNew.ajax.reload();
        });

        $('#tblTasksNew,.chknew').on('click',function(){
            if ($('#tblTasksNew input:checked').length - 1 == $('#tblTasksNew input:checkbox').length - 1){
                $('#chkSelectAllNew').prop('checked', true);
            }
            else{
                $('#chkSelectAllNew').prop('checked', false);
            }

            if ($('.chknew:checkbox:checked').length == $('#tblTasksNew .chknew').length)
                $('#chkSelectAllNew').prop('checked', true);

            });

            $('#chkSelectAllNew').on('click', function(){
                if (this.checked){
                    $('#tblTasksNew input:checkbox').prop('checked', true);
                }
                else{
                    $('#tblTasksNew input:checkbox').prop('checked', false);
                }
            });
     /*******************************************************************************************************************/
   
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
            tasksTableNew.draw();
            if ($('#tblTasks').length){
                $('#tblTasks_filter').find("input")[0].value = '';
                if($('#tblTasks input:checkbox').length > 0)
                    $('#tblTasks input:checkbox').prop('checked', false);
            }

            if ($('#tblTasksNew').length){
                $('#tblTasksNew_filter').find("input")[0].value = '';
                if($('#tblTasksNew input:checkbox').length > 0)
                    $('#tblTasksNew input:checkbox').prop('checked', false);
            }


            
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
            jsonObj[0].fields.ToolJson = '<span style=\'color:blue;cursor:pointer\' onclick=showJobHistoryToolJson(\'' + btoa(jsonObj[0].fields.ToolJson) + '\')>User Tool Json</span>'; //JSON.parse(jsonObj[0].fields.ToolJson);
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

function showTestResult(taskId) {
    //let jsonObj = JSON.parse(str);
    //$('#jsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
    $('#jsonData')[0].innerHTML = JSON.parse(document.getElementById(taskId).textContent);
    $('#jobJson').modal('show'); 
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


function setEmonEventCounters(stationName){
    $.ajax({  
        type: "GET",  
        url: "/api/event/" + stationName,//$('#ddlStation').find(":selected").val(),  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        beforeSend: function(){
            $('#loading').show();
        },
        complete: function(){
            $('#loading').hide();
        },
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

function setToolNames(stationName){
    $.ajax({  
        type: "GET",  
        url: "/api/toolByStation/" + stationName,  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            console.log(data);
            $.each(data, function (key, item) { 
                $('#ddlToolName')
                    .find('option')
                    .remove();
                $('#ddlToolName')
                    .append($("<option></option>")
                    .attr("value", "")
                    .text("-- Select Tool--"));                  
                $('#ddlToolName')
                    .append($("<option></option>")
                    .attr("value", item.fields.Name)
                    .text(item.fields.Name));
            }); 
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
            if (checkBoxes[i].value != 'on')
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

function sendJson() {
    $.ajax({  
        type: "POST",  
        url: "SendJson",  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        data: $('#jsonData').innerHTML,
        success: function (data) {
           alert('Task data posted to API');
        }, //End of AJAX Success function  
        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    });   
}

function showJson() {
    $.ajax({  
        type: "GET",  
        url: "ShowJson",  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {
            let jsonObj = JSON.stringify(data);
            let jsonPretty = JSON.parse(jsonObj);
            //$('#jsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
            $('#jsonData')[0].innerHTML = JSON.stringify(jsonPretty, null, '\t');
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

function showJobHistoryToolJson(jsonString){
    let jsonObj = atob(jsonString);
    let jsonPretty = JSON.parse(jsonObj);
    //$('#jsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
    $('#toolData')[0].innerHTML = JSON.stringify(jsonPretty, null, '\t');
    $('#toolJson').modal('show'); 
}

function showToolJsonData(jsonData) {
    if (jsonData === "") { alert('No json data found'); }
    let jsonObj = atob(jsonData);
    let jsonPretty = JSON.parse(jsonObj);
    //$('#jsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
    $('#toolData')[0].innerHTML = JSON.stringify(jsonPretty, null, '\t');
    $('#toolJson').modal('show'); 
}


function showToolJson(fileName) {
    $.ajax({  
        type: "GET",  
        url: "ShowToolJson/" + fileName,  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {
            let jsonObj = JSON.stringify(data);
            let jsonPretty = JSON.parse(jsonObj);
            //$('#jsonData')[0].innerHTML = JSON.stringify(jsonObj[0].fields, null, 2);
            $('#toolData')[0].innerHTML = JSON.stringify(jsonPretty, null, '\t');
            $('#toolJson').modal('show'); 
        }, //End of AJAX Success function  
        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    });   
}

function saveToolJson(){
    $('#ToolJson').text($('#toolData').val());
    $('#toolJson').modal('toggle');

    $.ajax({  
        type: "POST",  
        url: "SaveToolJson",  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        data: JSON.stringify({'ToolData': $('#toolData').val(), 'ToolName': $('#ToolName').val()}),
        success: function (data) {
          
        }, //End of AJAX Success function  
        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    }); 

   
}

function validateJSON(){
    jsonStr = $('#toolData').val();
    try {
        var c = $.parseJSON(jsonStr);
        $('#validJsonNotify').css('color','green');
        $('#validJsonNotify').html('Valid JSON');
        setTimeout(function(){
            $('#validJsonNotify').html('');
        }, 3000)
      }
      catch (err) {
        $('#validJsonNotify').css('color','red');
        $('#validJsonNotify').html('Invalid JSON. Error: ' + err);
        setTimeout(function(){
            $('#validJsonNotify').html('');
        }, 3000)
      }
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

