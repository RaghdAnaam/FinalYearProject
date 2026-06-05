<template>
  <div class="login-bg">
    <div class="loginForm">
      <form @submit.prevent="">
        <div class="adminTitle">
          <span class="admin-icon">👤</span>
          Admin Login
        </div>
        <div class="pair">
          <label for="email">Email</label>
          <input
            type="email"
            name="email"
            id="email"
            v-model="email"
            :disabled="loading"
            required
            autocomplete="username"
          />
        </div>
        <div class="pair">
          <label for="password">Password</label>
          <input
            type="password"
            name="password"
            id="password"
            v-model="password"
            :disabled="loading"
            required
            autocomplete="current-password"
          />
        </div>
        <button
          class="submit"
          @click.prevent="login"
          :disabled="loading"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      email: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async login() {
      if (!this.email || !this.password) {
        alert('Please enter both email and password')
        return
      }

      try {
        this.loading = true
        const response = await axios.post('http://localhost:5001/graphql/', {
          query: `
            mutation ($email: String!, $password: String!) {
              loginAdmin(email: $email, password: $password) {
                success
                message
                token
              }
            }
          `,
          variables: {
            email: this.email,
            password: this.password
          }
        })

        const { success, message, token } = response.data.data.loginAdmin

        if (success && token) {
          localStorage.setItem('token', token)
          this.$router.push('/admin/dashboard')
        } else {
          alert(message || 'Login failed')
        }
      } catch (error) {
        console.error('Login error:', error)
        alert(error.response?.data?.errors?.[0]?.message || 'Login failed')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  background: transparent;
  display: flex;
  justify-content: flex-start;
  align-items: stretch;
}

.loginForm {
  min-width: 340px;
  max-width: 410px;
  margin: auto 0 auto 7vw;
  background: rgba(255,255,255,0.27);
  backdrop-filter: blur(5px);
  border-radius: 30px;
  box-shadow: 0 6px 32px rgba(252, 92, 125, 0.10), 0 1.5px 10px rgba(106,130,251,0.07);
  padding: 42px 40px 36px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.adminTitle {
  width: 100%;
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  color: #23113b;
  margin-bottom: 20px;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
}

.admin-icon {
  font-size: 1.45rem;
  background: rgba(252,92,125,0.18);
  border-radius: 50%;
  padding: 7px 10px 7px 9px;
}

.pair {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
}

.pair label {
  font-size: 1.06rem;
  font-weight: 500;
  color: #23113b;
}

.pair input {
  width: 260px;
  max-width: 350px;
  height: 36px;
  padding: 0 17px;
  border: 2px solid #eebbc3;
  border-radius: 19px;
  font-size: 1rem;
  font-family: inherit;
  background: rgba(255,255,255,0.7);
  outline: none;
  transition: border 0.18s, box-shadow 0.15s;
}
.pair input:focus {
  border: 2px solid #fc5c7d;
  box-shadow: 0 0 8px #fc5c7d55;
  background: #fff;
}

.submit {
  height: 38px;
  width: 60%;
  min-width: 130px;
  margin: 12px auto 0 auto;
  border-radius: 20px;
  background: linear-gradient(90deg, #fc5c7d 40%, #6a82fb 100%);
  color: #fff;
  border: none;
  font-size: 1.12rem;
  font-weight: 600;
  letter-spacing: 0.2px;
  box-shadow: 0 2px 16px rgba(252, 92, 125, 0.13);
  cursor: pointer;
  transition: background 0.15s, opacity 0.13s;
  opacity: 1;
}
.submit:disabled {
  background: #f3eff0;
  color: #eee9ed;
  cursor: not-allowed;
  opacity: 0.75;
}
@media (max-width: 900px) {
  .loginForm {
    margin: 0 auto;
    min-width: 95vw;
    max-width: 97vw;
    padding: 24px 8vw 26px 8vw;
  }
  .pair input {
    width: 90vw;
    max-width: 97vw;
  }
}
</style>
