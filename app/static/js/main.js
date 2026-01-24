// Main JavaScript for FFSmart

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
});

// Confirm dialogs for destructive actions
function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}

// API helper functions
const API = {
    baseURL: '',
    
    async get(endpoint) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            credentials: 'same-origin'
        });
        return response.json();
    },
    
    async post(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async put(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
            body: JSON.stringify(data)
        });
        return response.json();
    }
};
