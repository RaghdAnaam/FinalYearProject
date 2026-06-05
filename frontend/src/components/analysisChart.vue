<template>
  <div class="chart-wrapper">
    <div class="custom-legend">
  <span class="legend-item" style="color:#74b9ff;">
    <span class="legend-dot" style="background:#74b9ff"></span> Texture
  </span>
  <span class="legend-item" style="color:#fdcb6e;">
    <span class="legend-dot" style="background:#fdcb6e"></span> Fine Lines
  </span>
  <span class="legend-item" style="color:#55efc4;">
    <span class="legend-dot" style="background:#55efc4"></span> Hydration
  </span>
</div>

    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'AnalysisChart',
  props: ['dataPoints'],
  mounted() {
    const labels = this.dataPoints.map((item) => {
      const date = new Date(item.date);
      return date.toLocaleString('en-US', { month: 'short', day: 'numeric' });
    });

    const chartData = {
      labels,
      datasets: [
        {
          label: 'Texture',
          data: this.dataPoints.map((item) => Number(item.result.texture)),
          borderColor: '#74b9ff',
          backgroundColor: 'rgba(116,185,255,0.12)',
          tension: 0.36,
          borderWidth: 4,
          pointRadius: 8,
          pointHoverRadius: 10,
          fill: false,
        },
        {
          label: 'Fine Lines',
          data: this.dataPoints.map((item) => Number(item.result.fineLines)),
          borderColor: '#fdcb6e',
          backgroundColor: 'rgba(253,203,110,0.12)',
          tension: 0.36,
          borderWidth: 4,
          pointRadius: 8,
          pointHoverRadius: 10,
          fill: false,
        },
        {
          label: 'Hydration',
          data: this.dataPoints.map((item) => Number(item.result.hydration)),
          borderColor: '#55efc4',
          backgroundColor: 'rgba(85,239,196,0.20)',
          tension: 0.36,
          borderWidth: 5,
          pointRadius: 10,
          pointHoverRadius: 13,
          fill: false,
        },
      ],
    };

    new Chart(this.$refs.canvas, {
      type: 'line',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        // In Chart options
layout: {
  padding: {
    top: 50,    // Increased from 130
    bottom: 30,  // Increased from 18
    left: 10,    // Added left padding
    right: 10,
  },


        },
        animation: {
          duration: 1000,
          easing: 'easeInOutQuart',
        },
        plugins: {
          legend: {
            display: false,
            position: 'top',
            labels: {
              color: '#35345b',
              font: { size: 18, weight: 'bold' },
              padding: 40,     // More padding around legend labels
              boxWidth: 38,    // Make the legend icon bigger
              boxHeight: 18,   // Optional: taller icon
              usePointStyle: true,
            },
          },
          tooltip: {
            enabled: true,
            backgroundColor: '#fff',
            borderColor: '#bbb',
            borderWidth: 1.5,
            titleColor: '#262626',
            bodyColor: '#444',
            padding: 14,
            titleFont: { weight: 'bold', size: 14 },
            bodyFont: { weight: 'normal', size: 13 },
          },
        },
        scales: {
          x: {
            display: true,
            title: { display: false },
            ticks: {
              color: 'black',
              font: { size: 15, weight: 'bold' },
              padding: 8,
            },
            grid: { display: false },
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Score (%)',
              color: '#444',
              font: { size: 18, weight: 'bold' },
              padding: 16,
            },
            ticks: {
              color: '#888',
              font: { size: 14 },
              stepSize: 10,
              maxTicksLimit: 8,
              padding: 10,
            },
            grid: {
              color: '#f1f1f1',
              drawBorder: false,
            },
            min: 0,
            max: 100,
            suggestedMax: 105,
          },
        },
      },
    });
  },
  methods: {
    // Remove calculateMetricChange and updateChart methods - they're not being used
  }
}
</script>

<style scoped>
.custom-legend {
  display: flex;
  gap: 32px;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  margin-top: 10px;
}

.legend-item {
  font-size: 1.15rem;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.legend-dot {
  display: inline-block;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  margin-right: 8px;
  border: 2.5px solid #fff;
  box-shadow: 0 1px 4px #33298e55;
}

.chart-wrapper {
  width: 100%;
  height: 750px; /* or even 650px */
  max-width: 98%;
  margin: 0 auto;
  position: relative;
  background: #f8f6fb;
  border-radius: 15px;
  box-shadow: 0 2px 12px #dfdbdb33;
  padding: 20px 16px 16px 16px;
}

canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}
</style>