<template>
  <div class="charts-wrapper">
    <div class="chart-container">
      <canvas ref="pieCanvas"></canvas>
    </div>
  </div>
</template>

<script>
import { 
  Chart, 
  ArcElement, 
  Tooltip, 
  Legend,
  Title  // Add Title plugin
} from 'chart.js'

Chart.register(ArcElement, Tooltip, Legend, Title)  // Register Title plugin

export default {
  name: 'AdminChart',
  props: {
    totalUsers: {
      type: Number,
      required: true
    },
    activeUsers: {
      type: Number,
      required: true
    }
  },
  created() {
    console.log('Component created')
  },
  mounted() {
    console.log('Component mounted with props:', {
      totalUsers: this.totalUsers,
      activeUsers: this.activeUsers
    })
    this.createChart()
  },
  updated() {
    console.log('Component updated')
  },
  methods: {
    createChart() {
      try {
        console.log('Creating chart with data:', {
          activeUsers: this.activeUsers,
          totalUsers: this.totalUsers
        })

        const ctx = this.$refs.pieCanvas.getContext('2d')
        if (!ctx) {
          console.error('Failed to get canvas context')
          return
        }

        // Clear any existing chart
        if (this.chart) {
          this.chart.destroy()
        }

        this.chart = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['Active Users', 'Inactive Users'],
            datasets: [{
              data: [this.activeUsers, this.totalUsers - this.activeUsers],
              backgroundColor: [
                'rgba(73, 209, 255, 0.8)',   // Light blue color
                'rgba(255, 183, 121, 0.8)'   // Light orange color
              ],
              borderWidth: 0,
              hoverOffset: 4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  font: {
                    size: 14
                  }
                }
              },
              title: {
                display: true,
                text: 'User Activity Distribution',
                font: {
                  size: 16,
                  weight: 'bold'
                },
                padding: 20
              }
            }
          }
        })
      } catch (error) {
        console.error('Error creating chart:', error)
      }
    }
  },
  watch: {
    activeUsers(newValue) {
      if (this.chart) {
        this.chart.data.datasets[0].data = [newValue, this.totalUsers - newValue]
        this.chart.update()
      }
    },
    totalUsers(newValue) {
      if (this.chart) {
        this.chart.data.datasets[0].data = [this.activeUsers, newValue - this.activeUsers]
        this.chart.update()
      }
    }
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
</script>

<style scoped>
.charts-wrapper {
  width: 100%;  /* Changed from 300% to 100% */
  padding: 1rem;
  min-height: 500px;  /* Increased from 400px */
}

.chart-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 500px;  /* Increased from 400px */
  width: 100%;    /* Changed from 300% */
  max-width: 800px;  /* Increased from 600px */
  margin: 0 auto;
  position: relative;
}

canvas {
  position: absolute; /* Position canvas absolutely */
  top: 0;
  left: 0;
  width: 100% !important;
  height: 100% !important;
}

@media (max-width: 768px) {
  .chart-container {
    height: 400px;  /* Adjusted for mobile */
  }
}
</style>