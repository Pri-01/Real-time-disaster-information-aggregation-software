// Dummy data simulation
function fetchModelMetrics() {
    const data = {
      accuracy: 97.8,
      precision: 90.0,
      recall: 69.0,
      f1: 73.0,
      updatedAt: new Date().toLocaleString(),
    };
  
    updateMetrics(data);
    updateCharts(data);
  }
  
  function updateMetrics(data) {
    document.getElementById("accuracy").textContent = `${data.accuracy}%`;
    document.getElementById("precision").textContent = `${data.precision}%`;
    document.getElementById("recall").textContent = `${data.recall}%`;
    document.getElementById("f1").textContent = `${data.f1}%`;
    document.getElementById("last-updated").textContent = data.updatedAt;
  }
  
  let lineChart, barChart, pieChart;
  
  function updateCharts(data) {
    const labels = ["Accuracy", "Precision", "Recall", "F1 Score"];
    const values = [data.accuracy, data.precision, data.recall, data.f1];
  
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
    };
  
    if (lineChart) lineChart.destroy();
    if (barChart) barChart.destroy();
    if (pieChart) pieChart.destroy();
  
    lineChart = new Chart(document.getElementById("lineChart"), {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Performance Over Time",
            data: values,
            borderColor: "#2563eb",
            fill: false,
            tension: 0.3,
          },
        ],
      },
      options: chartOptions,
    });
  
    barChart = new Chart(document.getElementById("barChart"), {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "% Score",
            data: values,
            backgroundColor: "#10b981",
            barThickness: 40, // ✅ Uniform bar width
            maxBarThickness: 40,
            minBarLength: 2,
          },
        ],
      },
      options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            color: "#333",
          },
        },
        y: {
          beginAtZero: true,
          min: 65,
          max: 100,
          ticks: {
            stepSize: 5,
            color: "#333",
          },
        },
      },
    },
  });
  
    pieChart = new Chart(document.getElementById("pieChart"), {
      type: "pie",
      data: {
        labels,
        datasets: [
          {
            data: values,
            backgroundColor: ["#2563eb", "#10b981", "#f59e0b", "#ef4444"],
          },
        ],
      },
      options: chartOptions,
    });
  }
  
  // Refresh every 10 seconds
  setInterval(fetchModelMetrics, 5000);
  fetchModelMetrics();