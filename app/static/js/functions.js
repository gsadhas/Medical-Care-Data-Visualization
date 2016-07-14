$(document).ready(function () {
    $(".bodySystemsPopover button").popover({
        title: 'Select Body Systems',
        content: '<form class="form-horizontal" method="POST" action="/showVitals">'+
        '<fieldset>'+
        '<legend>Select Filters</legend>'+
        '<div class="form-group">'+
          '<label class="col-md-4 control-label" for="checkboxes">Body Systems</label>'+
          '<div class="col-md-4">'+
          '<div class="checkbox">'+
            '<label for="checkboxes-0">'+
              '<input type="checkbox" name="bodySystem" id="checkboxes-0" value="1">'+
              'Neurologic'+
            '</label>'+
            '</div>'+
          '<div class="checkbox">'+
            '<label for="checkboxes-1">'+
              '<input type="checkbox" name="bodySystem" id="checkboxes-1" value="2">'+
              'Cardiovascular'+
            '</label>'+
            '</div>'+
            '<div class="checkbox">'+
              '<label for="checkboxes-2">'+
                '<input type="checkbox" name="bodySystem" id="checkboxes-2" value="3">'+
                'Pulmonary'+
              '</label>'+
            '</div>'+
            '<br/>'+
            '<div>'+
              '<button id="singlebutton" name="singlebutton" class="btn btn-primary">Go</button>'+
          '</div>'+
          '</div>'+
        '</div>'+
        '</fieldset>'+
        '<input id="vitalsLow" type="hidden" name="vitals" value="0" />'+
        '</form>',
        html: true
    });

    $(".filterChkBox").click(function(){

        var t = $(this);
        if (t.val() == 'pain') {
            if(t.is(':checked')) {
                $("#PSchart").show();
                consloe.log('fdf');
            }
            else {
                $("#PSchart").hide();
            }
        }
        else if (t.val() == 'bp') {
            if(t.is(':checked')) {
                $("#BPchart").show();
            }
            else {
                $("#BPchart").hide();
            }
        }
        else if (t.val() == 'temp') {
            if(t.is(':checked')) {
                $("#TempChart").show();
            }
            else {
                $("#TempChart").hide();
            }
        }
        else if (t.val() == 'rr') {
            if(t.is(':checked')) {
                $("#RespChart").show();
            }
            else {
                $("#RespChart").hide();
            }
        }
        else if (t.val() == 'pulse') {
            if(t.is(':checked')) {
                $("#PulseChart").show();
            }
            else {
                $("#PulseChart").hide();
            }
        }
        else if (t.val() == 'pulseOx') {
            if(t.is(':checked')) {
                $("#PulseOxChart").show();
            }
            else {
                $("#PulseOxChart").hide();
            }
        }
    });

    $(".filterChkBox2").click(function(){
        var t = $(this);
        if (t.val() == 'pain2') {
            if(t.is(':checked')) {
                $("#PSchart2").show();
            }
            else {
                $("#PSchart2").hide();
            }
        }
        else if (t.val() == 'bp2') {
            if(t.is(':checked')) {
                $("#BPchart2").show();
            }
            else {
                $("#BPchart2").hide();
            }
        }
        else if (t.val() == 'temp2') {
            if(t.is(':checked')) {
                $("#TempChart2").show();
            }
            else {
                $("#TempChart2").hide();
            }
        }
        else if (t.val() == 'rr2') {
            if(t.is(':checked')) {
                $("#RespChart2").show();
            }
            else {
                $("#RespChart2").hide();
            }
        }
        else if (t.val() == 'pulse2') {
            if(t.is(':checked')) {
                $("#PulseChart2").show();
            }
            else {
                $("#PulseChart2").hide();
            }
        }
        else if (t.val() == 'pulseOx2') {
            if(t.is(':checked')) {
                $("#PulseOxChart2").show();
            }
            else {
                $("#PulseOxChart2").hide();
            }
        }
    });

    $(".pulmonaryUpdate").click(function(){
        var patientNum = $(this).parent().find(".patientNumber").val();
        console.log("inside pulmonaryUpdate. patientNum is "+patientNum);
        console.log($(this).parent().find('.pulmonaryplan').val());
        if(patientNum === undefined)
        {
            $.post( "/updateResidentPlan", { residentplan: $('.pulmonaryplan').val(),
                body_system: 'pulmonary' })
              .done(function( data ) {
            });
        }
        else {
            $.post( "/updateResidentPlanTwo", {
                residentplan: $(this).parent().find('.pulmonaryplan').val(),
                patientNum: patientNum,
                body_system: 'pulmonary'
            })
              .done(function( data ) {
                console.log(data);
            });
        }
        var spanElement = $(this).parent().find('span');
        spanElement.toggleClass('hide');
        setTimeout(function(){ spanElement.toggleClass('hide');}, 3000);
    });

    $(".cardiovascularUpdate").click(function(){
        var patientNum = $(this).parent().find(".patientNumber").val();
        console.log("inside cardiovascularUpdate. patientNum is "+patientNum);
        if(patientNum === undefined)
        {
            $.post( "/updateResidentPlan", { residentplan: $('.cardiovascularplan').val(),
                body_system: 'cardiovascular' })
              .done(function( data ) {
              });
        }
        else {
            $.post( "/updateResidentPlanTwo", { 
                residentplan: $(this).parent().find('.cardiovascularplan').val(),
                patientNum: patientNum,
                body_system: 'cardiovascular' })
              .done(function( data ) {
              });
        }
        var spanElement = $(this).parent().find('span');
        spanElement.toggleClass('hide');
        setTimeout(function(){ spanElement.toggleClass('hide');}, 3000);
    });
    $(".neurologicUpdate").click(function(){

        var patientNum = $(this).parent().find(".patientNumber").val();
        console.log("inside neurologicUpdate. patientNum is "+patientNum);
        if(patientNum === undefined)
        {
            $.post( "/updateResidentPlan", { 
                residentplan: $('.neurologicplan').val(),
                body_system: 'neurologic' })
              .done(function( data ) {
                console.log(data);
              });
        }
        else {
            $.post( "/updateResidentPlanTwo", { 
                residentplan: $(this).parent().find('.neurologicplan').val(),
                 patientNum: patientNum,
                body_system: 'neurologic' })
              .done(function( data ) {
                console.log(data);
              });
        }
        var spanElement = $(this).parent().find('span');
        spanElement.toggleClass('hide');
        setTimeout(function(){ spanElement.toggleClass('hide');}, 3000);
    });


});