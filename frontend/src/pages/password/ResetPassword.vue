<template>
	<div class="reset-password">
		<h2>Set a New Password</h2>
		<input type="password" v-model="password" placeholder="New Password" />
		<button @click="submitReset">Reset Password</button>
		<p v-if="message">{{ message }} <p @click="loginRedirect()"><u>login</u></p></p>
	</div>
</template>

<script>
export default {
	data() {
		return {
			password: '',
			message: '',
		};
	},
	methods: {
        loginRedirect() {
            this.$router.push('/login');
        },
		async submitReset() {
			const token = this.$route.query.token;
			const query = `
				mutation($token: String!, $newPassword: String!) {
					resetPassword(token: $token, newPassword: $newPassword) {
						success
						message
					}
				}
			`;
			const resp = await fetch('http://localhost:5001/graphql/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					query,
					variables: {
						token,
						newPassword: this.password,
					},
				}),
			});
			const data = await resp.json();
			this.message = data.data.resetPassword.message;
		},
	},
};
</script>
<style scoped>
.reset-password {
	width: 50%;
	height: 40%;
	margin: 30% 25%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
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
