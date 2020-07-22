$(document).ready(function () {
    $(".tab-item").hide();
    $("#tab-item1").show();
    $("#tab1").click(function () {
        $(".tab-item").hide();
        $(".tab").removeClass("active");
        $("#tab1").addClass("active");
        $("#tab-item1").show();

    });
    $("#tab2").click(function () {
        $(".tab-item").hide();
        $(".tab").removeClass("active");
        $("#tab2").addClass("active");
        $("#tab-item2").show();
    });
    $("#tab3").click(function () {
        $(".tab-item").hide();
        $(".tab").removeClass("active");
        $("#tab3").addClass("active");
        $("#tab-item3").show();
    });
    $("#tab4").click(function () {
        $(".tab-item").hide();
        $(".tab").removeClass("active");
        $("#tab4").addClass("active");
        $("#tab-item4").show();
    });

    /** 侧边栏回到顶部 */
    var rocket = $('#rocket');

    $(window).on('scroll', debounce(slideTopSet, 200));

    function debounce(func, wait) {
        var timeout;
        return function () {
            clearTimeout(timeout);
            timeout = setTimeout(func, wait);
        };
    };

    function slideTopSet() {
        var top = $(document).scrollTop();

        if (top > 200) {
          //  console.log('top',top);
            rocket.show();
        } else {
            rocket.hide();
        }
    }

    $(document).on('click', '#rocket', function (event) {
        rocket.addClass('move');
        $('body, html').animate({
            scrollTop: 0
        }, 800);
    });
    $(document).on('animationEnd', function () {
        setTimeout(function () {
            rocket.removeClass('move');
        }, 400);

    });
    $(document).on('webkitAnimationEnd', function () {
        setTimeout(function () {
            rocket.removeClass('move');
        }, 400);
    });

});
