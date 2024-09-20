document.getElementById("checkTraffic").addEventListener("click", function() {
    fetch('/traffic-status')
        .then(response => response.json())
        .then(data => {
            // Update the text content with traffic stats
            const statusMessage = document.getElementById("trafficStatus");
            statusMessage.innerText = "Current Traffic: " + data.status;
            statusMessage.style.display = "block";

            // Update traffic statistics in the dashboard
            document.getElementById("requestCount").innerText = "Total Requests: " + data.total_requests;
            document.getElementById("uniqueIps").innerText = "Unique IPs: " + data.unique_ips;

            // Smooth transition for displaying the stats
            statusMessage.classList.add('fade-in');

            // Update the traffic chart
            const ctx = document.getElementById("trafficChart").getContext("2d");
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.time_stamps,
                    datasets: [{
                        label: 'Requests per minute',
                        data: data.request_rates,
                        borderColor: 'rgba(46, 204, 113, 1)',
                        backgroundColor: 'rgba(46, 204, 113, 0.2)',
                        borderWidth: 2,
                        fill: true
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            const statusMessage = document.getElementById("trafficStatus");
            statusMessage.innerText = "Failed to fetch traffic status.";
            statusMessage.style.display = "block";
            statusMessage.style.color = "red";
        });
});
