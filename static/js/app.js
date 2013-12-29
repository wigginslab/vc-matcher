$("#submit-desc").click(function(){
	desc = $("#description").val();
	page = 1;
	$.ajax({
		url:"/get/vcs/"+page,
		method:"POST",
		data:"description="+desc,
		success:function(data){
			_.templateSettings.variable = "rc";

			var template = _.template(
            	$( "script.template" ).html()
        	);
			console.log(data);
        	$( "#vc-list" ).html(
            template(data)
       		 );
        	page = page + 1;
		}
	});
});