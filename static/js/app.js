$("#submit-desc").click(function(){
	desc = $("#description").val();
	$("#desc-error").hide();
	$("#desc-warning").hide();
	page = 1;
	// description too short
	if (desc.split(" ").length < 3){
		$("#desc-parent").addClass("has-warning");
		$("#desc-warning").show();
	}
	else{
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
			},
			error:function(){
				$("#desc-error").show();
			}
		});
});