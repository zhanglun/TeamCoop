// setting module part
var settingModule = {};

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

// 个人设置
settingModule.personalSetting = function() {


};

//  admin成员设置
settingModule.memberSetting = function() {
    // render partment and user
    postData.postdata('/api/team/department/', {}, function(json) {
        console.log(json);
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
    settingModule.toggle();
    settingModule.memberDetail();
    settingModule.addperson('#partmentdetailform');
    settingModule.addperson('#newpartmentform');
    settingModule.resetModal();
})