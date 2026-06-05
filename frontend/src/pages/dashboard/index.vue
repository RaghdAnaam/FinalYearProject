<template>
	<div class="home">
		<h2>My Analyses</h2>
		<!-- PROGRESS RING + AVERAGE SCORE -->
		<div v-if="averagePosition !== null" class="progress-ring-banner">
			<ProgressChart :score="Number(averagePosition)" />
			<p class="score-label">Current average skin score</p>
			<p class="score-date">Based on your latest analysis on <b>{{ formatDate(startDate) }}</b></p>
		</div>

		<!-- CHART CARD WRAPPER -->
		<div class="chart-card">
			<h3 class="chart-title">Skin Score History</h3>
			<averaged-chart
				:data-points="analyses"
				v-if="analyses.length"
				class="temp_bg"
			/>
			<p v-else class="error-message">No analyses found.</p>
		</div>

		<!-- BUTTONS, now centered in a row below the chart -->
		<div class="button-row">
			<div class="uploadBtn" @click="openPanel()">Upload Image</div>
			<RouterLink class="histBtn" :to="'/dashboard/analysis'">View History</RouterLink>
		</div>

		<!-- Centered modal overlay -->
		<div class="overlay" v-if="panelOpen">
			<div class="upload-modal-content">
				<span class="closeBtn" @click="openPanel()">✖️</span>
				<div class="upload-title-row">
					<span class="upload-title"> Upload image of your skin</span>
				</div>
				<UploadPhoto />
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import UploadPhoto from '../../components/upload/UploadPhoto.vue';
import AveragedChart from '../../components/averagedChart.vue';
import ProgressChart from '../../components/ProgressChart.vue';
import { toAgeYears, toMetricPercent } from '../../utils/analysisMetrics';

export default {
	components: {
		ProgressChart,
		UploadPhoto,
		AveragedChart,
	},
	data() {
		return {
			averagePosition: null,
			analyses: [],
			errorMessage: null,
			panelOpen: false,
			startDate: null,
		};
	},
	async mounted() {
		await this.fetchAnalyses();
	},
	methods: {
		formatDate(dateStr) {
			const date = new Date(dateStr);
			const options = { day: 'numeric', month: 'long', year: 'numeric' };
			return new Intl.DateTimeFormat('en-GB', options).format(date);
		},
		openPanel() {
			this.panelOpen = !this.panelOpen;
		},
		async fetchAnalyses() {
			const token = localStorage.getItem('token');
			if (!token) {
				this.errorMessage = 'Unauthorized: Please log in.';
				return;
			}
			try {
				const response = await axios.post(
					'http://localhost:5001/graphql/',
					{
						query: `
              query {
                myPhotosWithAnalyses {
                  id
                  date
                  time
                  imageB64
                  analysis {
                    id
                    age
                    texture
                    fineLines
                    hydration
                    date
                  }
                }
              }
            `,
					},
					{
						headers: {
							Authorization: `Bearer ${token}`,
							'Content-Type': 'application/json',
						},
					},
				);

				const photos = response.data.data.myPhotosWithAnalyses;

				if (!photos || photos.length === 0) {
					this.errorMessage = 'No analyses found.';
					this.analyses = [];
				} else {
					this.analyses = photos
						.filter((photo) => photo.analysis && photo.analysis.length)
						.flatMap((photo) =>
							photo.analysis.map((a) => ({
								id: a.id,
								date: photo.date,
								dateFormatted: new Date(photo.date).toLocaleDateString('en-GB', {
									day: 'numeric',
									month: 'short',
									year: 'numeric',
								}),
								image: photo.imageB64,
								result: {
									age: toAgeYears(a.age),
									texture: toMetricPercent(a.texture),
									fineLines: toMetricPercent(a.fineLines),
									hydration: toMetricPercent(a.hydration),
								},
							}))
					);
					if (this.analyses.length >= 2) {
						const last = this.analyses[this.analyses.length - 1].result;
						this.averagePosition = (
							Number(last.fineLines) +
							Number(last.hydration) +
							Number(last.texture)
						) / 3;
						this.startDate = this.analyses[0].date;
					}
				}
			} catch (error) {
				console.error('Fetch error:', error);
				this.errorMessage = 'Failed to fetch analyses. Please try again.';
			}
		},
	},
};
</script>

