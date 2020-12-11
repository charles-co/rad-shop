/* Scrolling Effect */
$(window).scroll(function() {
    if ($(document).scrollTop() > 80) {
        $('.navv').addClass('affix navbar-dark text-white').removeClass('navbar-light bg-light text-dark');
        $('#cartnav-mobile a').removeClass('btn-light').addClass('btn-dark');
        $('.navv #sidebarCollapse').addClass('bg-dark');
        $('.navv #sidebarCollapse span').addClass('bg-white');
    } else {
        $('.navv').removeClass('affix navbar-dark text-white').addClass('navbar-light bg-light text-dark');
        $('#cartnav-mobile a').removeClass('btn-dark').addClass('btn-light');
        $('.navv #sidebarCollapse').removeClass('bg-dark');
        $('.navv #sidebarCollapse span').removeClass('bg-white');
    }
});

/* Navigation */
$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        // open sidebar
        $('#sidebar').addClass('active');
        // fade in the overlay
        $(this).addClass('active');
        $('#sidebarCollapsev').addClass('active');
        $('.overlayy').addClass('active');
        $('.collapse.in').addClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
    $('#sidebarCollapsev, .overlayy').on('click', function () {
        // open sidebar
        $('#sidebar').removeClass('active');
        // fade in the overlay
        $(this).removeClass('active');
        $('#sidebarCollapse').removeClass('active');
        $('.overlayy').removeClass('active');
        
        $('.collapse.in').removeClass('in');
    });
    $('#COLLECTIONSSubmenu').on('show.bs.collapse', function () {
        $('.menu-data-toggle i').removeClass('fa-plus').addClass('fa-minus');
    });
    $('#COLLECTIONSSubmenu').parent().on('hide.bs.collapse', function () {
        $('.menu-data-toggle i').removeClass('fa-minus').addClass('fa-plus');
    });
    $('.list-group.desktop .list-group-item').hover(function() {
        $(this).find('.collapse').collapse('show');
        $(this).addClass('text-dark');
    }, function() {
        $(this).find('.collapse').collapse('hide');
        $(this).removeClass('text-dark');
    });
    $(function(){
        setInterval(function(){
            var animationName = 'animate__animated animate__tada';
            var animationend = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
            $('.logo-logo').addClass(animationName).one(animationend, function(){
                $(this).removeClass(animationName);
            });
        }, 6000);
    });
});
/* Preloader */
$(window).on("load", function() {
    $(".loader-wrapper").fadeOut("slow");
});

/* Currency Formatter */
const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'NGN', 
    minimumFractionDigits: 2
})