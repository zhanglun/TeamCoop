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
// ajax POST
postData.postdata = function(url, data, callback) {
    data = JSON.stringify(data);
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

// ajax GET
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

// ajax DELETE
postData.deletedata = function(url, data, callback) {
    $.ajax({
        url: url,
        type: "DELETE",
        data: data,
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
    $(formSelector + ' :input').each(function(index, obj) {
        var input = $(obj);
        // required
        if (input.attr('required') == 'required' && $.trim(input.val()) == '') {
            input.parentsUntil('form').addClass('has-error');
        }
    });
    return $(formSelector + '>div').hasClass('has-error');
}

// confirm 
postData.confirm = function(text) {
    return confirm(text);
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
        data.is_public = 1;
    } else {
        // not checked is public 
        data.is_public = 2;
    }
    // data add userid
    data['creater_id'] = $('[data-userid]').attr('data-userid');
    postData.postdata('/api/user/project/', data, function(json) {
        if (json['code'] == 'success') {
            $('#createProject :input').val('');
            $('#createProject').modal('hide');
        } else {
            alert(json['message']);
        }
    });
});