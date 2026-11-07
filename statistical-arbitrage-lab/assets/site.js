const canvas = document.getElementById("equityChart");
if (canvas && window.Chart) {
  const labels = Array.from({length: 48}, (_, i) => `W${i + 1}`);
  const values = [1,1.006,1.003,1.012,1.009,1.018,1.014,1.021,1.019,1.016,1.028,1.024,1.032,1.029,1.038,1.034,1.041,1.037,1.045,1.042,1.039,1.051,1.047,1.056,1.052,1.06,1.055,1.063,1.059,1.068,1.064,1.071,1.067,1.076,1.072,1.069,1.081,1.077,1.086,1.082,1.09,1.086,1.094,1.09,1.099,1.095,1.103,1.1];
  new Chart(canvas, {
    type: "line",
    data: { labels, datasets: [
      { label: "Illustrative strategy", data: values, borderColor: "#7ce0c3", borderWidth: 2, pointRadius: 0, tension: .28, fill: true, backgroundColor: "rgba(124,224,195,.07)" },
      { label: "Flat baseline", data: labels.map(() => 1), borderColor: "#65777c", borderWidth: 1, borderDash: [4,5], pointRadius: 0 }
    ]},
    options: { maintainAspectRatio: false, interaction: { intersect: false, mode: "index" },
      plugins: { legend: { display: false }, tooltip: { backgroundColor: "#152329", titleColor: "#dce8e3", bodyColor: "#a9bbb5", borderColor: "#31464a", borderWidth: 1 } },
      scales: { x: { grid: { display: false }, ticks: { color: "#687e81", maxTicksLimit: 8, font: { family: "DM Mono", size: 9 } } },
        y: { grid: { color: "#25343a" }, ticks: { color: "#687e81", callback: v => v.toFixed(2), font: { family: "DM Mono", size: 9 } } } }
    }
  });
}
