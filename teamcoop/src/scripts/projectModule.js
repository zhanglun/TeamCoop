var projectModule = {};

projectModule.getProjectId = function() {


}

projectModule.setStep = function() {
    var step = $('.progressBar').attr('data-step'),
        data = {
            "project_id": 1,
            "status": step
        };
    postData.postdata('/api/project/detail/status/', data, function(json) {
        console.log(json);
    });
}