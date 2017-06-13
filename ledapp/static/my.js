function update(jscolor) {
var newcolor = '#' + jscolor;
$('body').css('background-color',newcolor);
var r=parseInt(newcolor.slice(1,3),16);
var g=parseInt(newcolor.slice(3,5),16);
var b=parseInt(newcolor.slice(5,7),16);
vals = 'r='+r+'&g='+g+'&b='+b+'&s='+1;
$.get('/apply',vals);
}
$(document).ready(function(){

});
