<template>
	<form @submit.prevent="sendForm">
		<div class="greeting">Create Your Account </div>
		<div class="pair">
			<label for="first_name">First Name</label>
			<input
				type="text"
				name="first_name"
				id="first_name"
				v-model="first_name"
				placeholder="Enter your first name"
				required
			/>
		</div>
		<div class="pair">
			<label for="last_name">Last Name</label>
			<input
				type="text"
				name="last_name"
				id="last_name"
				v-model="last_name"
				placeholder="Enter your last name"
				required
			/>
		</div>
		<div class="pair">
			<label for="email">Email</label>
			<input
				type="email"
				name="email"
				id="email"
				v-model="email"
				placeholder="Enter your email"
				required
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
				required
				@input="validatePassword"
			/>
			<!-- Password requirements indicator -->
			<div class="password-requirements" v-if="password">
				<div class="requirement" :class="{ met: hasMinLength }">
					<span class="check-icon">{{ hasMinLength ? '✓' : '✗' }}</span>
					At least 8 characters
				</div>
				<div class="requirement" :class="{ met: hasUpperCase }">
					<span class="check-icon">{{ hasUpperCase ? '✓' : '✗' }}</span>
					One uppercase letter
				</div>
				<div class="requirement" :class="{ met: hasLowerCase }">
					<span class="check-icon">{{ hasLowerCase ? '✓' : '✗' }}</span>
					One lowercase letter
				</div>
				<div class="requirement" :class="{ met: hasNumber }">
					<span class="check-icon">{{ hasNumber ? '✓' : '✗' }}</span>
					One number
				</div>
				<div class="requirement" :class="{ met: hasSpecialChar }">
					<span class="check-icon">{{ hasSpecialChar ? '✓' : '✗' }}</span>
					One special character
				</div>
			</div>
		</div>
		<div class="pair">
			<label for="confirmPassword">Confirm Password</label>
			<input
				type="password"
				name="confirmPassword"
				id="confirmPassword"
				v-model="confirmPassword"
				placeholder="Confirm your password"
				required
			/>
		</div>
		<input type="submit" value="Register"/>
	
		<div class="registerPrompt">
			Already have an account?
			<RouterLink :to="'/login'"> Login now</RouterLink>
		</div>
	</form>
</template>

<script>
import axios from 'axios';

export default {
	name: 'RegisterForm',
	data() {
		return {
			first_name: '',
			last_name: '',
			email: '',
			password: '',
			confirmPassword: '',
			hasMinLength: false,
			hasUpperCase: false,
			hasLowerCase: false,
			hasNumber: false,
			hasSpecialChar: false,
			isPasswordValid: false
		};
	},
	methods: {
		validatePassword() {
			this.hasMinLength = this.password.length >= 8;
			this.hasUpperCase = /[A-Z]/.test(this.password);
			this.hasLowerCase = /[a-z]/.test(this.password);
			this.hasNumber = /[0-9]/.test(this.password);
			this.hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(this.password);
			
			this.isPasswordValid = this.hasMinLength && 
								this.hasUpperCase && 
								this.hasLowerCase && 
								this.hasNumber && 
								this.hasSpecialChar;
		},
		async sendForm() {
			if (!this.isPasswordValid) {
				alert("Please ensure your password meets all requirements!");
				return;
			}
			if (this.password !== this.confirmPassword) {
				alert("Passwords don't match!");
				return;
			}

			const mutation = `
                mutation {
                    createUser(
                        firstName: "${this.first_name}",
                        lastName: "${this.last_name}",
                        email: "${this.email}",
                        password: "${this.password}",
                    ) {
                        success
                        user {
                            id
                            firstName
                            lastName
                            email
                        }
                        success
                    }
                }
            `;

			try {
				const response = await axios.post('http://localhost:5001/graphql/', {
					query: mutation,
				});

				console.log('User Created:', response.data);
				alert('User created successfully!');
				this.$router.push('/login');
			} catch (error) {
				console.error('Error creating user:', error);
				alert('Failed to register. Try again.');
			}
		},
	},
};
</script>

<style scoped>

.greeting {
    font-size: 28px;  /* or 32px */
    font-weight: bold;
    text-align: center;
    margin-bottom: 2rem;
	margin-left: 20px;
    color: rgb(36, 36, 138);
}

.registerPrompt {
	width: 100%;
	height: 90px;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

form {
	width: 40%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	padding: 2%;
	border-radius: 8px;
}

.pair {
	width: 100%;
	display: flex;
	flex-direction: column;
	margin-bottom: 15px;
}

.pair label {
	font-weight: bold;
	margin-bottom: 5px;
}

.pair input,
.pair select {
	width: 98%;
	border-radius: 8px;
	border: 1px solid rgb(248, 145, 162);
	padding: 10px 1%;
}

:is(input[type='submit']) {
	height: 45px;
	width: 100%;
	background-color: rgb(0, 0, 28);
	border: none;
	border-radius: 8px;
	color: white;
	padding: 10px;
	cursor: pointer;
}



.password-requirements {
	margin-top: 10px;
	padding: 15px;
	border-radius: 8px;
	background-color: #f8f9fa;
	border: 1px solid #e9ecef;
}

.requirement {
	margin: 8px 0;
	color: #dc3545;
	display: flex;
	align-items: center;
	font-size: 0.9em;
}

.requirement.met {
	color: #198754;
}

.check-icon {
	margin-right: 8px;
	font-weight: bold;
}

/* Additional styles for RouterLink */
a {
    color: rgb(39, 39, 132);  /* Dark blue/purple color to match other elements */
    text-decoration: none;
    font-weight: 500;
}

a:hover {
	text-decoration: underline;
}
</style>
