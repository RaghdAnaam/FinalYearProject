<template>
	<div class="forgot-password">
		<h2>Forgot your password?</h2>
		<input type="email" v-model="email" placeholder="Enter your email" />
		<button @click="requestReset">Send Reset Link</button>
		<p v-if="message">{{ message }}</p>
	</div>
</template>

<script>
export default {
	data() {
		return {
			email: '',
			message: '',
		};
	},
	methods: {
		async requestReset() {
			const query = `
                mutation($email: String!) {
                    requestPasswordReset(email: $email) {
                        success
                        message
                    }
                }
            `;
			const resp = await fetch('https://skinvision-backend-2pho.onrender.com/graphql/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					query,
					variables: { email: this.email },
				}),
			});
			const data = await resp.json();

			this.message = data.data.requestPasswordReset.message;
			window.alert(this.message);
		},
	},
};
</script>

<style scoped>
.forgot-password {
	width: 50%;
	height: 40%;
	margin: 30% 25%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	cursor: pointer;
}
input {
	width: 90%;
	height: 40px;
	border-radius: 5px;
	margin: 0 auto;
}

button {
	width: 50%;
	height: 40px;
	border-radius: 5px;
	margin: 10px auto;
	border: none;
	color: white;
	background-color: purple;
	cursor: pointer;
}
</style>
