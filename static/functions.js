lastelm=null
function scrolto(id,elm) {
  if (lastelm != $(elm)) {
  $(elm).addClass('active');
  if (lastelm != null) {
    lastelm.removeClass('active');
  }
  lastelm=$(elm);
  }
  $('html, body').animate({
        scrollTop: $(id).offset().top-160
    }, 2000);
}

lastelm_sm=null
function scrolto_sm(id,elm) {
  if (lastelm_sm != $(elm)) {

    $(elm).addClass('active_svg');

    if (lastelm_sm != null) {
      lastelm_sm.removeClass('active_svg');
    }

    lastelm_sm=$(elm);
  }else{
    alert('else');
  }
  $('html, body').animate({
        scrollTop: $(id).offset().top-160
    }, 2000);
}

function dict_to_utc(dict_array) {

  for (var i = 0; i < dict_array.length; i++) {
    dict=dict_array[i];
    list=dict['data'];
    for (var j = 0; j < list.length; j++) {
      list[j][0]=Date.UTC(list[j][0][2],list[j][0][1]-1,list[j][0][0],0,0,0,0);
    }
    dict['data']=list;
    dict_array[i]=dict;
  }
  return dict_array;
}

/*
 * jQuery Easing Compatibility v1 - http://gsgd.co.uk/sandbox/jquery.easing.php
 *
 * Adds compatibility for applications that use the pre 1.2 easing names
 *
 * Copyright (c) 2007 George Smith
 * Licensed under the MIT License:
 *   http://www.opensource.org/licenses/mit-license.php
 */

jQuery.extend( jQuery.easing,
{
	easeIn: function (x, t, b, c, d) {
		return jQuery.easing.easeInQuad(x, t, b, c, d);
	},
	easeOut: function (x, t, b, c, d) {
		return jQuery.easing.easeOutQuad(x, t, b, c, d);
	},
	easeInOut: function (x, t, b, c, d) {
		return jQuery.easing.easeInOutQuad(x, t, b, c, d);
	},
	expoin: function(x, t, b, c, d) {
		return jQuery.easing.easeInExpo(x, t, b, c, d);
	},
	expoout: function(x, t, b, c, d) {
		return jQuery.easing.easeOutExpo(x, t, b, c, d);
	},
	expoinout: function(x, t, b, c, d) {
		return jQuery.easing.easeInOutExpo(x, t, b, c, d);
	},
	bouncein: function(x, t, b, c, d) {
		return jQuery.easing.easeInBounce(x, t, b, c, d);
	},
	bounceout: function(x, t, b, c, d) {
		return jQuery.easing.easeOutBounce(x, t, b, c, d);
	},
	bounceinout: function(x, t, b, c, d) {
		return jQuery.easing.easeInOutBounce(x, t, b, c, d);
	},
	elasin: function(x, t, b, c, d) {
		return jQuery.easing.easeInElastic(x, t, b, c, d);
	},
	elasout: function(x, t, b, c, d) {
		return jQuery.easing.easeOutElastic(x, t, b, c, d);
	},
	elasinout: function(x, t, b, c, d) {
		return jQuery.easing.easeInOutElastic(x, t, b, c, d);
	},
	backin: function(x, t, b, c, d) {
		return jQuery.easing.easeInBack(x, t, b, c, d);
	},
	backout: function(x, t, b, c, d) {
		return jQuery.easing.easeOutBack(x, t, b, c, d);
	},
	backinout: function(x, t, b, c, d) {
		return jQuery.easing.easeInOutBack(x, t, b, c, d);
	}
});






