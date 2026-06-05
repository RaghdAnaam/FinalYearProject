<template>
	<div class="welcomePage">
		<div class="welcomeMsg">Welcome to SkinVision</div>
		
		<div v-if="error" class="error-message">
			{{ error }}
		</div>

		<AdminChart 
			v-if="!error"
			:totalUsers="Number(totalUsers)" 
			:activeUsers="Number(activeUsers)"
		/>
	</div>
</template>

<script>
import requests from '../../utils/requests'
import AdminChart from '../../components/AdminChart.vue'

export default {
	components: {
		AdminChart
	},
	data() {
		return {
			totalUsers: 0,
			activeUsers: 0,
			error: null,
			isDevelopment: import.meta.env.MODE === 'development'
		}
	},
	methods: {
		async getData() {
			try {
				const query = `query {
					metrics {
						totalUsers
						activeUsersLast30Days
					}
				}`
				
				const response = await requests(query)
				console.log('GraphQL Response:', response)

				if (!response || !response.data || !response.data.metrics) {
					throw new Error('Invalid response structure')
				}

				const { totalUsers, activeUsersLast30Days } = response.data.metrics

				if (typeof totalUsers !== 'number' || typeof activeUsersLast30Days !== 'number') {
					throw new Error('Invalid metrics values')
				}

				this.totalUsers = totalUsers
				this.activeUsers = activeUsersLast30Days

			} catch (error) {
				console.error('Failed to fetch metrics:', error)
				this.error = 'Failed to load metrics. Please try again later.'
				this.totalUsers = 0
				this.activeUsers = 0
			}
		},
	},
	async mounted() {
		await this.getData();
	},
};
</script>

<style scoped>
.welcomePage {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1.5rem;
	padding: 2rem;
	width: 100%;
	max-width: 600px;
	margin: 0 auto;
	box-sizing: border-box;
}

.welcomeMsg {
	text-align: center;
	font-size: 2rem;
	font-weight: bold;
	color: #333;
	margin-bottom: 1rem;
}

.stats-container {
	display: flex;
	flex-direction: column;
	gap: 1.5rem;
	width: 100%;
}

.statCard {
	background-color: rgb(3, 22, 29);
	color: black;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	padding: 2rem;
	border-radius: 12px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	font-size: 1.25rem;
	text-align: center;
	width: 100%;
}

.error-message {
	color: #dc3545;
	background-color: #f8d7da;
	border: 1px solid #f5c6cb;
	border-radius: 4px;
	padding: 1rem;
	margin: 1rem 0;
	text-align: center;
}

@media (max-width: 768px) {
	.welcomeMsg {
		font-size: 1.5rem;
	}
	.statCard {
		font-size: 1rem;
		padding: 1.5rem;
	}
}
</style>
