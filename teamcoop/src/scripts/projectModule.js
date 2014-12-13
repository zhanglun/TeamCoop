var projectModule = {};

projectModule.userid = $('#usertoggle').attr('data-userid');
// default project id
projectModule.projectid = "1";
projectModule.getProjectId = function() {
    projectModule.projectid = $('.nav-title').attr('data-project-id');
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

projectModule.addMember = function() {
    $('#add_btn').on('click', function() {
        $('#addMemberModal').modal('show');
    });
    $('#addmember_btn').on('click', function() {
        var data = postData.getData('#addmember_form');
        if (data.hasOwnProperty('members') == true) {
            data.members = data.members.split(',');
        }
        if (data.hasOwnProperty('person_in_charge') == true) {
            data.person_in_charge = data.person_in_charge.split(',');
        }
    });
}

projectModule.personalIssue = function() {
    var data = {
        "user_id": projectModule.userid,
        "project_id": projectModule.projectid,
    };
    postData.getdata('/api/user/project/task/', data, function(json) {
        // console.log(json);
        var array_create = json['result']['tasks']['create'],
            array_excute = json['result']['tasks']['execute'];
        $('#asignToMe tbody,#asignByMe tbody').empty();
        $.each(array_excute, function(index, obj) {
            var status = obj['status'];
            $('#asignToMe tbody').append('<tr data-issueid="' + obj['id'] + '"><td><a href="javascript:void(0);">' + obj['title'] + '</a></td><td>12</td><td>' + obj['create_user_id'] + '</td><td><select name="" id="" class="form-control"><option value="finished">finished</option><option value="unfinish">unfinish</option><option value="executed">executed</option></select></td><td><button type="button" class="btn btn-danger btn-xs">delete</button></td></tr>');
            $('#asignToMe tbody tr').last().find('option').eq(status - 1).attr('selected', 'selected');
        });
        $.each(array_create, function(index, obj) {
            var status = obj['status'];
            $('#asignByMe tbody').append('<tr data-issueid="' + obj['id'] + '"><td><a href="javascript:void(0);" >' + obj['title'] + '</a></td><td>12</td><td>' + obj['execute_user_id'] + '</td><td><select name="" id="" class="form-control"><option value="finished">finished</option><option value="unfinish">unfinish</option><option value="executed">executed</option></select></td><td><button type="button" class="btn btn-danger btn-xs">delete</button></td></tr>');
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
            projectModule.personalIssue();
        });
    } else {
        return false;
    }
}

projectModule.changeIssueStatus = function() {
    $('#asignToMe,#asignByMe').on('change', 'select', function(event) {
        var index = $(event.target).find(':selected').index() + 1,
            issueId = $(event.target).parentsUntil('tbody', 'tr').attr('data-issueid');
        // todo post and change 
    });
}

projectModule.deleteIssue = function() {
    $('#asignToMe,#asignByMe').on('click', 'button', function(event) {
        var issueId = $(event.target).parentsUntil('tbody', 'tr').attr('data-issueid'),
            data = {
                "project_id": projectModule.projectid,
                "task_id": issueId
            };
        console.log(data);
        if (postData.confirm('确认删除吗?') == true) {
            postData.postdata('/api/project/task/trash/', data, function(json) {
                project.removeIssue(issueId);
            });
        } else {
            return false;
        }
    });
}

projectModule.issueDetail = function(id) {
    $('#issueDetail').modal('show');
    // todo
}

projectModule.removeIssue = function(id) {
    $('[data-issueid="' + id + '"]').remove();
}

projectModule.resetModal = function() {
    $('.modal').on('hidden.bs.modal', function() {
        var divs = $(this).find('form>div');
        divs.each(function(index) {
            $(this).removeClass('has-error');
            $(this).find('input').val('');
        });
    });
}
$(function() {
    // get project id
    projectModule.getProjectId();
    // render  task list
    projectModule.personalIssue();
    projectModule.resetModal();
    // delete issue event bind
    projectModule.deleteIssue();
    // select event bind
    projectModule.changeIssueStatus();
    // addmember 
    projectModule.addMember();
    // new issue event bind
    $('#btnCreateIssue').on('click', projectModule.newIssue);
    // issue detail 
    $('#asignToMe,#asignByMe').on('click', 'a', function(event) {
        var issueid = $(event.target).parentsUntil('tbody', 'tr').attr('data-issueid');
        projectModule.issueDetail(issueid);
    });
    // new project btn event bind
    $('#project_btn').on('click', projectModule.newProject);
});