var platformData;
$(function(){
    $('#id_EmonEvents').hide();
    $('#ddlEmonEvents').hide();
    $('#id_EmonCounters').hide();
    $('#ddlEmonCounters').hide();
    //ajax call for fetching stations
    $.ajax({  
        type: "GET",  
        url: "/api/stations",  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            $.each(data, function (key, item) {  
                $('#ddlStation')
                    .append($("<option></option>")
                    .attr("value", item.StationID)
                    .text(item.Name)); 
            }); //End of foreach Loop   
        }, //End of AJAX Success function  

        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    });   
    //ajax call for fetching tools
    $.ajax({  
        type: "GET",  
        url: "/api/tools",  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            $.each(data, function (key, item) { 
                $('#ddlToolName')
                    .append($("<option></option>")
                    .attr("value", item.ToolID)
                    .text(item.Name));  
               
            }); //End of foreach Loop   
            $('#ddlToolName').multiselect(
                {
                    includeSelectAllOption: true,
                    selectAllText: 'Select all',
                    enableFiltering: true,
                    enableCaseInsensitiveFiltering: true,
                }
            );
            $('#ddlToolName').multiselect('rebuild');
        }, //End of AJAX Success function  

        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    }); 

    //ajax call for fetching platforms
    $.ajax({  
        type: "GET",  
        url: "/api/platforms",  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            $.each(data, function (key, item) { 
                $('#ddlPlatform')
                    .append($("<option></option>")
                    .attr("value", item.PlatformID)
                    .text(item.Name));  
               
            }); //End of foreach Loop   
        }, //End of AJAX Success function  
        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    }); 
    isPlatformChanged = false;
   
    $('#ddlPlatform').on('change', function(e){
       
        if (!isPlatformChanged){
            $.ajax({  
                type: "GET",  
                url: "/api/platforms",  
                contentType: "application/json; charset=utf-8",  
                dataType: "json",  
                success: function (data) {  
                    isPlatformChanged = true;
                    SetEmonEvents(data);
                }, //End of AJAX Success function  
                failure: function (data) {  
                    alert(data.responseText);  
                }, //End of AJAX failure function  
                error: function (data) {  
                    alert(data.responseText);  
                }
            }); 
        }
        else
            SetEmonEvents(platformData);

    });
    
    $('#chkEmon').on('change', function(e){
        if (e.target.checked)
        {
            $('#id_EmonEvents').show();
            $('#ddlEmonEvents').show();
            $('#id_EmonCounters').show();
            $('#ddlEmonCounters').show();
            SetEmonEvents(platformData);
        }
        else
        {
            $('#id_EmonEvents').hide();
            $('#ddlEmonEvents').hide();
            $('#id_EmonCounters').hide();
            $('#ddlEmonCounters').hide();
        }
    });
    $('.btn').on('click', function(){
        alert('Hi');
    });
    
    
});

function SetEmonEvents(result){
    selectedOptions = $('#ddlPlatform').find(":selected").val();
    if (platformData == undefined)
        platformData = result;
    if ($('#chkEmon').attr('checked') === 'checked'){
    $.each(platformData, function(key, item){
        if (item.PlatformID == selectedOptions){
            $('#ddlEmonEvents').find('option').remove();
            emonEvents = item.emonevents
            $.each(emonEvents, function(key, item){
                $('#ddlEmonEvents')
                            .append($("<option></option>")
                            .attr("value", item.EmonEventID)
                            .text(item.Name));  
                });
    }
    });
    $('#ddlEmonEvents').multiselect(
        {
            includeSelectAllOption: true,
            selectAllText: 'Select all',
            enableFiltering: true,
            enableCaseInsensitiveFiltering: true,
        }
    );
    $('#ddlEmonEvents').multiselect('rebuild');
    }
}




