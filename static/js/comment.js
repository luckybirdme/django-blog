$(function () {
	$("#comment").submit(function(e) {
		var self = $(this);

		var data = self.serialize();
		var url = self.attr('action');

		$.ajax({
			type: "POST",
			url: url,
			timeout : 10000,
			dataType: "json",
			data: data, // serializes the form's elements.
			success: function(data){
				if(data.error){
					
				}else if(data.redirect){
					location.href = data.redirect;
				};		
				console.log(data);		

			},
           	error:function(error) {

            },
			complete : function(XMLHttpRequest,status){
			}
        });
		e.preventDefault(); // avoid to execute the actual submit of the form.
	});



});