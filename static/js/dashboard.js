$(document).ready(function() {
    $('#custom-url-link').click(function(e) {
        e.preventDefault();
        $('#custom-url-input').toggle();
    });

    $('#change-username-link').click(function(e) {
        e.preventDefault();
        $('#username-update-form').toggle();
    });

    $('#change-password-link').click(function(e) {
        e.preventDefault();
        $('#password-update-form').toggle();
    });

    $('#delete-account-link').click(function(e) {
        e.preventDefault();
        var confirm = window.confirm('Are you sure you want to delete this account?')
        
        if (confirm) $('#delete-account-form').submit();
    })
});