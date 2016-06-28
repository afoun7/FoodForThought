$(document).ready(function() {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $('#submitButton').on('click', function(e){
    // We don't want this to act as a link so cancel the link action
    e.preventDefault();

    doSubmit();
  });

    // on the search page, users can add recipes to their calendar
    window.doSubmit = function() {
        $("#add").popup('close');
        console.log($('#meal').val());
        console.log($('#date').val()); // date that user enters 
  
        // need to add a time to each date object
        var newdate = new Date($('#date').val());
        if (($('#meal').val()) == "breakfast") {
            newdate.setHours(7); // automatically set the time of event to 7AM
        } else if (($('#meal').val()) == "lunch") {
            newdate.setHours(12); // automatically set the time of event to noon
        } else if (($('#meal').val()) == "dinner") {
            newdate.setHours(18); // automatically set the time of event to 6PM
        };
    
        calendar.fullCalendar('renderEvent',
            {
                // title: 'testing',
                // start: '2016-05-03'
                title: $('#recipeName').val(),
                start: newdate,
               end: newdate.setMinutes(newdate.getMinutes() + 60)
            },
            true);
        calendar.fullCalendar('rerenderEvents');

        console.log("done!")
       };
}); 


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

