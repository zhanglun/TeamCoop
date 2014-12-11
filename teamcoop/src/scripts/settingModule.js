// setting module part
var settingModule = {};

settingModule.partmentList = {};
settingModule.memberList = {};
// data
settingModule.getStaticData = function() {
    postData.getdata('/api/team/department/', function(json) {
        if (json['code'] == 'success') {
            settingModule.partmentList = json['result'];
            // render partmentlist
            settingModule.memberSetting();
        } else {
            memberlist.errorTip(json['message']);
        }
    });
    postData.getdata('/api/team/member/', function(json) {
        if (json['code'] == 'success') {
            settingModule.memberList = json['result'];
            settingModule.memberDetail();
        } else {
            memberlist.errorTip(json['message']);
        }
    });

}

// toggle selection
settingModule.toggle = function() {
    $('.setting_select button').on('click', function(event) {
        var name = $(event.target).attr('data-target');
        $('.member-setting,.personal-setting').hide();
        $('.' + name).show();
    });
}

// add_name
settingModule.addperson = function(formselector) {
    $(formselector).on('focus', 'input', function(event) {
        var eventObj = $(event.target);
        if (eventObj.parentsUntil('form', '.form-group').index() == ($(formselector + ' .form-group').size() - 1)) {
            $(formselector).append($(formselector + ' .form-group').last().find('button').show().end().clone());
        }
        $(formselector + ' button').last().hide();
    });
    $(formselector).on('click', 'button', function(event) {
        var eventObj = $(event.target);
        eventObj.parentsUntil('form', '.form-group').remove();
        $(formselector + ' button').last().hide();
    });
    $(formselector + ' button').last().hide();
}

// personSetting
settingModule.personalSetting = function() {


};

//  admin成员设置
settingModule.memberSetting = function() {
    // render partment and user
    $('#partmentList tbody').empty();
    $.each(settingModule.partmentList, function(index, obj) {
        $('#partmentList tbody').append('<tr><td><a href="javascript:void(0);" data-partid="' + obj['id'] + '">' + obj['department_name'] + '</a></td><td>' + obj['counts'] + '</td><td><button class="btn btn-xs btn-danger">delete</button></td></tr>');
    });
};

// 部门详情
settingModule.memberDetail = function() {

    $('#partmentList').on('partment.click', 'a', function(event) {
        var eventObj = $(event.target);
        var partid = eventObj.attr('data-partid'),
            partname = eventObj.html();
        $('#partmentDetail').modal('show');
        // get partment id and get the detail of partment
        $('#partmentDetail h4').html(partname);
        $('#partmentDetail form').attr('data-partid', partid);
        $.each(settingModule.memberList, function(index, obj) {
            if (obj['department_id'] == partid) {
                $.each(obj['members'], function(i, o) {
                    $('#partmentDetail form').prepend('<div class="form-group"><label class="col-sm-2 control-label">姓名</label><div class="col-sm-8"><p class="form-control-static">' + o['username'] + '</p></div> <div class="col-sm-2"><button class="btn btn-danger btn-sm" data-userid="' + o['id'] + '">delete</button></div>');
                });
            }
        });
    });
}

settingModule.addpartment = function() {
    var data = postData.getData('#newpartmentform');
    // members to array
    if (typeof data.members == 'string') {
        data.members = data.members.split(',');
    }
    postData.postdata('/api/team/department/', data, function(json) {
        $('#createPartment').modal('hide');
        // render new partmentlist
        postData.getdata('/api/team/department/', function(json) {
            if (json['code'] == 'success') {
                settingModule.partmentList = json['result'];
                // render partmentlist
                settingModule.memberSetting();
            } else {
                memberlist.errorTip(json['message']);
            }
        });
        postData.getdata('/api/team/member/', function(json) {
            if (json['code'] == 'success') {
                settingModule.memberList = json['result'];
            } else {
                // $('#newpartmentform>div').first().addClass('has-error');
                memberlist.errorTip(json['message']);
            }
        });
    });
}

settingModule.delpartment = function(event) {
    var eventObj = $(event.target),
        partmentId = eventObj.parentsUntil('tbody').find('a').attr('data-partid'),
        partmentName = eventObj.parentsUntil('tbody').find('a').html();
    if (postData.confirm('确认删除' + partmentName + '吗?') == true) {
        var data = {
            "department_id": partmentId
        };
        data = JSON.stringify(data);
        postData.deletedata('/api/team/department/', data, function(json) {
            console.log(json);
        });
    }
}

settingModule.addmember = function() {
    var data = postData.getData('#partmentdetailform');
    // members to array
    if (typeof data.members == 'string') {
        data.members = data.members.split(',');
    }
    data["department_id"] = parseInt($('#partmentdetailform').attr('data-partid'));
    data = JSON.stringify(data);
    console.log(data);
    postData.postdata('/api/department/detail/member/', data, function(json) {
        $('#partmentDetail').modal('hide');
    });
}


settingModule.resetModal = function() {
    $('.modal').on('hidden.bs.modal', function() {
        var divs = $(this).find('form>div');
        divs.each(function(index) {
            // clear val in input
            $(this).has('.form-control-static').remove();
            $(this).find('input').val('');
            if (index == 0 || index == divs.size() - 1) {
                return;
            } else {
                $(this).remove();
            }
        });
    });
}

$(function() {
    settingModule.getStaticData();
    settingModule.toggle();
    settingModule.addperson('#partmentdetailform');
    settingModule.addperson('#newpartmentform');
    settingModule.resetModal();
    // new partment event bind
    $('#department_btn').on('click', settingModule.addpartment);
    // new member event bind
    $('#partmentDetail_btn').on('click', settingModule.addmember);
    // partment detail event bind
    $('#partmentList').on('click', 'button', settingModule.delpartment);
});