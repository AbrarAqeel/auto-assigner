//function updateStatus() {
//    // Logic to update agent status
//    console.log('Status updated');
//}
//
//function confirmFormSubmission() {
//    const checkbox = document.getElementById('confirmCheckbox');
//    if (checkbox.checked) {
//        const confirmed = confirm("Are you sure you want to submit this form?");
//        if (confirmed) {
//            // Logic to submit the form
//            console.log('Form submission confirmed');
//        } else {
//            console.log('Form submission canceled');
//        }
//    } else {
//        alert("Please confirm that you want to submit this form.");
//    }
//}


// Function to update agent status
function updateStatus() {
    const agentId = document.getElementById('agent_id').innerText;
    const newStatus = document.getElementById('agent_status').value;

    fetch('/update_agent_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            agent_id: agentId,
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Status updated to ' + newStatus);
        } else {
            alert('Failed to update status.');
        }
    })
    .catch(error => {
        console.error('Error updating status:', error);
    });
}

// Function to load agent data
function loadAgentData() {
    const agentId = document.getElementById('agent_id').innerText;

    fetch(`/get_agent_data/${agentId}`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('agent_name').innerText = data.agent_name;
            document.getElementById('agent_status').value = data.agent_status;
        } else {
            alert('Failed to load agent data.');
        }
    })
    .catch(error => {
        console.error('Error loading agent data:', error);
    });
}

// Function to load form data
function loadFormData() {
    const agentId = document.getElementById('agent_id').innerText;

    fetch(`/get_form_data/${agentId}`)
    .then(response => response.json())
    .then(data => {
        if (data.success && data.form) {
            document.getElementById('form_id').innerText = data.form.form_id;
            document.getElementById('form_type').innerText = data.form.form_type;
            document.getElementById('form_detail').innerText = data.form.form_description;
        } else {
            document.querySelector('.form-details').style.display = 'none';
            alert('No forms assigned.');
        }
    })
    .catch(error => {
        console.error('Error loading form data:', error);
    });
}

// Function to confirm form submission
function confirmFormSubmission() {
    const checkbox = document.getElementById('confirmCheckbox');
    const formId = document.getElementById('form_id').innerText;

    if (checkbox.checked) {
        const confirmed = confirm("Are you sure you want to submit this form?");
        if (confirmed) {
            fetch('/complete_form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    form_id: formId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Form submission successful!');
                    document.getElementById('agent_status').value = 'Available';
                    loadFormData();
                } else {
                    alert('Form submission failed.');
                }
            })
            .catch(error => {
                console.error('Error during form submission:', error);
            });
        } else {
            console.log('Form submission canceled');
        }
    } else {
        alert("Please confirm that you want to submit this form.");
    }
}
