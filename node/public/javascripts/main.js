$(document).ready(function(){
	var socket = io.connect(location.host);
	passcode_bar = $("#dailyPasscode");
	current = "#000000";
	var update_color = function(color) {
		if (current != color)
		{
			current = color;
			$('#color-preview').css('background-color',color);
			console.log(color);
			socket.emit('color', {passcode: passcode_bar.val(), color: color});
		}
	};
	$('#color-picker').farbtastic(update_color);
	$('#radio-button').button();
});
