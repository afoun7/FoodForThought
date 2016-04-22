  $(document).on('pageshow','#index',function(e,data){    
        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
    
        $('#calendar').fullCalendar({
            editable: true,
            events: [
                {
                    title: 'Meal',
                    start: new Date(y, m, d, 10, 30),
                    allDay: false
                },
                {
                    title: 'Meal',
                    start: new Date(y, m, d, 12, 0),
                    end: new Date(y, m, d, 14, 0),
                    allDay: false
                }
            ]
        });
    });


$(document).ready(function() {
     $('#has_allergies').change(function() {
        if(this.value=="has_allergies") {
            $("#allergiesDiv").toggle();
        }       
    })
 });

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

