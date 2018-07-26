$(window).scroll(function(){
    let position = $(this).scrollTop();

    if (position >=718){
        $('#back-to-top').addClass('scrollTop');
    }
    else{
        $('#back-to-top').removeClass('scrollTop');
    }
})

$('#back-to-top').onclick(function(link){
    console.log("h");
    link.preventDefault();

     let target = $(this).attr('href');
     
     $('html, body').animate({
         scrollTop: $(target).offset().top -25
     },3000);
})