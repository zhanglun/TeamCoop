var projectModule = {};

projectModule.userid = $('#usertoggle').attr('data-userid');
projectModule.projectid = "1";
projectModule.getProjectId = function() {


}

projectModule.newProject = function() {
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
}
projectModule.setStep = function() {
    var step = $('.progressBar').attr('data-step'),
        data = {
            "project_id": projectModule.userid,
            "project_status": step
        };
    postData.postdata('/api/project/detail/status/', data, function(json) {
        console.log(json);
    });
}

projectModule.personalIssue = function() {
    var data = {
        "user_id": projectModule.userid,
        "project_id": projectModule.projectid,
    };
    postData.getdata('/api/user/project/task/', data, function(json) {
        console.log(json);
        var array_create = json['result']['tasks']['create'],
            array_excute = json['result']['tasks']['execute'];
        $('#asignToMe tbody,#asignByMe tbody').empty();
        $.each(array_excute, function(index, obj) {
            var status = obj['status'];
            $('#asignToMe tbody').append('<tr><td><a href="">' + obj['title'] + '</a></td><td>12</td><td>' + obj['create_user_id'] + '</td><td><select name="" id="" class="form-control"><option value="finished">finished</option><option value="unfinish">unfinish</option><option value="executed">executed</option></select></td><td><button type="button" class="btn btn-danger btn-xs" data-issueid="' + obj['id'] + '">delete</button></td></tr>');
            $('#asignToMe tbody tr').last().find('option').eq(status - 1).attr('selected', 'selected');
        });
        $.each(array_create, function(index, obj) {
            var status = obj['status'];
            $('#asignByMe tbody').append('<tr data-issueid="' + obj['id'] + '"><td><a href="" >' + obj['title'] + '</a></td><td>12</td><td>' + obj['execute_user_id'] + '</td><td><select name="" id="" class="form-control"><option value="finished">finished</option><option value="unfinish">unfinish</option><option value="executed">executed</option></select></td><td><button type="button" class="btn btn-danger btn-xs">delete</button></td></tr>');
            $('#asignByMe tbody tr').last().find('option').eq(status - 1).attr('selected', 'selected');
        });

    });
}

projectModule.newIssue = function() {
    var data = postData.getData('#createIssueForm');
    data['project_id'] = projectModule.projectid;
    // string to array
    if (data.hasOwnProperty('execute_user_id') == true) {
        data.execute_user_id = data.execute_user_id.split(',');
    }
    if (postData.checkForm('#createIssueForm') == false) {
        postData.postdata('/api/project/task/', data, function(json) {
            // console.log(json);
            $('#createIssue').modal('hide');
        });
    } else {
        return false;
    }
}


projectModule.resetModal = function() {
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
    projectModule.personalIssue();
    projectModule.resetModal();
    // new issue event bind
    $('#btnCreateIssue').on('click', projectModule.newIssue);
    // new project btn event bind
    $('#project_btn').on('click', projectModule.newProject);
});