function assignForms() {
    fetch('/assign_forms', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById('response-message').textContent = data.message;
                document.getElementById('response-message').style.color = 'green';
                updateAgentStatuses(); // This function updates agent statuses on the front end
            } else if (data.error) {
                document.getElementById('response-message').textContent = data.error;
                document.getElementById('response-message').style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').textContent = 'An error occurred while assigning forms.';
            document.getElementById('response-message').style.color = 'red';
        });
}

// Run the assignForms function every 10 seconds (10000 milliseconds)
setInterval(assignForms, 5000);


document.querySelectorAll('.delete-agent').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way

        const agentId = this.getAttribute('data-agent-id');
        console.log('Deleting agent with ID:', agentId); // Debugging

        fetch('/delete_agent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'agent_id': agentId,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.getElementById('agent-' + agentId).remove(); // Ensure this element exists
                document.getElementById('response-message').textContent = data.message;
                document.getElementById('response-message').style.color = 'green';
            } else if (data.error) {
                document.getElementById('response-message').textContent = data.error;
                document.getElementById('response-message').style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').textContent = 'An error occurred while deleting the agent.';
            document.getElementById('response-message').style.color = 'red';
        });
    });
});

document.querySelectorAll('.update-priority-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const agentId = this.getAttribute('data-agent-id');
        const priority = this.querySelector('input[name="agent_priority"]').value;

        fetch('/update_agent_priority', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'agent_id': agentId,
                'agent_priority': priority,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.querySelector(`#agent-${agentId} td:nth-child(3)`).textContent = priority;
                document.getElementById('response-message').textContent = data.message;
                document.getElementById('response-message').style.color = 'green';
            } else if (data.error) {
                document.getElementById('response-message').textContent = data.error;
                document.getElementById('response-message').style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').textContent = 'An error occurred while updating agent priority.';
            document.getElementById('response-message').style.color = 'red';
        });
    });
});

document.querySelectorAll('.update-workload-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const agentId = this.getAttribute('data-agent-id');
        const workLoad = this.querySelector('input[name="agent_workload"]').value;

        fetch('/update_agent_workload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'agent_id': agentId,
                'agent_workload': workLoad,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                document.querySelector(`#agent-${agentId} td:nth-child(4)`).textContent = workLoad;
                document.getElementById('response-message').textContent = data.message;
                document.getElementById('response-message').style.color = 'green';
            } else if (data.error) {
                document.getElementById('response-message').textContent = data.error;
                document.getElementById('response-message').style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').textContent = 'An error occurred while updating agent queue length.';
            document.getElementById('response-message').style.color = 'red';
        });
    });
});

function updateAgentStatuses() {
    fetch('/agents_status')
        .then(response => response.json())
        .then(data => {
            data.agents.forEach(agent => {
                const statusCell = document.getElementById('status-' + agent.Agent_ID);
                if (statusCell) {
                    statusCell.textContent = agent.Agent_Status;
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').textContent = 'An error occurred while fetching agent statuses.';
            document.getElementById('response-message').style.color = 'red';
        });
}

function updateFormStatuses() {
    fetch('/form_status')
        .then(response => response.json())
        .then(data => {
            data.forms.forEach(form => {
                const statusCell = document.getElementById('status-' + form.Form_ID);
                if (statusCell) {
                    statusCell.textContent = form.Form_Status;
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').textContent = 'An error occurred while fetching form statuses.';
            document.getElementById('response-message').style.color = 'red';
        });
}



function fetchForms() {
    fetch('/forms')
        .then(response => response.json())
        .then(forms => {
            const tbody = document.getElementById('forms-table').querySelector('tbody');
            tbody.innerHTML = ''; // Clear existing table rows
            forms.forEach(form => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${form.Form_ID}</td>
                    <td>${form.Form_Type}</td>
                    <td>${form.Form_Detail}</td>
                    <td>${form.Form_Status}</td>
                    <td>${form.Assigned_Agent_ID}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').textContent = 'An error occurred while fetching forms.';
            document.getElementById('response-message').style.color = 'red';
        });
}

// Call fetchForms when the page loads
document.addEventListener('DOMContentLoaded', fetchForms);