<template>
	<div class="left">
		<img
			:src="`data:image/jpeg;base64,${analysis.image}`"
			alt="Analysis Image"
			class="analysisImage"
		/>
	</div>
	<div class="middle">
		<p class="date">{{ formatDate(analysis.date) }}</p>
		<p class="time">{{ analysis.time.slice(0, -3) }}</p>
	</div>
	<div class="right">
		<div class="viewBtn" @click="toggleOpenPanel()">View Details</div>
	</div>

	<div class="analysisAttributes" v-if="openPanel">
		<div class="topBar">
			<p>
				Skin analysis<br />
				submitted on {{ formatDate(analysis.date) }} at
				{{ analysis.time.slice(0, -3) }}
			</p>
			<div class="closeBtn"><p @click="toggleOpenPanel()">X</p></div>
		</div>
		<div class="largeImg">
			<img
				:src="`data:image/jpeg;base64,${analysis.image}`"
				alt="Analysis Image"
				class="analysisImage"
			/>
		</div>
		<div class="normalPair">
			<p class="label">age:</p>
			<p class="value">~{{ analysis.result.age }} years</p>
		</div>

		<div class="pair">
			<p class="label">fine lines</p>
			<div class="value">
				<div class="progress-bar-wrapper">
					<div
						class="progress-bar"
						:style="{ width: Math.round(analysis.result.fineLines) + '%' }"
						style="background-color: #fdcb6e"
					></div>
				</div>
				<small>{{ Math.round(analysis.result.fineLines) }}%</small>
			</div>
		</div>

		<div class="pair">
			<p class="label">texture</p>
			<div class="value">
				<div class="progress-bar-wrapper">
					<div
						class="progress-bar"
						:style="{ width: Math.round(analysis.result.texture) + '%' }"
						style="background-color: #74b9ff"
					></div>
				</div>
				<small>{{ Math.round(analysis.result.texture) }}%</small>
			</div>
		</div>
		<div class="pair">
			<p class="label">hydration</p>
			<div class="value">
				<div class="progress-bar-wrapper">
					<div
						class="progress-bar"
						:style="{ width: Math.round(analysis.result.hydration) + '%' }"
						style="background-color: #55efc4"
					></div>
				</div>
				<small>{{ Math.round(analysis.result.hydration) }}%</small>
			</div>
		</div>
		<div class="btmAdvice">
			<div class="advice">
				<div class="imageSpace">
					<img src="../../assets/icons/icons8-water-drop-100.png" alt="" />
				</div>
				<div class="textSpace">
					<h2>Hydration</h2>
					<p>
						It's important to keep your skin hydrated. Try using a hyaluronic
						acid serum or mask to lock in moisture and plump the skin.
					</p>
				</div>
			</div>
			<div class="advice">
				<div class="imageSpace">
					<img src="../../assets/icons/icons8-pencil-100.png" alt="" />
				</div>
				<div class="textSpace">
					<h2>Fine Lines</h2>
					<p>
						To reduce fine lines, try incorporating retinol into your routine.
						Start with a lower concentration and gradually increase as your skin
						adjusts.
					</p>
				</div>
			</div>
			<div class="advice">
				<div class="imageSpace">
					<img src="../../assets/icons/icons8-photo-100.png" alt="" />
				</div>
				<div class="textSpace">
					<h2>Texture</h2>
					<p>
						Exfoliation can help improve skin texture. Look for a gentle
						chemical exfoliant with AHAS or BHAS to remove dead skin cells and
						reveal smoother, more even skin.
					</p>
				</div>
			</div>
			<div class="buttonRoutine">
				<router-link class="btnRoutine" :to="'/dashboard/routines'"
					>Update Routine</router-link
				>
				<div class="deleteBtn" @click="deleteAnalysis">
					<img src="../../assets/icons/trash.svg" alt="Delete" />
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'; // Add this import

export default {
	data() {
		return {
			openPanel: false,
		};
	},
	methods: {
		toggleOpenPanel() {
			this.openPanel = !this.openPanel;
		},
		async deleteAnalysis() {
			if (!confirm('Are you sure you want to delete this analysis?')) return;

			try {
				const response = await axios.post(
					'http://localhost:5001/graphql/',
					{
						query: `
							mutation DeleteAnalysis($id: Int!) {
								deleteAnalysis(id: $id) {
									success
									message
								}
							}
						`,
						variables: {
							id: Number(this.analysis.id)
						}
					},
					{
						headers: {
							'Authorization': `Bearer ${localStorage.getItem('token')}`,
							'Content-Type': 'application/json'
						}
					}
				);

				if (response.data.data.deleteAnalysis.success) {
					// Emit event to parent component
					this.$emit('analysis-deleted', this.analysis.id);
					this.toggleOpenPanel();
					// Show success message
					alert('Analysis deleted successfully');
				} else {
					throw new Error(response.data.data.deleteAnalysis.message);
				}
			} catch (error) {
				console.error('Delete error:', error);
				// Don't show the full error object in alert
				alert('Failed to delete analysis. Please try again.');
			}
		}
	},
	props: {
		analysis: {
			type: Object,
			required: true,
		},
		formatDate: {
			type: Function,
			required: true,
		},
	},
};
</script>

