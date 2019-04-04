$(document).ready(function () {

	$('#continue').click(function () {
		window.location.href = "/runtests";

	});

});

$(document).ready(function () {

	$('#index').click(function () {
		window.location.href = "/";
	});

});

$(document).ready(function () {
	$('#df').change(function () {
		var index = document.getElementById("df").selectedIndex;

		var get_url = '/read_data';
		$.get(get_url, function (data) {
			data_obj = JSON.parse(data);
			addItem(index, data_obj);
		});

	});
});

function addItem(index, data) {
	var ul = document.getElementById("di");
	$('#di').empty();
	var li = document.createElement("li");
	li.className = "list-group-item";
	li.appendChild(document.createTextNode(data_obj.Humidity[index]));
	ul.appendChild(li);
	var li2 = document.createElement("li");
	li2.className = "list-group-item";
	li2.appendChild(document.createTextNode(data_obj.Temperature[index]));
	ul.appendChild(li2);
}