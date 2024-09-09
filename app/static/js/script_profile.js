function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all tab content
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove the active class from all tabs
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    // Show the selected tab content and add the active class to the tab
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Automatically open the first tab
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".tab").click();

    // Pie chart logic
    var ctx = document.getElementById('pieChart').getContext('2d');
    var pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Победы', 'Поражения', 'Ничьи'],
            datasets: [{
                data: [30, 15, 5],
                backgroundColor: ['#4CAF50', '#FF3A00', '#FFD700'],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });
});
