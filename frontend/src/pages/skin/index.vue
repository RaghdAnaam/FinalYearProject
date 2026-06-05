<template>
  <div class="progress-outer">
    <div class="progress-card">
      <div class="overallProgress" v-if="startDate && progress !== null">
        Your skin has 
        <span :class="{ 'progress-value': progress >= 0, 'progress-value-negative': progress < 0 }">
          {{ progress >= 0 ? 'improved' : 'worsened' }} by 
          {{ Math.round(Math.abs(progress)) }}%
        </span> 
        since {{ formatDate(startDate) }}
      </div>

      <analysis-chart
        :data-points="analyses"
        v-if="analyses.length"
        class="temp_bg"
      />

      <div class="keyDiffs-row" v-if="differences">
        <div class="diffCard fine-lines">
          <div>
            <span class="diffTitle">Fine Lines</span>
            <span class="diffValue">{{ Math.round(differences.fineLines) }}%</span>
          </div>
        </div>
        <div class="diffCard texture">
          <div>
            <span class="diffTitle">Texture</span>
            <span class="diffValue">{{ Math.round(differences.texture) }}%</span>
          </div>
        </div>
        <div class="diffCard hydration">
          <div>
            <span class="diffTitle">Hydration</span>
            <span class="diffValue">{{ Math.round(differences.hydration) }}%</span>
          </div>
        </div>
      </div>

      <div class="progressBarWithDigits" v-if="progress !== null">
        <div class="progress-bar-wrapper">
          <div 
            class="progress-bar" 
            :class="{ 'negative': progress < 0 }"
            :style="{ width: Math.abs(progress) + '%' }"
          ></div>
        </div>
        <div class="digits" :class="{ 'negative': progress < 0 }">
          {{ progress > 0 ? '' : '-' }}{{ Math.round(Math.abs(progress)) }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AnalysisChart from '../../components/analysisChart.vue';
import { toAgeYears, toMetricPercent } from '../../utils/analysisMetrics';

export default {
  data() {
    return {
      analyses: [],
      progress: null,
      differences: null,
      startDate: null,
      errorMessage: null
    };
  },
  components: {
    AnalysisChart
  },
  mounted() {
    this.fetchAnalyses();
  },
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr);
      const options = { day: 'numeric', month: 'long', year: 'numeric' };
      return new Intl.DateTimeFormat('en-GB', options).format(date);
    },
    async fetchAnalyses() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.errorMessage = 'Unauthorized: Please log in.';
          return;
        }

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
            `
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          }
        );

        const photos = response.data.data.myPhotosWithAnalyses;

        if (!photos || photos.length === 0) {
          this.errorMessage = 'No analyses found.';
          this.analyses = [];
        } else {
          // Using your original calculation logic
          this.analyses = photos
            .filter((photo) => photo.analysis && photo.analysis.length)
            .flatMap((photo) =>
              photo.analysis.map((a) => ({
                id: a.id,
                date: photo.date,
                result: {
                  age: toAgeYears(a.age),
                  texture: toMetricPercent(a.texture),
                  fineLines: toMetricPercent(a.fineLines),
                  hydration: toMetricPercent(a.hydration),
                },
              }))
            );

          if (this.analyses.length >= 2) {
            const first = this.analyses[0].result;
            const last = this.analyses[this.analyses.length - 1].result;

            const calculatePercentChange = (current, initial, isInverse = false) => {
              if (!initial || initial === 0) return 0;
              const rawChange = ((current - initial) / initial) * 100;
              return isInverse ? -rawChange : rawChange;
            };

            // Update texture calculation to be inverse (lower is better)
            const textureChange = calculatePercentChange(last.texture, first.texture, true);
            const fineLinesChange = calculatePercentChange(last.fineLines, first.fineLines, true);
            const hydrationChange = calculatePercentChange(last.hydration, first.hydration);

            // Store the differences
            this.differences = {
              texture: Math.round(textureChange),  // Will now be positive when texture decreases
              fineLines: Math.round(fineLinesChange),
              hydration: Math.round(hydrationChange)
            };

            // Calculate overall progress
            const totalWeight = 3;
            this.progress = Math.round(
              (textureChange + fineLinesChange + hydrationChange) / totalWeight
            );

            this.startDate = this.analyses[0].date;
          }
        }
      } catch (error) {
        console.error('Fetch error:', error);
        this.errorMessage = 'Failed to fetch analyses. Please try again.';
      }
    }
  }
};
</script>

<style scoped>
.progress-outer {
  width: 100vw;
  min-height: 100vh;
  background: #faeafd;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 32px;
}

.progress-card {
  width: 95vw;
  max-width: 880px;
  background: #fff;
  border-radius: 30px;
  box-shadow: 0 8px 36px #19033918, 0 1.5px 6px #3ecfff12;
  margin: 0 auto;
  padding: 32px 32px 22px 32px;
  min-height: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.overallProgress {
  text-align: center;
  font-size: 2.2rem;
  color: #73268f;
  font-weight: 700;
  margin-bottom: 1.2rem;
}
.progress-value {
  color: #15a984;  /* You can change this to any color you prefer */
}

.progress-value-negative {
  color: #e74c3c;
}

.temp_bg {
  width: 99%;
  height: 380px;
  margin: 0 auto 1.2% auto !important;
}

.progressBarWithDigits {
  width: 88%;
  max-width: 520px;
  margin: 22px auto 10px auto;
  height: 34px;
  display: flex;
  align-items: center;
  flex-direction: row;
}

.progress-bar-wrapper {
  background-color: #eee;
  border-radius: 20px;
  height: 13px;
  overflow: hidden;
  width: 82%;
}

.progress-bar {
  background: linear-gradient(90deg, #5ed6a5 0%, #36c8c8 100%);
  height: 100%;
  transition: width 0.6s ease;
}

.progress-bar.negative {
  background: linear-gradient(90deg, #ff6b6b 0%, #e74c3c 100%);
}

.digits {
  width: 18%;
  text-align: right;
  padding-left: 14px;
  font-weight: 700;
  font-size: 1.18rem;
  color: #15a984;
}

.digits.negative {
  color: #e74c3c;
}

.keyDiffs-row {
  width: 85%;
  max-width: 620px;
  margin: 32px auto 12px auto;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  justify-content: center;
  gap: 28px;
}

/* Base card style */
.diffCard {
  display: flex;
  align-items: center;
  border-radius: 15px;
  box-shadow: 0 2px 8px #24877faf;
  padding: 18px 30px 16px 24px;
  min-width: 140px;
  gap: 0;
  font-weight: bold;
  color: #35345b;
  font-size: 1.12rem;
  background: #fafaff;
}

/* Specific backgrounds for each */
.diffCard.fine-lines {
  background: #fdcb6e;
  color: #664600; /* dark text for contrast */
}
.diffCard.texture {
  background: #74b9ff;
  color: #1a233a;
}
.diffCard.hydration {
  background: #55efc4;
  color: #064d39;
}

.diffTitle, .diffValue {
  display: block;
}

.diffTitle {
  font-weight: 700;
  font-size: 1.15rem;
  margin-bottom: 3px;
}

.diffValue {
  font-size: 1.19rem;
  font-weight: 700;
}
</style>
