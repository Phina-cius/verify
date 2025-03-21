// static/js/admin_dashboard.js
function approveManufacturer(manufacturerId) {
    fetch(`/approve-manufacturer/${manufacturerId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Ensure CSRF token is included
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Manufacturer approved successfully!');
            location.reload();  // Reload the page to reflect changes
        } else {
            alert('Failed to approve manufacturer.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}