// createMember addmember
// test data
var data = {
    'design': [{
        'id': 1,
        'name': 'xiaoming'
    }, {
        'id': 2,
        'name': 'xiaobai'
    }],
    'frontend': [{
        'id': 3,
        'name': 'xiaosong'
    }, {
        'id': 4,
        'name': 'xiaoli'
    }]
};

var memberlist = {};
memberlist.data = {};


memberlist.renderPartmentList = function(data) {
    $.each(data, function(key, obj) {
        $('#partment').append('<li class="list-group-item">' + key + '</li>');
        $('#partment li').first().addClass('active');
    });
    $('#partment').on('click', 'li', function() {
        var partmentName = $(this).html();
        // toggle class
        $('#partment li').removeClass('active');
        $(this).addClass('active');
        // render member list
        memberlist.rendermemberlist(partmentName);
    });
    $('#member').on('click', 'li', function() {
        $(this).toggleClass('active');
        // get and update data
        memberlist.getSelectList();
    });

}
memberlist.rendermemberlist = function(partmentName) {
    $('#member').attr('title', partmentName).empty();

    $.each(data[partmentName], function(i, v) {
        // recoard selection
        if (memberlist.data.hasOwnProperty(v['id']) == true) {
            $('#member').append('<li class="list-group-item active" data-userid="' + v['id'] + '">' + v['name'] + '</li>');
        } else {
            $('#member').append('<li class="list-group-item" data-userid="' + v['id'] + '">' + v['name'] + '</li>');
        }
    });
}

memberlist.getSelectList = function() {
    $('#member li').each(function() {
        var key = $(this).attr('data-userid'),
            value = $(this).html();
        if ($(this).hasClass('active')) {
            memberlist.data[key] = value;
        } else {
            delete memberlist.data[key];
        }
    });
}

// todo: get data from api
memberlist.renderPartmentList(data);