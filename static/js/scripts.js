$(document).ready(function() {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();
    var calendar = $('#calendar').fullCalendar({
      defaultView: 'basicWeek',
      editable: true,
      selectable: true,
    });

    $('#submitButton').on('click', function(e){
    // We don't want this to act as a link so cancel the link action
    e.preventDefault();

    doSubmit();
  });

    window.doSubmit = function() {
         $("#add").popup('close');
        console.log($('#meal').val());
        console.log($('#date').val());
  
        var d = new Date($('#date').val());
        if (($('#meal').val()) == "breakfast") {
            d.setHours(7);
        };
    
        $("#calendar").fullCalendar('addEventSource',
            {
                title: $('#recipeName').val(),
                start: d,
                end: d.setMinutes(d.getMinutes() + 60)
            },
            true);
        $("#calendar").fullCalendar('rerenderEvents');

       };
}); 


// function doSubmit(){
//         $("#add").popup('close');
//         console.log($('#meal').val());
//         console.log($('#date').val());
//         alert("form submitted");

//         $("#calendar").fullCalendar('renderEvent',
//             {
//                 title: $('#recipeName').val(),
//                 start: new Date($('#date').val()),
//             },
//             true);
//         $("#calendar").fullCalendar('rerenderEvents');
//         alert("added to calendar");
//        };


// allergy form
$(document).ready(function() {
     $('#has_allergies').change(function() {
        if(this.value=="has_allergies") {
            $("#allergiesDiv").toggle();
        }       
    })
 });

// indicate other allergies
$(document).ready(function() {
     $("#other").change(function () {
        //check if it's checked. If checked move inside and check for others value
        if(this.value == "other") {
            //add a text box next to it
           // alert("hi")
           $("#other-text").toggle();
        } 
    })
});

