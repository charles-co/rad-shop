// function setFooterStyle() {
//     var docHeight = $(window).height();
//     var footerHeight = $('.footer').outerHeight();
//     var footerTop = $('.footer').position().top + footerHeight;
//     if (footerTop < docHeight) {
//         $('.footer').css('margin-top', (docHeight - footerTop + 'px'));
//     } else {
//         $('.footer').css('margin-top', '');
//     }
//     $('.footer').removeClass('invisible');
// }

// $(document).ready(function() {
//     setFooterStyle();
//     window.onresize = setFooterStyle;
// });
$(window).on("load", function() {
    $(".loader-wrapper").fadeOut("slow");
});