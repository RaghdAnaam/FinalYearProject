<template>
  <div class="edit-profile-overlay" v-if="show">
    <div class="edit-profile-modal">
      <button class="close-btn" @click="$emit('close')" aria-label="Close">&times;</button>
      <div class="form-card">
        <h1>Profile</h1>
        <p class="subtitle">Update your personal details</p>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="firstName">First Name</label>
            <input
              type="text"
              id="firstName"
              v-model="formData.firstName"
              required
            />
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input
              type="text"
              id="lastName"
              v-model="formData.lastName"
              required
            />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="formData.email"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">New Password</label>
            <input
              type="password"
              id="password"
              v-model="formData.password"
              minlength="6"
              placeholder="Enter new password"
            />
          </div>
          <div class="form-group">
            <label for="confirmPassword">Confirm New Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="formData.confirmPassword"
              minlength="6"
              placeholder="Re-enter new password"
            />
          </div>
          <p v-if="error" class="error-message">{{ error }}</p>
          <div class="button-group">
            <button type="button" class="cancel-btn" @click="$emit('close')">
              Cancel
            </button>
            <button type="submit" class="save-btn" :disabled="loading">
              {{ loading ? 'Saving...' : 'Update' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import requests from '../../utils/requests';

export default {
  name: 'EditProfileForm',
  props: { show: { type: Boolean, required: true } },
  emits: ['close', 'updated'],
  data() {
    return {
      formData: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      error: null,
      loading: false
    };
  },
  async created() {
    await this.getCurrentUser();
  },
  methods: {
    async getCurrentUser() {
      const query = `query {
        currentUser {
          firstName
          lastName
          email
        }
      }`;
      try {
        const response = await requests(query);
        if (response.data?.currentUser) {
          this.formData.firstName = response.data.currentUser.firstName;
          this.formData.lastName = response.data.currentUser.lastName;
          this.formData.email = response.data.currentUser.email;
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async handleSubmit() {
      if (this.formData.password) {
        if (this.formData.password.length < 6) {
          this.error = "Password must be at least 6 characters.";
          return;
        }
        if (this.formData.password !== this.formData.confirmPassword) {
          this.error = "Passwords do not match.";
          return;
        }
      }
      const mutation = `
        mutation UpdateProfile(
          $firstName: String!
          $lastName: String!
          $email: String!
          $password: String
        ) {
          updateProfile(
            firstName: $firstName
            lastName: $lastName
            email: $email
            password: $password
          ) {
            success
            message
            user {
              firstName
              lastName
              email
            }
            token
          }
        }
      `;
      this.loading = true;
      this.error = null;
      try {
        const variables = {
          firstName: this.formData.firstName,
          lastName: this.formData.lastName,
          email: this.formData.email,
        };
        if (this.formData.password) {
          variables.password = this.formData.password;
        }
        // This is KEY: wrap variables in { variables } when using axios-style GraphQL
        const response = await requests(mutation, { variables });
        const updateProfile = response.data?.updateProfile || response?.data?.data?.updateProfile;
        if (updateProfile?.success) {
          if (updateProfile.token) {
            localStorage.setItem('token', updateProfile.token);
          }
          // Send back both user and message!
          this.$emit('updated', updateProfile.user, updateProfile.message);
          this.$emit('close');
        } else {
          this.error =
            updateProfile?.message ||
            response.message ||
            'Update failed.';
        }
      } catch (error) {
        this.error = error.message || 'An unexpected error occurred.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>


<style scoped>
.edit-profile-overlay {
  position: fixed;
  inset: 0;
  background: #fff;
  z-index: 2000;
  min-height: 100vh;
  min-width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-profile-modal {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
}

.form-card {
  width: 100%;
  max-width: 370px;
  background: linear-gradient(120deg, #f3e8ff 0%, #dbeafe 100%);
  border-radius: 20px;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  box-shadow: 0 4px 32px 0 rgba(80, 12, 109, 0.12), 0 1.5px 6px 0 rgba(64, 200, 224, 0.08);
  position: relative;
  margin: 0 20px;
}

.close-btn {
  position: absolute;
  right: 18px;
  top: 18px;
  background: none;
  border: none;
  font-size: 2rem;
  color: #818cf8;
  cursor: pointer;
  z-index: 10;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #312e81;
}

h1 {
  margin-top: 0;
  margin-bottom: 0.2rem;
  color: #18181b;
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  letter-spacing: -1px;
}
.subtitle {
  margin-bottom: 1.5rem;
  color: #6366f1;
  font-size: 1.02rem;
  font-weight: 500;
  text-align: center;
}

.form-group {
  margin-bottom: 1.1rem;
  width: 92%;
  margin-left: auto;
  margin-right: auto;
}

label {
  display: block;
  margin-bottom: 0.22rem;
  font-weight: 600;
  color: #312e81;
  font-size: 1rem;
  text-align: left;
  margin-left: 2px;
}

input {
  width: 100%;
  padding: 0.54rem 0.75rem;
  border: 1.5px solid #818cf8;
  border-radius: 10px;
  font-size: 0.98rem;
  background: #fff;
  outline: none;
  transition: border 0.2s, background 0.2s;
  display: block;
  margin-top: 0.18rem;
}
input:focus {
  border: 1.8px solid #38bdf8;
  background: #f1f5f9;
}

.error-message {
  color: #e1004d;
  background: #e8fbff;
  border-radius: 8px;
  padding: 0.7em 0.5em;
  margin-top: 0.3em;
  margin-bottom: 0.3em;
  text-align: center;
  font-size: 0.97rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.2rem;
  justify-content: center;
  width: 92%;
  margin-left: auto;
  margin-right: auto;
}
.save-btn,
.cancel-btn {
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 14px;
  padding: 0.67em 2em;
  cursor: pointer;
  transition: background 0.18s, color 0.18s, opacity 0.2s, box-shadow 0.2s;
}

.save-btn {
  background: linear-gradient(90deg, #818cf8 0%, #38bdf8 100%);
  color: #fff;
  box-shadow: 0 2px 6px #aeefff7d;
}

.save-btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  background: #fff;
  color: #6366f1;
  border: 2px solid #6366f1;
  box-shadow: 0 1px 2px #c5ebf480;
}
.cancel-btn:hover {
  background: #e0e7ff;
  color: #312e81;
}
.save-btn:hover {
  background: linear-gradient(90deg, #6366f1 0%, #38bdf8 100%);
  color: #fff;
}

/* Responsive tweaks */
@media (max-width: 600px) {
  .form-card {
    max-width: 98vw;
    padding: 1.1rem 0.7rem;
  }
  .close-btn {
    right: 4vw;
    top: 10px;
  }
  h1 { font-size: 1.08rem; }
}
</style>