<style scoped>
.buttonRoutine {
	width: 100%;
	height: 50px;
	display: flex;
	align-items: center;
	justify-content: space-between; /* Change from flex-start to space-between */
	padding: 0 10px; /* Add padding for better spacing */
}

.btnRoutine {
	padding: 10px 20px;
	background-color: #c43ea9;
	color: white;
	border-radius: 20px;
	text-decoration: none;
	font-weight: 600;
	width: fit-content; /* Add this line */
}

.deleteBtn {
	width: 40px;
	height: 40px;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	background-color: #ff6b6b;
	border-radius: 20px;
	transition: background-color 0.2s;
	margin-left: auto; /* Add this line to push it to the right */
}

.deleteBtn:hover {
	background-color: #e74c3c;
}

.deleteBtn img {
	width: 20px;
	height: 20px;
	opacity: 1;
}

.btmAdvice {
	width: 100%;
	height: auto;
	display: flex;
	flex-direction: column;
	gap: 15px;          /* Add gap between advice items */
  padding: 15px 0; 
}
.advice {
	width: 100%;
	display: flex;
	flex-direction: row;
	margin: 0;
	min-height: 80px; 
}

.advice .imageSpace {
	width: 10%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.advice .imageSpace :is(img) {
	max-width: 80%;
	max-height: 80%;
	border-radius: 8px;
	background-color: pink;
	padding: 5px 5px;
}

.advice .textSpace {
	width: 87.5%;
	margin-left: 2.5%;
	height: auto;       /* Change from 100% to auto */
  display: flex;
  flex-direction: column;
  gap: 5px; 
}

.advice .textSpace :is(h2) {
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: flex-start;
	margin: 0;
	font-size: 18px;
	color: black;
}

.advice .textSpace :is(p) {
	width: 100%;
	text-align: left;
	margin: 0;
	font-size: 14px;
	color: rgb(225, 124, 225);
	font-weight: 500;
}

.largeImg {
	width: 100%;
  height: auto;       /* Change from 32.5% to auto */
  padding: 15px 0; 
}
.largeImg img {
  max-height: 300px;  /* Set maximum height for image */
  width: auto;        /* Maintain aspect ratio */
}

.topBar {
	width: 100%;
	display: flex;
	flex-direction: row;
	height: 50px;
	position: relative;
}

.topBar :is(p) {
	width: 90%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-left: 5% !important;
	font-size: 24px;
	color: black;
	margin: 0;
	font-weight: 600;
}

.topBar .closeBtn {
	width: 5%;
	display: flex;
	height: 100%;
	align-items: center;
	justify-content: center;
	font-size: 30px;
	cursor: pointer;
}

.deleteBtn {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 10px;
}

.deleteBtn img {
  width: 20px;
  height: 20px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.deleteBtn:hover img {
  opacity: 1;
}

.closeBtn p {
	width: 20px;
	height: 20px;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 50%;
	border: 2px solid black;
	color: black;
	cursor: pointer;
	margin: 0;
	padding: 0;
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
	width: 100%;
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
	margin-left: 1% !important;
	margin: 0;
}

.analysisImage {
	height: 80%;
	object-fit: cover;
	border-radius: 8px;
}
/* --------------------------- */
.pair {
	width: 100%;
	display: flex;
	flex-direction: column;
	margin: 1% 0;
}

.label {
	width: 100%;
	margin: 0;
	text-align: left;
	font-weight: 600;
	font-weight: 600;
	color: black;
}

.value {
	width: 100%;
	margin: 0;
	display: flex;
	flex-direction: row;
	align-items: center;
	/* justify-content: center; */
}

.value :is(small) {
	width: 10%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 0.75rem;
	font-weight: 500;
}

.analysisAttributes {
	position: absolute;
	width: 38.1%;
	height: 83.5%;
	top: 8%;
	margin-left: -0.5%;
	padding: 1%;
	display: flex;
	flex-direction: column;
	background-color: white;
	border-radius: 8px;
	box-shadow: 0 0px 6.2px rgba(0, 0, 0, 0.2);
	height: fit-content;  /* Change from 83.5% to fit-content */
  max-height: 90vh;     /* Add max-height */
  overflow-y: auto; 
}
.progress-bar-wrapper {
	background-color: pink;
	border-radius: 20px;
	height: 12px;
	margin: 10px 0;
	overflow: hidden;
	width: 90%;
}

.progress-bar {
	height: 100%;
	transition: width 0.6s ease;
}

.normalPair {
	width: 100%;
	display: flex;
	flex-direction: row;
	margin: 1% 0;
}
.normalPair .label {
	width: 10%;
	margin: 0;
	text-align: left;
	font-weight: 600;
	color: black;
}
.normalPair .value {
	width: 70%;
	margin: 0;
	display: flex;
	flex-direction: row;
	align-items: center;
	color: black;
}
</style>