<style scoped>
/* Progress Ring Banner Styles */
.progress-ring-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 18px 0 8px 0;
  background: #b9dbec;
  border-radius: 15px;
  padding: 24px 0 12px 0;
  width: 65%;
  box-shadow: 0 2px 14px #4195ee1c;
  margin-left: auto;
  margin-right: auto;
}
.score-label {
  font-size: 1.1rem;
  font-weight: 700;
  margin-top: 10px;
  color: #355642;
}
.score-date {
  font-size: 0.98rem;
  color: #10101b;
  margin-top: 2px;
}

/* Chart Card Styles */
.chart-card {
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 8px 36px #566ae924, 0 1.5px 6px #6dc2df12;
  padding: 0.5rem 1.2rem 0.7rem 1.2rem;
  margin: 0 auto 1.1rem auto;
  max-width: 850px;
  width: 78%;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 330px;
}
.chart-title {
  text-align: center;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
  color: #1049d8;
  font-weight: 700;
  letter-spacing: 0.01em;
}

/* Chart inside card */
.temp_bg {
  width: 99%;
  height: 280px;
  margin: 0 auto 1.2% auto !important;
}

.button-row {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin: 16px auto 0 auto;
  width: 100%;
}

/* Main button: Upload Image */
.uploadBtn {
  width: 160px;
  height: 42px;
  background: linear-gradient(90deg, #ff5fa2 10%, #8f5fff 90%);
  color: #fff;
  font-weight: 700;
  font-size: 1.09rem;
  border: none;
  border-radius: 18px;
  box-shadow: 0 2px 8px #ff5fa22a;
  letter-spacing: 0.01em;
  cursor: pointer;
  transition: background 0.18s, box-shadow 0.16s, transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 2px 8px #8f5fff1a;
}
.uploadBtn:hover, .uploadBtn:focus {
  background: linear-gradient(90deg, #8f5fff 0%, #3ecfff 100%);
  box-shadow: 0 6px 16px #8f5fff3d;
  transform: translateY(-2px) scale(1.03);
}

.histBtn {
  width: 160px;
  height: 42px;
  background: linear-gradient(90deg, #4f8cff 0%, #38e4ff 100%);
  color: #fff;
  font-weight: 700;
  font-size: 1.05rem;
  border: none;
  border-radius: 15px;
  box-shadow: 0 2px 8px #38e4ff18;
  transition: background 0.14s, color 0.14s, transform 0.08s;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}
.histBtn:hover, .histBtn:focus {
  background: linear-gradient(90deg, #38e4ff 0%, #4f8cff 100%);
  color: #fff;
  transform: translateY(-2px) scale(1.03);
}

.overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(78, 53, 106, 0.1);
  z-index: 3000;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}
.upload-modal-content {
  background: #f4eeefe7;
  border-radius: 18px;
  box-shadow: 0 8px 32px #bdbdbd36, 0 2px 12px #e0e7ff34;
  padding: 40px 36px 30px 36px;
  min-width: 350px;
  min-height: 260px;
  max-width: 98vw;
  max-height: 92vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.error-message {
	color: red;
	text-align: center;
	margin-top: 10px;
	font-size: 14px;
}
.closeBtn {
  position: absolute;
  top: 5px;
  right: 10px;
  font-size: 2.2rem;      /* Increase size */
  font-weight: bold;
  color: #a14b7c;
  cursor: pointer;
  background: none;
  border: none;
  z-index: 10;
  transition: color 0.18s;
}
.closeBtn:hover {
  color: #ff5fa2;
}
.upload-title-row {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-top: -18px;    /* Move title up */
  margin-bottom: 18px;  /* Space below title */
}

.upload-title {
  font-size: 24px;      /* Increase font size */
  font-weight: 700;
  color: #121011;
  letter-spacing: 0.01em;
  text-align: center;
}
</style>
