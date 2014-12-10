$(function() {
    // set modal initializes
    $('.modal').modal({
        'backdrop': 'static',
        'keyboard': false,
        'show': false // show when modal initializes
    });
    // datepicker init
    $(".form_datetime").datetimepicker({
        format: "yyyy-mm-ddThh:ii:ssZ",
        autoclose: true,
        startDate: new Date()
    });
})

var postData = {};

postData.getData = function(formSelector) {
    var fields = $(formSelector + ' :input').serializeArray();
    // var fields = $('.form-horizontal').serializeArray()
    // array of form-data
    var data = {};
    $.each(fields, function(index, obj) {
        var name = obj.name,
            value = obj.value;
        if ($.trim(value) == '') {
            return;
        }
        if (data.hasOwnProperty(name) == false) {
            data[name] = value;
        } else if ($.isArray(data[name]) == true) {
            // update value
            data[name].push(value);
        } else {
            // new array and push oldvalue
            var oldvalue = data[name];
            data[name] = new Array();
            data[name].push(oldvalue);
            data[name].push(value);
        }
    });
    return data;
};

postData.postdata = function(url, data, callback) {
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        contentType: 'application/json;charset=UTF-8',
        success: function(json) {
            callback(json);
        },
        error: function() {
            // something error
        }
    });
};

postData.getdata = function(url, callback) {
    $.ajax({
        url: url,
        type: "GET",
        success: function(json) {
            callback(json);
        },
        error: function() {
            // something error
        }
    });
};

// check form input, return boolean
postData.checkForm = function(formSelector) {
    return $(formSelector + '>div').hasClass('has-error');
}

// confirm input of required 
$(function() {
    $(':input').on('blur', function(event) {
        var input = $(event.target);
        // required
        if (input.attr('required') == 'required' && $.trim(input.val()) == '') {
            input.parentsUntil('form').addClass('has-error');
        }
    });
    $(':input').on('focus', function(event) {
        var input = $(event.target);
        input.parentsUntil('form').removeClass('has-error');
    });

    $(':password').last().on('blur', function(event) {
        var input = $(event.target);
        if ($(':password').first().val() != $(':password').last().val()) {
            input.parentsUntil('form').addClass('has-error');
        }
    });
});

// setting module part
var settingModule = {};

// 个人设置
settingModule.personalSetting = function() {


};
//  admin成员设置
settingModule.memberSetting = function() {
    // add partment and user
    // postData.postdata('/api/team/department/', {}, function (json) {
    // console.log(json);
    // });
};
settingModule.memberSetting();

// new project btn event bind
$('#project_btn').on('click', function() {
    if (postData.checkForm('#project_form')) {
        return false;
    }
    // check success
    var data = postData.getData('#project_form');
    // string to array
    if (data.hasOwnProperty('members') == true) {
        data.members = data.members.split(',');
    }
    if (data.hasOwnProperty('person_in_charge') == true) {
        data.person_in_charge = data.person_in_charge.split(',');
    }
    if (data.hasOwnProperty('is_public') == true) {
        // checked ispublic
        data.person_in_charge = 1;
    }else{
        // not checked is public 
        data.person_in_charge = 2;
    }

    // data add userid
    data['creater_id'] = $('[data-userid]').attr('data-userid');
    // data ispublic 
    data = JSON.stringify(data);
    postData.postdata('/api/user/project/', data, function(json) {
        console.log(json);
        if (json['code'] == 'success') {
            $('#createProject :input').val('');
            $('#createProject').modal('hide');
        } else {
            alert(json['message']);
        }
    });
});