<template>
  <div class="analysisDiv">
    <div class="historyDiv">
      <h1>Analysis History</h1>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-else-if="!analyses.length" class="error-message">No analyses found.</div>
      <div v-else>
        <div
          class="analysisInstance"
          v-for="(analysis, index) in analyses"
          :key="analysis.id"
        >
          <analysis
            :analysis="analysis"
            :formatDate="formatDate"
            @analysis-deleted="handleAnalysisDeleted"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import requests from '../../utils/requests';
import { toAgeYears, toMetricPercent } from '../../utils/analysisMetrics';
import analysis from './analysis.vue';
export default {
	data() {
  return {
    analyses: [],
    errorMessage: null,
  };
},
	components: {
		analysis,
	},
	async mounted() {
		await this.fetchAnalysis();
	},
	methods: {
		formatDate(dateStr) {
			const date = new Date(dateStr);
			const options = { day: 'numeric', month: 'long', year: 'numeric' };
			return new Intl.DateTimeFormat('en-GB', options).format(date);
		},
		async fetchAnalysis() {
			const query = `
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
        }
      }
    }
  `;
			const { data, errors } = await requests(query);

			if (data && data.myPhotosWithAnalyses) {
				const photos = data.myPhotosWithAnalyses;

				if (!photos.length) {
					this.errorMessage = 'No analyses found.';
					this.analyses = [];
				} else {
					this.analyses = photos.flatMap((photo) =>
						photo.analysis.map((a) => ({
							id: a.id,
							date: photo.date,
							time: photo.time,
							image: photo.imageB64,
							result: {
								age: toAgeYears(a.age),
								texture: toMetricPercent(a.texture),
								fineLines: toMetricPercent(a.fineLines),
								hydration: toMetricPercent(a.hydration),
							},
						})),
					);
					this.errorMessage = null;
				}
			} else {
				this.analyses = [];
				this.errorMessage = errors?.[0]?.message || 'No analyses found.';
			}
		},
		async handleAnalysisDeleted(analysisId) {
      const mutation = `
        mutation DeleteAnalysis($id: Int!) {
          deleteAnalysis(id: $id) {
            success
            message
          }
        }
      `;

      try {
        const { data, errors } = await requests(mutation, {
          id: Number(analysisId)
        });

        if (errors) {
          throw new Error(errors[0].message);
        }

        if (data.deleteAnalysis.success) {
          // Remove the deleted analysis from the list
          this.analyses = this.analyses.filter(a => a.id !== analysisId);
        }
      } catch (error) {
        console.error('Error deleting analysis:', error);
        this.errorMessage = 'Failed to delete analysis: ' + error.message;
      }
    }
	},
};
</script>

<style scoped>
.analysisDiv {
	padding: 10px;
	overflow-y: auto;
}
.analysisInstance {
	margin: 1%;
	width: 98%;
	height: 50px;
	border-radius: 8px;
	display: flex;
	flex-direction: row;
}

.historyDiv {
	margin: 2.5% auto;
	width: 40%;
	height: 90%;
	overflow-y: auto;
	background-color: white;
	border-radius: 8px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.analysisInstance {
	margin: 1%;
	width: 98%;
	height: 50px;
	border-radius: 8px;
	display: flex;
	flex-direction: row;
}

.left {
	height: 100%;
	width: 10%;
	margin: 0;
	display: flex;
	align-items: center;
	justify-content: center;
}

.middle {
	width: 60%;
	height: 100%;
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	justify-content: center;
}

.date {
	font-size: 16px;
	color: black;
	font-weight: 600;
}

.time {
	font-size: 14px;
	color: grey;
	font-weight: 400;
}

.right {
	width: 30%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.viewBtn {
	width: 60%;
	height: 60%;
	background-color: grey;
	color: white;
	border-radius: 20px;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
}

.middle :is(p) {
	margin: 0;
}

.analysisImage {
	height: 80%;
	margin-left: 5%;
	object-fit: cover;
	border-radius: 8px;
}

.pair {
	width: 100%;
	display: flex;
	flex-direction: row;
	margin: 1% 0;
}

.label {
	width: 30%;
	margin: 0;
	text-align: left;
	font-weight: 600;
}

.value {
	width: 60%;
	margin: 0;
	text-align: left;
}

.analysisAttributes {
	width: 75%;
	height: 100%;
	display: flex;
	flex-direction: column;
	justify-content: center;
}
</style>
