
$('#submit-btn').click(function(e){

		data = {}
		$('input[type=text]').each( (i, e) => {	
			console.log(e);
			data[e.name] = e.value
		})

	$.ajax({
		dataType:'json',
		contentType:'application/json',
		data:JSON.stringify(data),
		type:'POST',
		url:'/checkout/',
		success:function(result){
			console.log(JSON.stringify(result))
		}
	})
})
