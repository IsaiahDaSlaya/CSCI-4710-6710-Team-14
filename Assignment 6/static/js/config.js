var data_obj = read_data();
$(document).ready(function(){

	$('#continue').click(function(){
		window.location.href = "/runtests";
		
	});

});

$(document).ready(function(){
$('#df').change(function(){
	var index = document.getElementById("df").selectedIndex;   
	addItem(index, data_obj);
   });	
$('#modifyButton').click(function(){
		var index = document.getElementById("df").selectedIndex;
		document.getElementById("humiditytext").value = data_obj.Humidity[index];
		document.getElementById("temperaturetext").value = data_obj.Temperature[index];
	});   
 $('#modifyCan').click(function(){
	 document.getElementById("modifyDia").close();
 });
 $('#modifySave').click(function(){
	 var index = document.getElementById("df").selectedIndex;
	 data_obj.Humidity[index] = document.getElementById("humiditytext").value;
	 data_obj.Temperature[index] = document.getElementById("temperaturetext").value
	 
 });
 
 $('#testSave').click(function(){
	  save_data();
 });
});


function addItem(index, data){
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
function read_data()
{
	var get_url = '/read_data';		
		$.get(get_url, function( data ) {
		data_obj = JSON.parse(data);
		return data_obj;
		});
}

function save_data()
{	        
    var url = '/save_data';
	$.get(url, function() {alert()});
   	
}


