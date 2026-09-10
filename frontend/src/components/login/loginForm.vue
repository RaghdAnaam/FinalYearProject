<template>
	<form @submit.prevent="sendForm">
		<div class="greeting">
			Welcome Back <img src="../../assets/icons/wave.png" alt="" />
		</div>
		<div class="pair">
			<label for="email">Email</label>
			<input
				type="email"
				name="email"
				id="email"
				v-model="email"
				placeholder="Enter your email"
			/>
		</div>
		<div class="pair">
			<label for="password">Password</label>
			<input
				type="password"
				name="password"
				id="password"
				v-model="password"
				placeholder="Enter your password"
			/>
		</div>
		<div class="forgotPassword" @click="forgotPassword()">Forgot Password?</div>
		<button type="submit">Login</button>
		<div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
		<div class="registerPrompt" style="margin-top: 5px">
			don't have an account?
			<RouterLink style="margin-left: 5px" to="/register"
				>Register now</RouterLink
			>
		</div>
		<div class="adminLogin" style="margin-top: 5px">
			<RouterLink to="/admin/login">Administrator Login</RouterLink>
		</div>
	</form>
</template>

<script>
import axios from 'axios';

export default {
	name: 'loginForm',
	data() {
		return {
			email: '',
			password: '',
			errorMessage: null,
		};
	},
	methods: {
		forgotPassword() {
			this.$router.push('/forgot-password');
		},
		async sendForm() {
			console.log('Entered');
			try {
				const response = await axios.post('https://skinvision-backend-2pho.onrender.com/graphql/', {
					query: `
                        mutation {
                            login(email: "${this.email}", password: "${this.password}") {
                                token
                            }
                        }
                    `,
				});

				console.log(response.data);
				const token = response.data.data.login.token;

				if (token && token !== 'Invalid email or password') {
					localStorage.setItem('token', token);
					this.$router.push('/dashboard'); // Redirect to a dashboard page
				} else {
					this.errorMessage = 'Invalid email or password';
				}
			} catch (error) {
				console.error('Login error:', error);
				this.errorMessage = 'Something went wrong. Please try again.';
			}
		},
	},
};
</script>

<style scoped>
.greeting {
	width: 100%;
	height: 90px;
	font-size: 36px;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	font-weight: 600;
	margin-bottom: 2rem;
}

button {
    padding: 12px 40px;  /* Increased padding */
    background-color: rgb(0, 0, 28);
    border: none;
    border-radius: 25px;
    color: white;
    font-size: 16px;     
    font-weight: 500;    
    width: 100%;         
    height: 45px;        
    cursor: pointer;    
    margin: 10px 0;     
}
.greeting :is(img) {
    height: 40px;  
    width: 40px;   
    margin-left: 15px; 
}
.registerPrompt {
	width: 100%;
	height: 90px;
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	justify-content: center;
	align-items: center;
	font-size: 16px;
}
.registerPrompt a {
    font-size: 16px;
    color: rgb(39, 39, 115);
    text-decoration: underline;
    font-weight: 600;
}

.registerPrompt a:hover {
    text-decoration: none;
}
adminLogin {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.adminLogin a {
    font-size: 16px;
    color: rgb(39, 39, 115);
    text-decoration: underline;
    font-weight: 600;
}

.adminLogin a:hover {
    text-decoration: underline;
}
.spacer {
	width: 100%;
	height: 50px;
}
.google {
	width: 100%;
	height: 45px;
	background-color: #ffffff;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	border-radius: 10px;
}

.google :is(img) {
	width: 35px;
	height: 35px;
	margin-right: 5px;
}

.google :is(p) {
	text-align: center;
	font-size: 14px;
	font-weight: 500;
	margin-left: 5px;
}
form {
	width: 50%;
	height: 50%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	/* background-color: rgb(255, 192, 203, 0.2); */
	/* box-shadow: 0 0 6.2px rgb(0, 0, 0, 0.2); */
	padding: 2%;
	border-radius: 8px;
}

.pair {
	width: 100%;
	display: flex;
	flex-direction: column;
}

.pair :is(label) {
	text-align: left;
	width: 100%;
	margin-bottom: 10px;
}

.pair :is(input) {
	width: 90%;
	border-radius: 8px;
	border: 1px solid rgb(248, 145, 162);
	padding: 2.5% 5%;
	margin-bottom: 20px;
}

.forgotPassword {
	width: 100%;
	text-align: right;
	margin-top: -10px;
	font-size: 0.8em;
	margin-bottom: 15px;
	color: blue;
	cursor: pointer;
}

:is(input[type='submit']) {
	height: 45px;
	width: 100%;
	background-color: rgb(0, 0, 28);
	border: none;
	border-radius: 8px;
	color: white;
	padding: 10px;
}

.error-message {
	color: red;
	text-align: center;
	margin-top: 10px;
	font-size: 14px;
}
</style>
