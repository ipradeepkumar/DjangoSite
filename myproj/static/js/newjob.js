var platformData;
BASEAPI_URL = 'http://127.0.0.1:8000'
$(function(){
    setEmonCounters([0]);
    $('#id_EmonEvents').hide();
    $('#ddlEmonEvents').hide();
    $('#id_EmonCounters').hide();
    $('#ddlEmonCounters').hide();
    $('.multiselect-native-select').hide();
    $('.regression').hide();
    $('.advanced').hide();
    $('.algorithm').hide();
    
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
                    .attr("value", item.Desc + "^" + item.Name)
                    .text(item.Name)); 
            }); //End of foreach Loop  
            $('#ddlStation').selectpicker({
                liveSearch: true,
                maxOptions: 1,
                liveSearchStyle: 'contains',
            });
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
            // $('#ddlToolName').multiselect(
            //     {
            //         includeSelectAllOption: true,
            //         selectAllText: 'Select all',
            //         enableFiltering: true,
            //         enableCaseInsensitiveFiltering: true,
            //     }
            // );
            // $('#ddlToolName').multiselect('rebuild');
        }, //End of AJAX Success function  

        failure: function (data) {  
            alert(data.responseText);  
        }, //End of AJAX failure function  
        error: function (data) {  
            alert(data.responseText);  
        } //End of AJAX error function  

    }); 

    //ajax call for fetching platforms
    // $.ajax({  
    //     type: "GET",  
    //     url: "/api/platforms",  
    //     contentType: "application/json; charset=utf-8",  
    //     dataType: "json",  
    //     success: function (data) {  
    //         $('#ddlPlatform')
    //                 .append($("<option></option>")
    //                 .attr("value", "")
    //                 .text("-- Select Platform--"));  
    //         $.each(data, function (key, item) { 
    //             $('#ddlPlatform')
    //                 .append($("<option></option>")
    //                 .attr("value", item.fields.Name)
    //                 .text(item.fields.Name));  
               
    //         }); //End of foreach Loop   
    //     }, //End of AJAX Success function  
    //     failure: function (data) {  
    //         alert(data.responseText);  
    //     }, //End of AJAX failure function  
    //     error: function (data) {  
    //         alert(data.responseText);  
    //     } //End of AJAX error function  

    // }); 
   
    // $('#ddlPlatform').on('change', function(e){
       
    // });
    
    $('#chkEmon').on('change', function(e){
        if (e.target.checked)
        {
            $('#id_EmonEvents').show();
            $('#ddlEmonEvents').show();
            $('#id_EmonCounters').show();
            $('#ddlEmonCounters').show();
            $('#id_EmonEvents > .multiselect-native-select').show();
        }
        else
        {
            $('#id_EmonEvents').hide();
            $('#ddlEmonEvents').hide();
            $('#id_EmonCounters').hide();
            $('#ddlEmonCounters').hide();
            $('#id_EmonEvents > .multiselect-native-select').hide();
        }
        setEmonCounters($('#ddlEmonEvents').val());
    });

    //ajax call for fetching ideas
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
    
    //setSections();
    


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
    emonEventsVal = 0;
    if ( $("#ddlEmonEvents").val().length == 0)  
        emonEventsVal = 0; 
    else  
        emonEventsVal = $("#ddlEmonEvents").val();
    //if ($('#chkEmon').attr('checked') === 'checked'){
        $.ajax({  
            type: "GET",  
            url: "/api/counter/" + emonEventsVal ,  
            contentType: "application/json; charset=utf-8",  
            dataType: "json",  
            success: function (data) {  
                //isPlatformChanged = true;
                $('#ddlEmonCounters').find('option').remove();
                emonCounters = data;
                    $.each(emonCounters, function(idx, counterItem){
                        $('#ddlEmonCounters')
                            .append($("<option></option>")
                            .attr("value", counterItem.fields['EmonCounterID'])
                            .text(counterItem.fields['Name']));  
                        });
                        BuildEmonCounter();
                       
            }, //End of AJAX Success function  
            failure: function (data) {  
                console.log(data.responseText);  
            }, //End of AJAX failure function  
            error: function (data) {  
                console.log(data.responseText);  
            }
        }); 
    //}
}
function BuildEmonCounter(){
    $('#ddlEmonCounters').multiselect(
        {
            includeSelectAllOption: true,
            selectAllText: 'Select all',
            enableFiltering: true,
            enableCaseInsensitiveFiltering: true,
            maxHeight: 200
        }
    );
    $('#ddlEmonCounters').multiselect('rebuild');
}
function setSections(){
    var divElement = $('#section1')[0];
    divElement.innerText = 'Section 1';
    $('#id_DebugMode')[0].insertBefore(divElement, null);
}

function showSection1(){
   $('#id_RegressionName').toggle();
   $('#id_TotalIterations').toggle();
}

function clearForm(){
    $('#taskForm')[0].reset();
    $('#ddlEmonCounters').multiselect('refresh');
    $('#ddlEmonEvents').multiselect('refresh');
}


function toggleRegression(obj){
    if (obj.className == 'ti-angle-up'){
        obj.className = 'ti-angle-down';
        $('.regression').hide();
    }
    else{
        obj.className = 'ti-angle-up';
        $('.regression').show();
    }

}

function toggleAlgorithm(obj){
    if (obj.className == 'ti-angle-up'){
        obj.className = 'ti-angle-down';
        $('.algorithm').hide();
    }
    else{
        obj.className = 'ti-angle-up';
        $('.algorithm').show();
    }

}

function toggleAdvance(obj){
    if (obj.className == 'ti-angle-up'){
        obj.className = 'ti-angle-down';
        $('.advanced').hide();
    }
    else{
        obj.className = 'ti-angle-up';
        $('.advanced').show();
    }

}



