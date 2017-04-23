	function hexFromRGB(r, g, b) {
	  var hex = [
		r.toString( 16 ),
		g.toString( 16 ),
		b.toString( 16 )
	  ];
	  $.each( hex, function( nr, val ) {
		if ( val.length === 1 ) {
		  hex[ nr ] = "0" + val;
		}
	  });
	  return hex.join( "" ).toUpperCase();
	}
    var software=1;//use software input vs hardware
    var inUse=false;// boolean determine if updateAll is already working, to avoid cyclic calls
	function updateAll(r,g,b,caller){
        if($(".ui-slider").length){ //ensure that the sliders are loaded before we manipulate them
            if(!inUse){
                inUse=true;//sets boolean
                switch(caller){
                    case 'palette':
                        //update sliders
                        $("#red").slider("value",r)
                        $("#green").slider("value",g)
                        $("#blue").slider("value",b)
                        //update lights
                        vals = 'r='+r+'&g='+g+'&b='+b+'&s='+software;
                        $.get('/apply',vals);
                        break;
                    case 'slider':
                        //change r,g,b from current slider values
                        r=$("#red").slider("value")
                        g=$("#green").slider("value")
                        b=$("#blue").slider("value")
                        var hexy=hexFromRGB(r,g,b);
                        $(".sp-input").val('#'+hexy);
                        $(".sp-input").change();
                        vals = 'r='+r+'&g='+g+'&b='+b+'&s='+software;
                        $.get('/apply',vals);
                        break;
                    case 'lights':
                        var hexy=hexFromRGB(r,g,b);
                        $(".sp-input").val('#'+hexy);
                        $(".sp-input").change();
                        $("#red").slider("value",r)
                        $("#green").slider("value",g)
                        $("#blue").slider("value",b)
                        break;
                    default:
                        break;
                }
                $( "#swatch" ).css( "background-color", "#" + hexFromRGB(r,g,b) );
                inUse=false;
            }
        }
    }     
	
function slideWrapper(){
    updateAll(0,0,0,'slider');
}
           
function pollServerForNewInfo() {
  	if(software==0){
		$.getJSON('/supply', function (response) {
            if(response.info==1){
                updateAll(response.red,response.green,response.blue,'lights');
		    }
        });
		setTimeout(pollServerForNewInfo, 15);
	}
  } 
$(function() {

	$( "#red, #green, #blue" ).slider({
	  orientation: "horizontal",
	  range: "min",
	  max: 255,
	  value: 0,
	  slide: slideWrapper,
	  change: slideWrapper
	});

	$("#b2").click( function (){
		$("#pane1").hide();
		$("#pane2").show();
		$("#pane3").hide();
		$("#pane4").hide();
		$("[role='presentation']").removeClass("active");
		$("#b2").addClass("active");
        $(".full-spectrum").trigger("click");
        $('.sp-replacer').hide();
		$(window).trigger('resize');
	});
 
	$("#b3").click( function (){
		$("#pane1").hide();
		$("#pane2").hide();
		$("#pane3").show();
		$("#pane4").hide();
		$("[role='presentation']").removeClass("active");
		$("#b3").addClass("active");
        $.get('/nappy');
	});

    $('#b2').trigger("click");
      $(window).resize(function(){
          var left=$(".sp-container").outerWidth();
          $('.ui-slider,#swatch').css('margin-left',left+25);
      });
   // clicking software button 
    $("#soft").click( function(){
        software=1;
        $("#soft").addClass('btn-primary');
        $("#soft").removeClass('btn-default');
        $('#hard').addClass('btn-default');
        $('#hard').removeClass('btn-primary');
        $('.ui-slider,.sp-container').css('pointer-events','auto');
        updateAll(0,0,0,'slider');
    });

    $("#hard").click( function(){
        software=0;
        $("#hard").addClass('btn-primary');
        $("#hard").removeClass('btn-default');
        $('#soft').addClass('btn-default');
        $('#soft').removeClass('btn-primary');
        $('.ui-slider,.sp-container').css('pointer-events','none');
        vals = 'r='+0+'&g='+0+'&b='+0+'&s='+software; //applys that trailing 0 to alert Arduino/python
        $.get('/apply',vals); // and sends it
		pollServerForNewInfo();
    } );
});
