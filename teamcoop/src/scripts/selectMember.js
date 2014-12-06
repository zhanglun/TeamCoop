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
memberlist.static_data = {
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
memberlist.data_charger = {};
memberlist.data_participant = {};
memberlist.trigger = null;


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
    var data = (memberlist.trigger.attr('id').indexOf('charger') == -1) ? memberlist.data_participant : memberlist.data_charger;

    $('#member').attr('title', partmentName).empty();

    $.each(memberlist.static_data[partmentName], function(i, v) {
        // recoard selection
        if (data.hasOwnProperty(v['id']) == true) {
            $('#member').append('<li class="list-group-item active" data-userid="' + v['id'] + '">' + v['name'] + '</li>');
        } else {
            $('#member').append('<li class="list-group-item" data-userid="' + v['id'] + '">' + v['name'] + '</li>');
        }
    });
}

memberlist.getSelectList = function() {
    $('#member li').each(function() {
        var key = $(this).attr('data-userid'),
            value = $(this).html(),
            data = (memberlist.trigger.attr('id').indexOf('charger') == -1) ? memberlist.data_participant : memberlist.data_charger;
        if ($(this).hasClass('active')) {
            data[key] = value;
        } else {
            delete data[key];
        }
    });
}

memberlist.sendForward = function() {
    $('#send-forward').on('click', function() {
        var data = (memberlist.trigger.attr('id').indexOf('charger') == -1) ? memberlist.data_participant : memberlist.data_charger;
        $.each(data, function(key, value) {
            memberlist.trigger.parentsUntil('.col-sm-10').find('input').get(0).value += value + ',';
        });
        $('#select_member').modal('hide');
        var data = (memberlist.trigger.attr('id').indexOf('charger') == -1) ? memberlist.data_participant : memberlist.data_charger;
        data = {};
        memberlist.trigger = null;
        $('#member,#partment').empty();
    });
}


$('#select_chargers,#select_participants').on('click', function() {
    memberlist.trigger = $(this);
    $('#select_member').modal('show');
    // todo: get data from api
    memberlist.renderPartmentList(memberlist.static_data);
    memberlist.sendForward();
});