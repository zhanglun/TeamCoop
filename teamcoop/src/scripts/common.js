$(function() {
    // set modal initializes
    $('.modal').modal({
        'backdrop': 'static',
        'keyboard': false,
        'show': false // show when modal initializes
    });
    // datepicker init
    $(".form_datetime").datetimepicker({
        format: "dd MM yyyy - hh:ii",
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
        dataType: "json",
        success: function(json) {
            callback(json);
        },
        error: function() {
            // something error
        }
    });
};

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
            console.log(input.parentsUntil('form').get(0));
            input.parentsUntil('form').addClass('has-error');
        }
    });
});

// setting module part
var settingModule = {};

// 个人设置
settingModule.personalSetting = function() {};
//  admin成员设置
settingModule.memberSetting = function() {
    // add user
    var url = "/api/team/member/";


};