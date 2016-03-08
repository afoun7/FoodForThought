function getSearchRequest() {
    console.log("in getSearchRequest");
    var x = document.getElementById("userSearch").value;
    document.getElementById("input").innerHTML = x; // x is what the user typed into search box
    $.ajax({
    	url: '/search',
    	//data: $('id'), // what the user typed into the search box
    	data: JSON.stringify({id:'amanda'}),
        type: 'POST',
    	success: function(response) {
    		console.log(response);
    	},
    	error: function(error) {
    		console.log(error);
    	}
    });
};

// clicking hamburger menu button
$('#sidebar-btn').click(function() {
  $('#sidebar').toggleClass('visible');
});
               