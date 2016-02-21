(function($) {
    var $pswp = $('.pswp')[0];
    var image = [];
    var lightbox;

    $('div#lightbox').each( function() {
        var $pic     = $(this),
            getItems = function() {
                var items = [];
                $pic.find('a').each(function() {
                    var $href   = $(this).attr('href'),
                        $title  = $(this).data('title');

                    var sizeRegex = /(\d+)[x](\d+)([\.jpg]+)/g;
                    var $size = sizeRegex.exec($href);

                    var item = {
                        src     : $href,
                        w       : $size[1],
                        h       : $size[2],
                        title   : $title
                    };

                    items.push(item);
                });
                return items;
            };

        var items = getItems();

        $.each(items, function(index, value) {
            image[index]     = new Image();
            image[index].src = value.src;
        });

        $pic.on('click', 'a', function(event) {
            event.preventDefault();
            var $index = $(this).index('figure a');
            var options = {
                index: $index,
                showHideOpacity: true,
                bgOpacity: 0.8
            };

            lightBox = new PhotoSwipe($pswp, PhotoSwipeUI_Default, items, options);
            lightBox.init();
        });
    });


    $('img.lazy').hide();
    $('img.lazy').each(function(i) {
        if (this.complete) {
            $(this).fadeIn("slow");
        } else {
            $(this).load(function() {
                $(this).fadeIn("slow");
            });
        }
    });

    $('button.pswp__button--info').on('click', function(event) {
        event.preventDefault();
        $('.exif-info').parent().addClass('exif-show-info');
        var currImage = image[lightBox.getCurrentIndex()];
        EXIF.getData(currImage, function() {
            var make = EXIF.getTag(this, "Make"),
                model = EXIF.getTag(this, "Model"),
                aperture = EXIF.getTag(this, "FNumber"),
                shutterSpeed = EXIF.getTag(this, "ExposureTime"),
                focalLength = EXIF.getTag(this, "FocalLength"),
                iso = EXIF.getTag(this, "ISOSpeedRatings");

            $('#camera-make').text(make);
            $('#camera-model').text(model);
            $('#aperture').text(aperture);
            $('#shutter-speed').text(shutterSpeed +'s (' + shutterSpeed.numerator + '/' + shutterSpeed.denominator + ')');
            $('#focal-length').text(focalLength);
            $('#iso').text(iso);
        });
    });

    $('button.exif-close').on('click', function(event) {
        event.stopPropagation();
        $('.exif-info').parent().removeClass('exif-show-info');
    });

    $(document).keyup(function(e) {
     if (e.keyCode == 27) { // escape key maps to keycode `27`
        $('.exif-info').parent().removeClass('exif-show-info');
    }
});
})(jQuery);
