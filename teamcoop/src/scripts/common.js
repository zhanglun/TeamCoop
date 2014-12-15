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
        cache: false,
        success: function(json) {
            callback(json);
        },
        error: function() {
            // something error
        }
    });
};

// ajax GET
postData.getdata = function(url, data, callback) {
    if (arguments.length == 3) {
        $.ajax({
            url: url,
            type: "GET",
            data: data,
            cache: false,
            success: function(json) {
                callback(json);
            },
            error: function() {
                // something error
            }
        });
    } else {
        $.ajax({
            url: url,
            type: "GET",
            cache: false,
            success: function(json) {
                // argument[1] =>  function
                data(json);
            },
            error: function() {
                // something error
            }
        });
    }
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
            input.parentsUntil('form', '.form-group').addClass('has-error');
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
            input.parentsUntil('form', '.form-group').addClass('has-error');
        }
    });
    $(':input').on('focus', function(event) {
        var input = $(event.target);
        input.parentsUntil('form').removeClass('has-error');
    });

    $(':password').last().on('blur', function(event) {
        var input = $(event.target);
        if ($(':password').first().val() != $(':password').last().val()) {
            input.parentsUntil('form', '.form-group').addClass('has-error');
        }
    });
});

// siderbar height auto change
$(function() {
    if (window.innerWidth >= 992) {
        setTimeout(function() {
            $('#main-nav').height(function() {
                return window.innerHeight > $(document).height() ? window.innerHeight : $(document).height();
            });
        }, 100);
    }
    $(window).on('resize', function() {
        if (window.innerWidth >= 992) {
            setTimeout(function() {
                $('#main-nav').height(function() {
                    return window.innerHeight > $(document).height() ? window.innerHeight : $(document).height();
                });
            }, 200);
        } else {
            $('#main-nav').height('auto');
        }
    });
});

var teamcoop = {};
teamcoop.hash = function(hash) {
    if (arguments.length == 0) {
        return window.location.hash;
    } else {
        window.location.hash = hash;
    }
}
teamcoop.refresh = function() {
    window.location.reload(false);
}