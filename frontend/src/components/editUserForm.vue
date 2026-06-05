<template>
	<div class="edit-form">
		<h2>Edit User</h2>
		
		<div v-if="error" class="error-message">
			{{ error }}
		</div>

		<form @submit.prevent="updateUser">
			<div class="form-group">
				<label for="firstName">First Name</label>
				<input 
					type="text"
					id="firstName"
					v-model="firstName"
					required
				/>
			</div>

			<div class="form-group">
				<label for="lastName">Last Name</label>
				<input 
					type="text"
					id="lastName"
					v-model="lastName"
					required
				/>
			</div>

			<div class="form-group">
				<label for="email">Email</label>
				<input 
					type="email"
					id="email"
					v-model="email"
					required
				/>
			</div>

			<div class="form-actions">
				<button 
					type="button" 
					class="cancel-btn" 
					@click="cancel"
					:disabled="loading"
				>
					Cancel
				</button>
				<button 
					type="submit" 
					class="update-btn"
					:disabled="loading"
				>
					{{ loading ? 'Updating...' : 'Update User' }}
				</button>
			</div>
		</form>
	</div>
</template>

<script>
import requests from '../utils/requests'

export default {
  name: 'EditUserForm',
  props: {
    id: {
      type: Number,
      required: true
    },
    userObject: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      firstName: this.userObject?.firstName || '',
      lastName: this.userObject?.lastName || '',
      email: this.userObject?.email || '',
      loading: false,
      error: null
    }
  },
  methods: {
    async updateUser() {
      try {
        this.loading = true
        this.error = null
        
        const query = `
          mutation UpdateUser(
            $id: Int!,
            $firstName: String!,
            $lastName: String!,
            $email: String!
          ) {
            updateUser(
              id: $id,
              firstName: $firstName,
              lastName: $lastName,
              email: $email
            ) {
              success
              message
              user {
                id
                firstName
                lastName
                email
                lastLogin
              }
            }
          }
        `

        const response = await requests(query, {
          variables: {
            id: this.id, // Remove String conversion since we're using Int
            firstName: this.firstName,
            lastName: this.lastName,
            email: this.email
          }
        })

        console.log('Update response:', response)

        if (!response?.data?.updateUser?.success) {
          throw new Error(response?.data?.updateUser?.message || 'Update failed')
        }

        // Emit success event to parent with updated user data
        this.$emit('user:updated', response.data.updateUser.user)
        this.$emit('update:closeOverlay')

      } catch (error) {
        console.error('Failed to update user:', error)
        this.error = error.response?.data?.errors?.[0]?.message || 
                    error.message || 
                    'Failed to update user. Please try again.'
      } finally {
        this.loading = false
      }
    },
    cancel() {
      this.$emit('update:closeOverlay')
    }
  }
}
</script>

<style scoped>
.edit-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.update-btn {
  background: #6c5ce7;
  color: white;
}

.cancel-btn {
  background: #e9ecef;
  color: #212529;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
