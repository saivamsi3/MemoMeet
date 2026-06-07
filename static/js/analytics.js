document.addEventListener('DOMContentLoaded', function () {
    // Configure dynamic Chart.js defaults based on active theme
    const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
    const textColor = isDark ? '#cbd5e1' : '#475569';
    const gridColor = isDark ? 'rgba(255,255,255,0.07)' : '#e2e8f0';
    const cardBg = isDark ? '#1e2535' : '#ffffff';

    Chart.defaults.color = textColor;
    if (Chart.defaults.scale && Chart.defaults.scale.grid) {
        Chart.defaults.scale.grid.color = gridColor;
    }
    if (Chart.defaults.scale && Chart.defaults.scale.ticks) {
        Chart.defaults.scale.ticks.color = textColor;
    }
    if (Chart.defaults.plugins && Chart.defaults.plugins.legend && Chart.defaults.plugins.legend.labels) {
        Chart.defaults.plugins.legend.labels.color = textColor;
    }

    // ─── 1. FullCalendar ───────────────────────────────────────────────────────
    const calendarEl = document.getElementById('meetingCalendar');
    if (calendarEl) {
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,listMonth'
            },
            height: 'auto',
            eventSources: [{
                url: '/analytics/data/calendar',
                failure: function () {
                    console.warn('Failed to load calendar events.');
                }
            }],
            eventDidMount: function (info) {
                // Tooltip with meeting title
                info.el.setAttribute('title', info.event.title);
                info.el.setAttribute('data-bs-toggle', 'tooltip');
                // Bootstrap tooltip init
                if (window.bootstrap && bootstrap.Tooltip) {
                    new bootstrap.Tooltip(info.el, { placement: 'top', trigger: 'hover' });
                }
            },
            eventClick: function (info) {
                info.jsEvent.preventDefault();
                if (info.event.url) {
                    window.location.href = info.event.url;
                }
            },
            // Render past events subtler
            eventContent: function (arg) {
                const isPast = arg.event.extendedProps.isPast;
                return {
                    html: `<div class="fc-event-main-frame" style="opacity:${isPast ? 0.75 : 1}">
                               <div class="fc-event-title-container">
                                   <div class="fc-event-title fc-sticky">${arg.event.title}</div>
                               </div>
                           </div>`
                };
            },
            // Theme-aware colours
            dayCellDidMount: function (info) {
                info.el.style.backgroundColor = '';
            },
        });
        calendar.render();
    }

    // ─── 2. Task Status Doughnut Chart ────────────────────────────────────────
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
                            backgroundColor: ['#f59e0b', '#0ea5e9', '#10b981'],
                            borderWidth: 0,
                            hoverOffset: 8
                        }]
                    },
                    options: {
                        cutout: '65%',
                        plugins: {
                            legend: { position: 'bottom' }
                        }
                    }
                });
            });
    }

    // ─── 3. Meetings History Line Chart ───────────────────────────────────────
    const meetingsCanvas = document.getElementById('meetingsChart');
    if (meetingsCanvas) {
        fetch('/analytics/data/meetings')
            .then(res => res.json())
            .then(data => {
                new Chart(meetingsCanvas, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Meetings',
                            data: data.counts,
                            backgroundColor: 'rgba(99,102,241,0.7)',
                            borderColor: '#6366f1',
                            borderWidth: 1,
                            borderRadius: 6
                        }]
                    },
                    options: {
                        scales: {
                            y: { beginAtZero: true, ticks: { stepSize: 1 } }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            });
    }

    // ─── 4. Completion Rate Line Chart ────────────────────────────────────────
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
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16,185,129,0.10)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointBackgroundColor: '#10b981'
                        }]
                    },
                    options: {
                        scales: {
                            y: { beginAtZero: true, max: 100 }
                        },
                        plugins: { legend: { display: false } }
                    }
                });
            });
    }

    // ─── 5. Meeting Timeline Split (Past vs Future) Doughnut ─────────────────
    const splitCanvas = document.getElementById('timelineSplitChart');
    if (splitCanvas) {
        fetch('/analytics/data/calendar')
            .then(res => res.json())
            .then(events => {
                const past = events.filter(e => e.extendedProps && e.extendedProps.isPast).length;
                const future = events.length - past;
                new Chart(splitCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: ['Past Meetings', 'Upcoming Meetings'],
                        datasets: [{
                            data: [past, future],
                            backgroundColor: ['rgba(100,116,139,0.7)', 'rgba(99,102,241,0.85)'],
                            borderWidth: 0,
                            hoverOffset: 8
                        }]
                    },
                    options: {
                        cutout: '65%',
                        plugins: {
                            legend: { position: 'bottom' }
                        }
                    }
                });
            });
    }
});
