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
		$('.progress-bar').progressbar();
		$('#loading').show();
		queryVCs(page);
	}
});

function queryVCs(){
	$.ajax({
		url:"/get/vcs/"+page,
		method:"POST",
		data:"description="+desc,
		success:function(data){
			// remove progress bar
			$('#loading').hide();
			_.templateSettings.variable = "rc";

			var template = _.template(
            	$( "script.template" ).html()
        	);
			console.log(data);
        	$( "#vc-list" ).append(
            template(data)
       		 );
        	page = page + 1;
        	if (page < 8){
        		queryVCs();
        	}
		},
		error:function(){
			$("#desc-error").show();
		}
	});
}

$('.progress-bar').on("positionChanged", function (e) {
    if (e.percent == 100){
    	$('.progress-bar').reset();
    }
});