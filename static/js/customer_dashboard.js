$(document).ready(function() {
    $('#form-submission').on('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting normally
        $.ajax({
            type: 'POST',
            url: '/submit-form',
            data: $(this).serialize(), // Serialize form data
            success: function(response) {
                $('#response-message').text(response.message).css('color', 'green');
                // Optionally, clear the form fields after successful submission
                $('#form-submission')[0].reset();
            },
            error: function(xhr) {
                let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'An error occurred';
                $('#response-message').text(errorMessage).css('color', 'red');
            }
        });
    });
});