// header
$(window).scroll(function(){
    if ($(this).scrollTop() > 50) {
       $('.header-top-main').addClass('nav-down');
    } else {
       $('.header-top-main').removeClass('nav-down');
    }
});

// over header


// // auto tab

// var tabChange = function(){
//     var tabs = $('.nav-pills > li');
//     var active = tabs.filter('.active');
//     var next = active.next('li').length? active.next('li').find('a') : tabs.filter(':first-child').find('a');
  
//     next.tab('show')
// }
 
// var tabCycle = setInterval(tabChange, 1000)
 
// $(function(){
//     $('.nav-tabs a').click(function(e) {
//         e.preventDefault();
         
//         clearInterval(tabCycle);
         
//         $(this).tab('show')
         
//         setTimeout(function(){
//             tabCycle = setInterval(tabChange, 1000) 
//         }, 1000);
//     });
// });

// // over auto tab

$('.owl-carousel').owlCarousel({
    loop:true,
    margin:10,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
            nav:true
        },
        600:{
            items:3,
            nav:false
        },
        1000:{
            items:2.5,
            nav:true,
            loop:false
        }
    }
})