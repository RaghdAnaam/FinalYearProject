<template>
	<div class="chart-wrapper">
		<canvas ref="canvas"></canvas>
	</div>
</template>

<script>
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
	name: 'AveragedBarChart',
	props: ['dataPoints'],
	mounted() {
		const labels = this.dataPoints.map((item) => {
			const date = new Date(item.date);
			return date.toLocaleString('en-US', { day: 'numeric', month: 'short' }); // e.g. "17 May"
		});

		const scores = this.dataPoints.map((item) => {
			const { texture, fineLines, hydration } = item.result;
			// Calculate average without age
			return (
				(Number(texture) +
					Number(fineLines) +
					Number(hydration)) /
				3
			).toFixed(0);
		});

		const chartData = {
			labels,
			datasets: [
				{
					label: 'Average Score (%)',
					data: scores,
					backgroundColor: 'rgba(140, 111, 238, 0.55)', // a soft purple
					borderRadius: 12,
					maxBarThickness: 44,
				},
			],
		};

		new Chart(this.$refs.canvas, {
			type: 'bar',
			data: chartData,
			options: {
				responsive: true,
				maintainAspectRatio: false,
				animation: {
					duration: 1000,
					easing: 'easeInOutQuad',
				},
				plugins: {
					legend: {
						display: false, // no need for legend on single bar series
					},
					tooltip: {
						enabled: true,
						backgroundColor: '#222',
						borderColor: '#8f5fff',
						borderWidth: 1,
						padding: 12,
						titleFont: { weight: 'bold' },
						bodyFont: { weight: 'normal' },
					},
				},
				scales: {
					x: {
						display: true,
						ticks: {
							color: 'black',
							font: { size: 13, weight: 'bold' },
						},
						grid: {
							display: false,
						},
					},
					y: {
						display: true,
						title: {
							display: true,
							text: 'Score (%)',
							color: '#444',
							font: { size: 14, weight: 'bold' },
						},
						ticks: {
							color: '#666',
							font: { size: 12 },
							stepSize: 20,
						},
						grid: {
							color: '#f1f1f1',
							drawBorder: false,
						},
						min: 0,
						max: 100,
					},
				},
			},
		});
	},
};
</script>

<style scoped>
.chart-wrapper {
	width: 100%;
	height: 330px; /* You can adjust height for dashboard layout */
	position: relative;
	padding-bottom: 12px;
}
canvas {
	display: block;
	width: 100% !important;
	height: 100% !important;
}
</style>
