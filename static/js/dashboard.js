document.addEventListener("DOMContentLoaded", function() {
    if (typeof trendData !== "undefined" && trendData.length > 0) {
        renderTrendChart();
    }

    if (typeof categoryData !== "undefined" && categoryData.length > 0) {
        renderCategoryChart();
    }
});

function getValue(item, key) {
    return item[key] || item[key.toLowerCase()] || 0;
}

function renderTrendChart() {
    const ctx = document.getElementById("trendChart");
    if (!ctx) return;

    const labels = trendData.map(item => item.month);
    const income = trendData.map(item => getValue(item, "Income"));
    const expenses = trendData.map(item => getValue(item, "Expense"));
    const profit = trendData.map(item => getValue(item, "Profit"));

    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                { label: "Revenue", data: income, borderWidth: 3, tension: 0.4 },
                { label: "Expenses", data: expenses, borderWidth: 3, tension: 0.4 },
                { label: "Profit", data: profit, borderWidth: 3, tension: 0.4 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: "bottom" } },
            scales: {
                y: {
                    ticks: {
                        callback: value => "₦" + Number(value).toLocaleString()
                    }
                }
            }
        }
    });
}

function renderCategoryChart() {
    const ctx = document.getElementById("categoryChart");
    if (!ctx) return;

    const labels = categoryData.map(item => item.category);
    const amounts = categoryData.map(item => item.amount || 0);

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{ label: "Expenses", data: amounts, borderWidth: 2 }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: "bottom" } }
        }
    });
}