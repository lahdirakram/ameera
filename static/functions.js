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

