// module namespace
var memberlist = {};
// data 
memberlist.static_data = {
    'design': [{
        'id': 1,
        'name': 'xiaoming'
    }, {
        'id': 2,
        'name': 'xiaobai'
    }, {
        'id': 5,
        'name': 'xiaobai'
    }, {
        'id': 6,
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
// select connent data
memberlist.data_chargers = {};
memberlist.data_participants = {};
// trigger btn
memberlist.triggerbutton = null;
// input container
// memberlist.input = (memberlist.triggerbutton != null) ? memberlist.triggerbutton.parentsUntil('.col-sm-10').find('input').get(0) : null;
// selectMember modal action (show and hide)
memberlist.modalshow = function() {
    $('#select_member').modal('show');
}
memberlist.modalhide = function() {
    $('#select_member').modal('hide');
}

memberlist.renderPartmentList = function() {
    $('#partment,#member').empty();
    $.each(memberlist.static_data, function(key, obj) {
        $('#partment').append('<li class="list-group-item">' + key + '</li>');
        $('#partment li').first().addClass('active');
    });
    $('#partment li').first().trigger('click');
}

memberlist.renderMemberlist = function(partmentName) {
    var data = (memberlist.triggerbutton.attr('id').indexOf('charger') == -1) ? memberlist.data_participants : memberlist.data_chargers;

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
    var data = {};
    $('#member li').each(function() {
        var key = $(this).attr('data-userid'),
            value = $(this).html();
        if ($(this).hasClass('active')) {
            data[key] = value;
        } else {
            delete data[key];
        }
    });
    if (memberlist.triggerbutton.attr('id').indexOf('charger') == -1) {
        memberlist.data_participants = data;
    } else {
        memberlist.data_chargers = data;
    }
}

memberlist.sendForward = function() {
    var data = (memberlist.triggerbutton.attr('id').indexOf('charger') == -1) ? memberlist.data_participants : memberlist.data_chargers;
    var input = memberlist.triggerbutton.parentsUntil('.col-sm-10').find('input').get(0);
    input.value = '';
    $.each(data, function(key, value) {
        input.value += value + ',';
    });
    // remove last indefieder
    input.value = input.value.substr(0,input.value.length-1);
    memberlist.modalhide();
    if (memberlist.triggerbutton.attr('id').indexOf('charger') == -1) {
        memberlist.data_participants = {};
    } else {
        memberlist.data_chargers = {};
    }
    // memberlist.trigger = null;
}


// bind event
memberlist.init = function() {
    $('#select_chargers,#select_participants').on('click', function() {
        memberlist.triggerbutton = $(this);
        memberlist.modalshow();
        memberlist.renderPartmentList();
    });
    // bind only once
    $('#partment').on('click', 'li', function() {
        var partmentName = $(this).html();
        // toggle class
        $('#partment li').removeClass('active');
        $(this).addClass('active');
        // render member list
        memberlist.renderMemberlist(partmentName);
    });
    $('#member').on('click', 'li', function(event) {
        $(this).toggleClass('active');
        // get and update data
        memberlist.getSelectList();
    });
    $('#send-forward').on('click', function() {
        memberlist.sendForward();
    });
}