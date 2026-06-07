document.addEventListener('DOMContentLoaded', function() {
    // 1. Task Chart
    const taskCanvas = document.getElementById('taskChart');
    if (taskCanvas) {
        fetch('/analytics/data/tasks')
            .then(res => res.json())
            .then(data => {
                new Chart(taskCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: ['Pending', 'In Progress', 'Completed'],
                        datasets: [{
                            data: [data.pending, data.in_progress, data.completed],
                            backgroundColor: ['#ffc107', '#0dcaf0', '#198754']
                        }]
                    }
                });
            });
    }

    // 2. Relationship Charts (Score and Distribution)
    const relCanvas = document.getElementById('relationshipChart');
    const distCanvas = document.getElementById('relationshipDistChart');
    if (relCanvas || distCanvas) {
        fetch('/analytics/data/relationships')
            .then(res => res.json())
            .then(data => {
                if (relCanvas && data.individual_scores && data.individual_scores.length > 0) {
                    new Chart(relCanvas, {
                        type: 'bar',
                        data: {
                            labels: data.individual_scores.map(r => r.name.substring(0, 15)),
                            datasets: [{
                                label: 'Health Score',
                                data: data.individual_scores.map(r => r.score),
                                backgroundColor: '#0d6efd'
                            }]
                        }
                    });
                }
                if (distCanvas && data.distribution) {
                    new Chart(distCanvas, {
                        type: 'pie',
                        data: {
                            labels: ['Strong', 'Moderate', 'At Risk'],
                            datasets: [{
                                data: [data.distribution.strong, data.distribution.moderate, data.distribution.at_risk],
                                backgroundColor: ['#198754', '#0d6efd', '#dc3545']
                            }]
                        }
                    });
                }
            });
    }

    // 3. Meetings Chart
    const meetingsCanvas = document.getElementById('meetingsChart');
    if (meetingsCanvas) {
        fetch('/analytics/data/meetings')
            .then(res => res.json())
            .then(data => {
                new Chart(meetingsCanvas, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Meetings',
                            data: data.counts,
                            borderColor: '#20c997',
                            backgroundColor: 'rgba(32,201,151,0.1)'
                        }]
                    }
                });
            });
    }

    // 4. Completion Chart
    const completionCanvas = document.getElementById('completionChart');
    if (completionCanvas) {
        fetch('/analytics/data/completion')
            .then(res => res.json())
            .then(data => {
                new Chart(completionCanvas, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Completion Rate %',
                            data: data.rates,
                            borderColor: '#ffc107',
                            backgroundColor: 'rgba(255,193,7,0.08)'
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            });
    }

    // 5. Engagement Chart
    const engagementCanvas = document.getElementById('engagementChart');
    if (engagementCanvas) {
        fetch('/analytics/data/engagement')
            .then(res => res.json())
            .then(data => {
                new Chart(engagementCanvas, {
                    type: 'bar',
                    data: {
                        labels: data.labels.map(l => l.substring(0, 15)),
                        datasets: [{
                            label: 'Engagement %',
                            data: data.values,
                            backgroundColor: '#0dcaf0'
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            });
    }
});
