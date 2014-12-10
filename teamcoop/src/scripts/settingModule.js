// setting module part
var settingModule = {};

settingModule.partmentList = {};
settingModule.memberList = {};
// data
settingModule.getStaticData = function() {
    postData.getdata('/api/team/department/', function(json) {
        if (json['code'] == 'success') {
            settingModule.partmentList = json['result'];
        } else {
            memberlist.errorTip(json['message']);
        }
        postData.getdata('/api/team/member/', function(json) {
            if (json['code'] == 'success') {
                settingModule.memberList = json['result'];
            } else {
                memberlist.errorTip(json['message']);
            }
            postData.getdata('/api/team/member/', function(json) {
                if (json['code'] == 'success') {
                    settingModule.memberList = json['result'];
                } else {
                    memberlist.errorTip(json['message']);
                }
            });
        });
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
    console.log(settingModule.partmentList);
    // render partment and user
    $.each(settingModule.partmentList, function(index, obj) {
        $('#partmentList tbody').empty();
        $('#partmentList tbody').append('<tr><td><a href="javascript:void(0);" data-partid="' + obj['id'] + '">' + obj['partmentName'] + '</a></td><td>2</td><td><button class="btn btn-xs btn-danger">delete</button></td></tr>')
    });
};
// 部门详情
settingModule.memberDetail = function() {
    $('#partmentList').on('click', 'a', function(event) {
        var eventObj = $(event.target);
        $('#partmentDetail').modal('show');
        // get partment id and get the detail of partment 
    });

}

settingModule.resetModal = function() {
    $('.modal').on('hidden.bs.modal', function() {
        var divs = $(this).find('form>div');
        divs.each(function(index) {
            // clear val in input
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
    settingModule.memberDetail();
    settingModule.addperson('#partmentdetailform');
    settingModule.addperson('#newpartmentform');
    settingModule.resetModal();


})