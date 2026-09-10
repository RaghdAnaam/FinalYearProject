<template>
	<div>
		<h1>Photo History</h1>
		<div v-if="loading">Loading...</div>
		<div v-else>
			<div v-if="error" class="error">Error: {{ error }}</div>
			<div v-if="photos && photos.length">
				<div v-for="photo in photos" :key="photo.id" class="photo-item">
					<img
						:src="'data:image/png;base64, ' + photo.imageB64"
						alt="photo"
						class="photo-image"
					/>
					<p>{{ photo.id }}</p>
				</div>
			</div>
			<div v-else>
				<p>No photos found</p>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			photos: [], // List of photos
			loading: true, // Loading state
			error: null, // Error state
		};
	},
	methods: {
		async fetchPhotos() {
			try {
				// Fetch the photos using the GraphQL API

				const token = localStorage.getItem('token');
				const response = await fetch('https://skinvision-backend-2pho.onrender.com/graphql/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`,
					},
					body: JSON.stringify({
						query: `
                            query {
                                userPhotos {
                                userId
                                analysis{
                                    id
                                }
                                photoLink
                                imageB64
                                }
                            }
                            `,
					}),
				});

				const data = await response.json();

				if (data.errors) {
					throw new Error('Error fetching data');
				}

				this.photos = data.data.userPhotos;
			} catch (error) {
				this.error = error.message;
			} finally {
				this.loading = false;
			}
		},
	},
	mounted() {
		this.fetchPhotos();
	},
};
</script>

<style scoped>
.photo-item {
	margin-bottom: 20px;
}

.photo-image {
	width: 100%;
	max-width: 300px;
	height: auto;
}

.error {
	color: red;
}
</style>
