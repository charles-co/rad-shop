Vue.use(VueAwesomeSwiper)
const index = new Vue({
    el: '#index',
    store: store,
    delimiters: ['[[', ']]'],
    data (){
        return {
            swiperOptions: {
                grabCursor: true,
                loop: false,
                pagination: {
                    el: '.swiper-pagination',
                    dynamicBullets: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev'
                },
                breakpoints: {
                    1200: {
                        slidesPerView: 5,
                        spaceBetween: 10
                    },
                    768: {
                        slidesPerView: 4,
                        spaceBetween: 10
                    },
                    320: {
                        slidesPerView: 2,
                        spaceBetween: 10
                    },
                }
            },
            newArrivalProducts: [],
            bestSellerProducts: [],
            indexSlideShow: [],
            slideshowloading: true,
        }
    },
    created(){
        AOS.init();
        this.slideshows();
    },
    updated(){
        AOS.refreshHard();
    },
    mounted(){
        this.index();
    },
    filters: {
        currency: function(value){
            if (!value) return ''
            value = formatter.format(value)
            return value
        },
    },
    computed: {
    },
    methods: {
        slideshows(){
            Promise.all([
                fetch('api/all-products/slideshow/new-arrivals/').then(res => res.ok && res.json() || Promise.reject(res)),
                fetch('api/all-products/slideshow/best-sellers/').then(res => res.ok && res.json() || Promise.reject(res)),
            ])
            .then(response => {
                this.newArrivalProducts = response[0];
                this.bestSellerProducts = response[1];
                this.indexSlideShow = response[2];
                setTimeout( function(){
                    this.slideshowloading = false;
                }.bind(this), 1000);
            })
            .catch(function (error){
                console.log(error);
            })
        },
        index(){
            fetch('api/index/slideshow/').then(res => res.ok && res.json())
            .then( response => {
                $("#home-slideshow").vegas({
                    slides: response.images,
                    transition: ['zoomOut', 'flash'],
                    delay: 10000,
                    shuffle: true,
                    transitionDuration: 2000,
                    overlay: response.overlay
                });
                $('.vegas-timer').addClass('d-none')
                $('.vegas-content-scrollable').addClass('d-flex align-items-end justify-content-start p-md-5 py-5 px-4 w-100')
            });
        },
        slideshowhover(e){
        }
        
    }
});