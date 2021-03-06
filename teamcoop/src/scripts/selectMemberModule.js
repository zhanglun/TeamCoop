// module namespace
var memberlist = {};

memberlist.errorTip = function(msg) {
        console.log(msg);
        alert('something error occured. refresh you page');
    }
    // default multiplable choices
memberlist.multiplable = "true";

// data 
memberlist.partment_data = {};
memberlist.member_data = {};
memberlist.getStaticData = function() {
        // get all static data
        postData.getdata('/api/team/department/', function(json) {
            if (json['code'] == 'success') {
                memberlist.partment_data = json['result'];
            } else {
                memberlist.errorTip(json['message']);
            }
        });
        postData.getdata('/api/team/member/', function(json) {
            if (json['code'] == 'success') {
                memberlist.member_data = json['result'];
            } else {
                memberlist.errorTip(json['message']);
            }
        });
    }
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
    $.each(memberlist.partment_data, function(index, obj) {
        $('#partment').append('<li class="list-group-item" data-partid="' + obj['id'] + '">' + obj['department_name'] + '</li>');
        $('#partment li').first().addClass('active');
    });
    $('#partment li').first().trigger('click');
}

memberlist.renderMemberlist = function(partmentId) {
    var data = (memberlist.triggerbutton.hasClass('select_chargers') == false) ? memberlist.data_participants : memberlist.data_chargers;
    $('#member').attr('title', partmentId).empty();
    // clear storage
    if (memberlist.multiplable == "false") {
        data = {};
    }
    $.each(memberlist.member_data, function(i, v) {
        if (v['department_id'] == partmentId) {
            var members = v['members'];
            $.each(members, function(i, o) {
                // recoard selection
                if (data.hasOwnProperty(o['id']) == true) {
                    $('#member').append('<li class="list-group-item active" data-userid="' + o['id'] + '">' + o['username'] + '</li>');
                } else {
                    $('#member').append('<li class="list-group-item" data-userid="' + o['id'] + '">' + o['username'] + '</li>');
                }
            });
        }
    });
}

memberlist.getSelectList = function() {
    var data = (memberlist.triggerbutton.hasClass('select_chargers') == false) ? memberlist.data_participants : memberlist.data_chargers;
    // clear storage
    if (memberlist.multiplable == "false") {
        data = {};
    }
    $('#member li').each(function() {
        var key = $(this).attr('data-userid'),
            value = $(this).html();
        if ($(this).hasClass('active')) {
            data[key] = value;
        } else {
            delete data[key];
        }
    });


    if (memberlist.triggerbutton.hasClass('select_chargers') == false) {
        memberlist.data_participants = data;
    } else {
        memberlist.data_chargers = data;
    }
}

memberlist.sendForward = function() {
    var data = (memberlist.triggerbutton.hasClass('select_chargers') == false) ? memberlist.data_participants : memberlist.data_chargers;
    var inputValue = memberlist.triggerbutton.parentsUntil('.col-sm-10').find('input').get(0),
        inputKey = memberlist.triggerbutton.parentsUntil('.col-sm-10').find('input').get(1);
    inputKey.value = '';
    inputValue.value = '';
    $.each(data, function(key, value) {
        inputKey.value += key + ',';
        inputValue.value += value + ',';
    });
    // remove last indefieder
    inputKey.value = inputKey.value.substr(0, inputKey.value.length - 1);
    inputValue.value = inputValue.value.substr(0, inputValue.value.length - 1);
    memberlist.modalhide();
    if (memberlist.triggerbutton.hasClass('select_chargers') == false) {
        memberlist.data_participants = {};
    } else {
        memberlist.data_chargers = {};
    }
    // memberlist.trigger = null;
}


// bind event
memberlist.init = function() {
    memberlist.getStaticData();
    $('.select_chargers,.select_participants').on('click', function() {
        if ($(this).attr('data-multiplable')) {
            memberlist.multiplable = $(this).attr('data-multiplable') == undefined ? "true" : $(this).attr('data-multiplable');
        }
        // remove event
        $('#member').off('click', 'li');
        if (memberlist.multiplable == "true") {
            console.log('multiplable');
            $('#member').on('click', 'li', function(event) {
                $(this).toggleClass('active');
                // get and update data
                memberlist.getSelectList();
            });
        } else {
            console.log('no multiplable');
            $('#member').on('click', 'li', function(event) {
                $('#member li').removeClass('active');
                $(this).addClass('active');
                // get and update data
                memberlist.getSelectList();
            });
        }
        memberlist.triggerbutton = $(this);
        memberlist.modalshow();
        memberlist.renderPartmentList();
    });
    // bind only once
    $('#partment').on('click', 'li', function() {
        var partmentId = $(this).attr('data-partid');
        // toggle class
        $('#partment li').removeClass('active');
        $(this).addClass('active');
        // render member list
        memberlist.renderMemberlist(partmentId);
    });
    $('#send-forward').on('click', function() {
        memberlist.sendForward();
    });
}