<template>
  <div class="progress-ring-wrapper">
    <canvas ref="progressCanvas"></canvas>
    <div class="center-label">
      <span class="score">{{ Number(score).toFixed(0) }}%</span>
      <span class="caption">Average</span>
    </div>
  </div>
</template>

<script>
import { Chart, ArcElement, Tooltip } from 'chart.js';
Chart.register(ArcElement, Tooltip);

export default {
  name: "ProgressChart",
  props: {
    score: {
      type: Number,
      required: true
    }
  },
  mounted() {
    const ctx = this.$refs.progressCanvas.getContext('2d');
    this.chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets: [
          {
            data: [this.score, 100 - this.score],
            backgroundColor: ['#6c5ce7', '#eceaff'],
            borderWidth: 0,
            cutout: '78%',
            hoverOffset: 2,
          }
        ]
      },
      options: {
        cutout: '78%',
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        }
      }
    });
  },
  watch: {
    score(newScore) {
      if (this.chart) {
        this.chart.data.datasets[0].data = [newScore, 100 - newScore];
        this.chart.update();
      }
    }
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
};
</script>

<style scoped>
.progress-ring-wrapper {
  width: 130px;
  height: 130px;
  margin: 0 auto;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
canvas {
  width: 130px !important;
  height: 130px !important;
}
.center-label {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.score {
  font-size: 20px;
  font-weight: 800;
  color: #0e0f12;
  line-height: 2;
}
.caption {
  font-size: 1.05rem;
  color: #888;
  margin-top: -1px;
  display: block;
  letter-spacing: 0.02em;
}
</style>
