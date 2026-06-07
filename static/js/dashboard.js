document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('meetingsChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Meetings',
                    data: [],
                    borderColor: '#0d6efd'
                }]
            }
        });
    }
});
