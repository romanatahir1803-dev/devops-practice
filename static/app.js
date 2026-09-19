/**
 * Ultra-Readable Mattress AI Sentiment Dashboard
 * High-legibility horizontal bar charts with direct in-bar labels and filter switcher.
 */

document.addEventListener("DOMContentLoaded", () => {
    initViewSwitcher();
    renderLikesChart();
    renderPainsChart();
});

// View Switcher (All / Likes / Pains / Search)
function initViewSwitcher() {
    const buttons = document.querySelectorAll(".view-btn");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const filter = btn.getAttribute("data-filter");
            const verdict = document.getElementById("verdictSection");
            const scorecards = document.getElementById("scorecardsSection");
            const charts = document.getElementById("chartsSection");
            const search = document.getElementById("searchSection");
            const likesCard = document.getElementById("chartLikesCard");
            const painsCard = document.getElementById("chartPainsCard");

            // Reset visibility
            verdict.style.display = "block";
            scorecards.style.display = "block";
            charts.style.display = "block";
            search.style.display = "block";
            likesCard.style.display = "block";
            painsCard.style.display = "block";

            if (filter === "likes") {
                verdict.style.display = "none";
                scorecards.style.display = "none";
                search.style.display = "none";
                painsCard.style.display = "none";
                likesCard.scrollIntoView({ behavior: 'smooth' });
            } else if (filter === "pains") {
                verdict.style.display = "none";
                scorecards.style.display = "none";
                search.style.display = "none";
                likesCard.style.display = "none";
                painsCard.scrollIntoView({ behavior: 'smooth' });
            } else if (filter === "search") {
                verdict.style.display = "none";
                scorecards.style.display = "none";
                charts.style.display = "none";
                search.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// 1. Horizontal Bar Chart for Positive Drivers (Likes)
function renderLikesChart() {
    const canvas = document.getElementById("canvasLikes");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const labels = [
        'Spinal & Back Pain Relief',
        '2-in-1 Dual Hardness Flip',
        'Hygiene / Washable Cover (60°C)',
        'Odorless & Fast Expansion',
        'Price-to-Value Index'
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'AM Qualitätsmatratzen',
                    data: [94, 82, 92, 85, 96],
                    backgroundColor: '#06B6D4',
                    borderRadius: 4,
                    barPercentage: 0.75,
                    categoryPercentage: 0.8
                },
                {
                    label: 'bett1 BODYGUARD',
                    data: [89, 95, 84, 91, 94],
                    backgroundColor: '#8B5CF6',
                    borderRadius: 4,
                    barPercentage: 0.75,
                    categoryPercentage: 0.8
                }
            ]
        },
        options: {
            indexAxis: 'y', // HORIZONTAL BAR CHART
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    min: 0,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: {
                        color: '#94A3B8',
                        font: { size: 12 },
                        callback: v => v + '%'
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        color: '#F8FAFC',
                        font: { size: 13, weight: '600' }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#FFFFFF',
                        font: { size: 13, weight: '700' },
                        boxWidth: 14,
                        padding: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.dataset.label}: ${ctx.raw}% Positive Feedback`
                    }
                }
            }
        }
    });
}

// 2. Horizontal Bar Chart for Complaints & Pain Points
function renderPainsChart() {
    const canvas = document.getElementById("canvasPains");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const labels = [
        'Pelvic Sagging (Liegekuhle >6 mos)',
        'Too Hard / Stiff (Wooden Plank Feel)',
        'Heat Retention / Night Sweating',
        'Heavy Parcel Delivery Logistics',
        'Trial Period Return Repacking'
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'AM Qualitätsmatratzen',
                    data: [28, 16, 18, 14, 10],
                    backgroundColor: '#F43F5E',
                    borderRadius: 4,
                    barPercentage: 0.75,
                    categoryPercentage: 0.8
                },
                {
                    label: 'bett1 BODYGUARD',
                    data: [22, 29, 12, 16, 14],
                    backgroundColor: '#FB923C',
                    borderRadius: 4,
                    barPercentage: 0.75,
                    categoryPercentage: 0.8
                }
            ]
        },
        options: {
            indexAxis: 'y', // HORIZONTAL BAR CHART
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    min: 0,
                    max: 35,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: {
                        color: '#94A3B8',
                        font: { size: 12 },
                        callback: v => v + '%'
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        color: '#F8FAFC',
                        font: { size: 13, weight: '600' }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#FFFFFF',
                        font: { size: 13, weight: '700' },
                        boxWidth: 14,
                        padding: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: ctx => ` ${ctx.dataset.label}: ${ctx.raw}% Complaint Frequency`
                    }
                }
            }
        }
    });
}
