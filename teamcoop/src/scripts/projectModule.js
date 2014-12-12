var projectModule = {};

projectModule.userid = "1";
projectModule.projectid = "1";
projectModule.getProjectId = function() {


}

projectModule.setStep = function() {
    var step = $('.progressBar').attr('data-step'),
        data = {
            "project_id": projectModule.userid,
            "status": step
        };
    postData.postdata('/api/project/detail/status/', data, function(json) {
        console.log(json);
    });
}

projectModule.personalIssue = function() {
    var userid = $('#usertoggle').attr('data-userid'),
        data = {
            "user_id": projectModule.userid,
            "project_id": projectModule.projectid,
        };
    postData.getdata('/api/user/project/task/', data, function(json) {
        console.log(json);
        $.each(json['create'], function(index, obj) {
                $('#asignToMe').empty();
                $('#asignToMe').append('<tr><td><a href="">frontend</a></td><td>12</td><td>A</td><td><select name="" id="" class="form-control"><option value="finished">finished</option><option value="unfinish">unfinish</option><option value="executed">executed</option></select></td><td><button class="btn btn-danger btn-xs">delete</button></td></tr>');

        });

    });
}

$(function() {
    projectModule.personalIssue();

});