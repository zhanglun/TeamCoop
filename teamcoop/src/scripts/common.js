var postData = {};

postData.getData = function(formSelector) {
    var fields = $(formSelector + ' :input').serializeArray();
    // var fields = $('.form-horizontal').serializeArray()
    // array of form-data
    var data = {};
    $.each(fields, function(index, obj) {
        var name = obj.name,
            value = obj.value;
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
}

// confirm input of required 
$(function(){
    $(':input').on('blur',function(event){

    });
});




// setting module part
var settingModule = {};

// 个人设置
settingModule.personalSetting = function(){}
//  admin成员设置
settingModule.memberSetting = function(){}
