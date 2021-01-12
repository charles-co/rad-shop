/* Scrolling Effect */
$(window).scroll(function() {
    if ($(document).scrollTop() > 80) {
        $('.navv').addClass('affix navbar-dark text-white').removeClass('navbar-light bg-light text-dark');
        $('#cartnav-mobile a').removeClass('text-dark').addClass('text-white');
        $('#cartnav-mobile button').removeClass('text-dark').addClass('text-info');
        $('.navv #sidebarCollapse').addClass('bg-dark');
        $('.navv #sidebarCollapse span').addClass('bg-white');
    } else {
        $('.navv').removeClass('affix navbar-dark text-white').addClass('navbar-light bg-light text-dark');
        $('#cartnav-mobile a').removeClass('text-white').addClass('text-dark');
        $('#cartnav-mobile button').removeClass('text-info').addClass('text-dark');
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
    $('.list-group.desktop .shop').hover(function() {
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
    $('#searchModal').on('shown.bs.modal', function(){
        $('#InputSearch').focus();
    });
    $('#searchModal').on('show.bs.modal', function(){
        var closeBtn = $(this).find("button[data-custom-dismiss='modal']");
        closeBtn.one('click', function(){
            $('#searchModal').on('webkitAnimationEnd oanimationend msAnimationEnd animationend', function(evt){
                $('#searchModal').modal('hide')
            });
            $('#searchModal').removeClass('animate__zoomIn').addClass('animate__zoomOut');
        })
    });
    $('#searchModal').on('hide.bs.modal', function(evt){
        var closeBtn = $(this).find("button[data-custom-dismiss='modal']");
        $('#searchModal').removeClass('animate__zoomOut').addClass('animate__zoomIn');
        $(this).off('webkitAnimationEnd oanimationend msAnimationEnd animationend')
        closeBtn.off('click')
    })
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