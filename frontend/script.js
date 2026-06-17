/*
 * Functions for opening/closing nav bar: send to Abby to check with her nav bar?
 */

function closeNav() {
    document.getElementById("sideNav").style.width = "0";
    document.getElementById("menuBtn").style.width = "inline";
}

function openNav() {
    document.getElementById("sideNav").style.width = "250px";
    document.getElementById("menuBtn").style.width = "none";
}

/*
 * Code for hardcoding values in histogram: will need to change with actual values once backend/database are up
 */

const ctx = document.getElementById('Histogram').getContext('2d');

const histogramChart = new Chart(ctx, {
    type: 'bar', 
    data: {
        labels: ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100'], 
        datasets: [{
            label: 'Frequency (Count)',
            data:[2, 5, 10, 7, 4, 5, 10, 15, 4, 19],
            backgroundColor: '#d6bf95ff',
            borderColor: '#cea863ff', 
            borderWidth: 1,
            barPercentage: 1.0,
            categoryPercentage: 1.0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                grid: {
                    display: false 
                },
                title: {
                    display: true,
                    text: 'People',
                    font: { size: 12, weight: 'bold' }
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Hours',
                    font: { size: 12, weight: 'bold' }
                }
            }
        }
    }
});