// Notifications JavaScript

// Update unread notification count
function updateUnreadCount() {
    fetch('/notifications/api/unread-count')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('unread-count');
            if (badge) {
                if (data.count > 0) {
                    badge.textContent = data.count;
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error fetching unread count:', error);
        });
}

// Poll for new notifications every 30 seconds
document.addEventListener('DOMContentLoaded', function() {
    updateUnreadCount();
    setInterval(updateUnreadCount, 30000); // Update every 30 seconds
});
