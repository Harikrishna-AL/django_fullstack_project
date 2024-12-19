// Chart.js Initialization
document.addEventListener("DOMContentLoaded", function () {
    // Visitors Chart
    new Chart(document.getElementById('visitorsChart'), {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            datasets: [{
                label: 'Visitors',
                data: [100, 200, 400, 800, 600],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                tension: 0.2
            }]
        }
    });

    // Success Rate Chart
    new Chart(document.getElementById('successRateChart'), {
        type: 'bar',
        data: {
            labels: ['Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4', 'Quiz 5'],
            datasets: [{
                label: 'Success Rate (%)',
                data: [65, 70, 80, 75, 90],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderWidth: 1
            }]
        }
    });

    // Participation Breakdown (Pie Chart)
    new Chart(document.getElementById('participationChart'), {
        type: 'doughnut',
        data: {
            labels: ['Beginner', 'Intermediate', 'Advanced'],
            datasets: [{
                data: [40, 35, 25],
                backgroundColor: ['#36a2eb', '#ffcd56', '#ff6384'],
            }]
        }
    });

    // Net Retention Rate (Bar Chart)
    new Chart(document.getElementById('retentionChart'), {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            datasets: [{
                label: 'Net Retention (%)',
                data: [90, 85, 80, 78, 88],
                backgroundColor: '#4caf50'
            }]
        }
    });

    // User Engagement Chart (Bar Chart)
    new Chart(document.getElementById('engagementChart'), {
        type: 'bar',
        data: {
            labels: ['Monthly', 'Yearly'],
            datasets: [{
                label: 'Engagement',
                data: [70, 85],
                backgroundColor: ['#007bff', '#6c757d']
            }]
        }
    });
});
