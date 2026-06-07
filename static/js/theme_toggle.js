document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('themeToggle');
    const icon = document.getElementById('themeIcon');
    if (!toggle) return;

    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme') || 'light';

    toggle.addEventListener('click', function() {
        const newTheme = html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-bs-theme', newTheme);
        icon.className = newTheme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        
        // Sync theme with the database
        fetch('/settings/toggle-theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ theme: newTheme })
        }).catch(err => console.error('Failed to save theme to backend:', err));
    });
});
