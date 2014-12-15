$(document).ready(function(){
	var socket = io.connect(location.host);
	passcode_bar = $("#dailyPasscode");
	color_preview = $('#color-preview');
	current = "#000000";
	var update_color = function(color) {
		if (current != color)
		{
			current = color;
			strip = $("#strip-picker #radio-button .active").data('value');
			color_preview.css('background-color',color);
			socket.emit('color', {passcode: passcode_bar.val(), color: color, strip: strip});
		}
	};
	var update_theme = function(event) {
		strip = $("#strip-picker #radio-button .active").data('value');
		theme = $(event.target).data('theme');
		socket.emit('theme', {passcode: passcode_bar.val(), theme: theme, strip: strip});
	};
	$('.theme-button').click(update_theme);
	$('#turn-on-button').click(function(){ update_color("#ffffff"); });
	$('#turn-off-button').click(function(){ update_color("#000000"); });
	$('#color-picker').farbtastic(update_color);
	$('#radio-button').button();
});
