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
