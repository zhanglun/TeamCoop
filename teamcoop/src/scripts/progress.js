// progress
$(function() {
    var progress = {};
    progress.status = false;
    progress.selector = ".progressBar ul";
    progress.circleSize = $(progress.selector + ' li:even').size();
    progress.circleWidth = $(progress.selector + ' li:even').width();
    progress.setWidth = function() {
        var width = ($(progress.selector).width() - progress.circleSize * progress.circleWidth) / (progress.circleSize - 1) - 3;
        $(progress.selector + ' li:odd').width(width);
    };
    // resize div width
    $(window).on('resize', function() {
        setTimeout(progress.setWidth, 100);
    });
    $('#edit_btn').on('click', function() {
        $(this).html(progress.status == false ? '保存' : '编辑');
        progress.status = !progress.status;
    })
    $(progress.selector).on('click', 'li:even span', function(event) {
        if (progress.status == false) {
            return false;
        }
        var eventobj = $(event.target);
        if (eventobj.hasClass('checked')) {
            return false;
        } else {
            var index = eventobj.parent().index();
            $(progress.selector + ' li').slice(0, index + 1).addClass('checked');
            $(progress.selector + ' li').slice(0, index + 1).find('span').html('');
        }
    });
    progress.setWidth();
});