<template>
	<div class="upload-container">
		<div
			class="drop-area"
			@dragover.prevent
			@drop="handleDrop"
			@click="triggerFileInput"
		>
			<input
				type="file"
				ref="fileInput"
				@change="handleFileSelect"
				accept="image/*"
				hidden
			/>
			<img
				v-if="imagePreview"
				:src="imagePreview"
				alt="Preview"
				class="preview"
			/>
			<div v-else class="placeholder">
				<p>Drag & drop your photo here</p>
				<p>OR</p>
				<button class="upload-btn">Upload Photo</button>
			</div>
		</div>

		<p class="recommendation" v-if="!submitted">
		We recommend taking a photo with good lighting and no filters
		</p>

		<button
			class="submit-btn"
			v-if="!submitted"
			@click="submitPhoto"
			:disabled="!selectedFile"
		>
			Submit for Analysis
		</button>
		<router-link
            v-if="processed && successMessage"
            to="/dashboard/analysis"
            class="analysis-btn"
        >
            View Analysis
        </router-link>
		
		<p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
		<p v-if="successMessage" class="success-message">{{ successMessage }}</p>
	</div>
</template>
<script>
import axios from 'axios';

export default {
	data() {
		return {
			selectedFile: null,
			imagePreview: null,
			errorMessage: null,
			successMessage: null,
			processed: false,
			submitted: false,
		};
	},
	methods: {
		triggerFileInput() {
			this.$refs.fileInput.click();
		},
		handleFileSelect(event) {
			const file = event.target.files[0];
			this.processFile(file);
		},
		handleDrop(event) {
			event.preventDefault();
			const file = event.dataTransfer.files[0];
			this.processFile(file);
		},
		processFile(file) {
			if (file && file.type.startsWith('image/')) {
				this.selectedFile = file;
				this.imagePreview = URL.createObjectURL(file);
				this.errorMessage = null;
			} else {
				this.errorMessage = 'Please upload a valid image file.';
			}
		},
		async submitPhoto() {
			if (!this.selectedFile) {
				this.errorMessage = 'No photo selected!';
				return;
			}

			const token = localStorage.getItem('token');
			if (!token) {
				this.errorMessage = 'Unauthorized: Please log in.';
				return;
			}
			this.submitted = true;
			const formData = new FormData();

			formData.append(
				'operations',
				JSON.stringify({
					query: `
                        mutation UploadPhoto($file: Upload!) {
                        uploadPhoto(photo: $file) {
                            id
                            imageUrl
                            analysis{
                                id
                            }
                        }
                        }
                    `,
					variables: {
						file: null,
					},
				}),
			);

			formData.append(
				'map',
				JSON.stringify({
					0: ['variables.file'], // This maps the uploaded file to 'variables.file'
				}),
			);

			formData.append('0', this.selectedFile);

			try {
				const response = await axios.post(
					'https://skinvision-backend-2pho.onrender.com/graphql/',
					formData,
					{
						headers: {
							Authorization: `Bearer ${token}`,
							'Content-Type': 'multipart/form-data',
						},
					},
				);

				const uploadedPhoto = response.data.data.uploadPhoto;
				this.processed = true;
				if (uploadedPhoto?.imageUrl) {
					this.successMessage =
						'Photo uploaded successfully! Please wait for analysis';
				} else {
					this.errorMessage = 'Upload failed.';
				}
			} catch (error) {
				this.processed = true;
				this.errorMessage =
					error.response?.data?.errors?.[0]?.message ||
					'Failed to upload photo. Please try again.';
				console.error(error);
			}
		},
	},
};
</script>

<style scoped>
.upload-container {
	width: 370px;
	min-height: 320px;
	margin: 0 auto;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: flex-start;
	background: none;
}

.drop-area {
	width: 100%;
	min-height: 170px;
	border: 2.5px dashed #a78bfa;
	border-radius: 16px;
	background: #f7f4ff;
	display: flex;
	justify-content: center;
	align-items: center;
	cursor: pointer;
	position: relative;
	transition: border-color 0.15s, box-shadow 0.15s;
	margin-bottom: 14px;
	box-shadow: 0 1px 12px #a78bfa14;
}
.drop-area.has-preview {
	background: #fff;
}
.placeholder p {
	color: #7c3aed;
	font-weight: 500;
	margin: 6px 0;
}
.upload-btn {
	background: linear-gradient(90deg, #ff5fa2 10%, #8f5fff 90%);
	color: #fff;
	border: none;
	padding: 9px 24px;
	border-radius: 11px;
	cursor: pointer;
	font-weight: 700;
	font-size: 1rem;
	margin-top: 3px;
	transition: background 0.2s, box-shadow 0.2s;
	box-shadow: 0 2px 8px #ff5fa233;
}
.upload-btn:hover,
.upload-btn:focus {
	background: linear-gradient(90deg, #8f5fff 0%, #3ecfff 100%);
}
.preview {
	max-width: 97%;
	max-height: 150px;
	object-fit: contain;
	border-radius: 12px;
	box-shadow: 0 2px 8px #7c3aed18;
}

.recommendation {
  color: #848b9a;
  font-size: 14.5px;
  margin-bottom: 10px;
  text-align: center;
  font-style: italic;
  width: 100%;
  max-width: 340px;      /* Adjust as needed for your modal width */
  margin: 0 auto 10px auto;
}


.submit-btn {
	background: linear-gradient(90deg, #4f8cff 0%, #38e4ff 100%);
	color: #fff;
	border: none;
	padding: 11px 30px;
	border-radius: 13px;
	cursor: pointer;
	font-weight: 700;
	font-size: 1.08rem;
	margin-top: 16px;
	transition: background 0.14s, box-shadow 0.12s, transform 0.1s;
	box-shadow: 0 2px 10px #38e4ff1b;
}
.submit-btn:disabled {
	background: #d2d2e9;
	color: #aaa;
	cursor: not-allowed;
}
.submit-btn:not(:disabled):hover,
.submit-btn:not(:disabled):focus {
	background: linear-gradient(90deg, #38e4ff 0%, #4f8cff 100%);
	transform: scale(1.04);
}


.error-message {
	color: #ef4444;
	font-size: 14px;
	margin-top: 10px;
}

.success-message {
	color: #10b981;
	font-size: 14px;
	margin-top: 10px;
}
.analysis-btn {
    background: linear-gradient(90deg, #ff5fa2 10%, #8f5fff 90%);
    color: #fff;
    border: none;
    padding: 11px 30px;
    border-radius: 13px;
    cursor: pointer;
    font-weight: 700;
    font-size: 1.08rem;
    margin-top: 16px;
    text-decoration: none;
    display: inline-block;
    transition: background 0.14s, box-shadow 0.12s, transform 0.1s;
    box-shadow: 0 2px 8px #ff5fa233;
}

.analysis-btn:hover,
.analysis-btn:focus {
    background: linear-gradient(90deg, #8f5fff 0%, #3ecfff 100%);
    transform: scale(1.04);
}
</style>