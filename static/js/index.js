$(document).ready(function() {
	console.log('calledasds');
	var country_selected = '';
	$('#countryID').change(function(obj){
		country_selected = this.value;
	});

	$("#submit_closest").click (function () {
		var lat = $('#lat').val();
		var lon = $('#lon').val();
		var k = $('#k').val();
		var url = 'http://localhost:5000/cities/proximity?lat='+lat+ '&lon=' + lon + '&size=' + k + '&country_code='+ country_selected;
		$.ajax({
			url : url,
			success : function(response) {
				var html = '';
				$.each(response, function (index, singleCity) {
					html += '<div>'+singleCity+'</div>';
				});
				$("#result_for_closest").html(html);
			}
		})
	})
	$.ajax({
		url : 'http://localhost:5000/countries',
		type : 'GET',
		success : function (response) {
			$.each(response, function (index, country) {
				$('#countryID').append("<option value=" +country +">" +country+"</>")
			});
		}
	});

	$("#submit_lexical").click (function () {
		var keyword = $('#keyword').val();
		var url = 'http://localhost:5000/cities/lexical?keyword='+ keyword;
		$.ajax({
			url : url,
			success : function(response) {
				var html = '';
				$.each(response, function (index, singleCity) {
					html += '<div>'+singleCity+'</div>';
				});
				$("#result_for_lexical").html(html);
			}
		})
	})
});