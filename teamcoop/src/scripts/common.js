var postData = {};

postData.createProject = function(formSelector) {
    $(formSelector + ' :input').serializeArray();
    var fields = $('.form-horizontal').serializeArray()
        // array of form-data
    var data = {};
    $.each(fields, function(index, obj) {
        var name = obj.name,
            value = obj.value;
        console.log('participants:' + data['participants']);
        if (data.hasOwnProperty(name) == false) {
            data[name] = value;
        } else if ($.isArray(data[name]) == true) {
            console.log(33)
                // data[name] = data[name].push(value);
        } else {
            data[name] = [value];
        }
    });
    console.log(data);
}
