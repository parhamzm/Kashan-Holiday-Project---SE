$(window).scroll(function(){
    let position = $(this).scrollTop();

    if (position >=700){
        $('#back-to-top').addClass('scrollTop');
        $('.navbar').addClass('fix');
    }
    else{
        $('#back-to-top').removeClass('scrollTop');
        $('.navbar').removeClass('fix');
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


function showFlashMessage(message){
    // var template = "{% include 'alert.html' with message='" + message + "' %}";
    var template = "<div class='container container-alert-flash'><div class='col-sm-3 col-sm-offset-8'><div class='alert alert-warning alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>" + message + "</div></div></div>";
    console.log(template);
    $("body").append(template);
    $(".container-alert-flash").fadeIn();
    setTimeout(function () {
        $(".container-alert-flash").fadeOut();
    }, 1800);
}


