var platformData;
$(function(){
    setEmonCounters([0]);
    $('#id_EmonEvents').hide();
    $('#ddlEmonEvents').hide();
    $('#id_EmonCounters').hide();
    $('#ddlEmonCounters').hide();
    $('.multiselect-native-select').hide();
    
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
                    .attr("value", item.Name)
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
                    .attr("value", item.Name)
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
                    .attr("value", item.Name)
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
                    setEmonCounters([0]);
                }, //End of AJAX Success function  
                failure: function (data) {  
                    alert(data.responseText);  
                }, //End of AJAX failure function  
                error: function (data) {  
                    alert(data.responseText);  
                }
            }); 
        }
        else{
            SetEmonEvents(platformData);
            setEmonCounters([0]);
        }
            

    });
    
    $('#chkEmon').on('change', function(e){
        if (e.target.checked)
        {
            $('#id_EmonEvents').show();
            $('#ddlEmonEvents').show();
            $('#id_EmonCounters').show();
            $('#ddlEmonCounters').show();
            $('.multiselect-native-select').show();
            
        }
        else
        {
            $('#id_EmonEvents').hide();
            $('#ddlEmonEvents').hide();
            $('#id_EmonCounters').hide();
            $('#ddlEmonCounters').hide();
            $('.multiselect-native-select').hide();
        }
        SetEmonEvents(platformData);
        setEmonCounters($('#ddlEmonEvents').val());
    });

    //ajax call for fetching stations
    $.ajax({  
        type: "GET",  
        url: "/api/ideas",  
        contentType: "application/json; charset=utf-8",  
        dataType: "json",  
        success: function (data) {  
            $.each(data, function (key, item) {  
                $('#ddlIdea')
                    .append($("<option></option>")
                    .attr("value", item.Name)
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
    
});

function SetEmonEvents(result){
    selectedOptions = $('#ddlPlatform').find(":selected").val();
    if (platformData == undefined)
        platformData = result;
    if ($('#chkEmon').attr('checked') === 'checked'){
    $.each(platformData, function(key, item){
        if (item.Name == selectedOptions){
            $('#ddlEmonEvents').find('option').remove();
            emonEvents = item.emonevents
            $.each(emonEvents, function(key, item){
                $('#ddlEmonEvents')
                            .append($("<option></option>")
                            .attr("value", item.Name)
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
    }
}

function setEmonCounters(selectedArray){
    if (platformData != undefined &&  $('#chkEmon').attr('checked') === 'checked'){
        $('#ddlEmonCounters').find('option').remove();
        $.each(selectedArray, function(index, obj){
            $.each(platformData, function(key, platformItem){
                if (platformItem.Name == selectedOptions){
                    emonEvents = platformItem.emonevents
                    $.each(emonEvents, function(key, eventItem){
                        if (eventItem.Name == obj)
                        {
                            emonCounters = eventItem.emoncounters;
                            $.each(emonCounters, function(idx, counterItem){
                                $('#ddlEmonCounters')
                                    .append($("<option></option>")
                                    .attr("value", counterItem.Name)
                                    .text(counterItem.Name));  
                                });
                        }
                    });
                }
            });

        });
    }
    
    $('#ddlEmonCounters').multiselect(
        {
            includeSelectAllOption: true,
            selectAllText: 'Select all',
            enableFiltering: true,
            enableCaseInsensitiveFiltering: true
        }
    );
    $('#ddlEmonCounters').multiselect('rebuild');
}




