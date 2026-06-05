<template>
	<div class="usersPage">
		<div class="title">User management</div>
		<div class="search">
			<input
				type="text"
				name="searchterm"
				id="searchterm"
				v-model.trim="searchTerm"
				placeholder="Search by name or email"
				@keyup.enter="search()"
			/>
			<div v-if="error" class="error-message">{{ error }}</div>
		</div>
		<div class="table">
			<div class="tableLabels">
				<div class="name">First Name</div>
				<div class="name">Last Name</div>
				<div class="email">Email</div>
				<div class="status">Account Status</div>
				<div class="status">Last Login</div>
				<div class="actBtns">Actions</div>
			</div>
			<div class="tableData" v-if="users && total != 0">
				<div class="row" v-for="user in users">
					<div class="name dataName">{{ user.firstName }}</div>
					<div class="name dataname">{{ user.lastName }}</div>
					<div class="email dataEmail">{{ user.email }}</div>
					<div class="status dataStatus" :class="{ 
  'active-status': user.lastLogin, 
  'inactive-status': !user.lastLogin 
}">
						{{ user.lastLogin ? 'Active' : 'Inactive' }}
					</div>
					<div class="status dataStatus">{{ date(user.lastLogin) }}</div>
					<div class="actBtns dataBtns">
						<div class="button" @click="openEditForm(user)">Edit</div>
						<div class="separator">|</div>
						<div class="button" @click="deleteUser(user.email)">Delete</div>
					</div>
				</div>
			</div>
			<div v-else class="tableDataSearch">No Users Found</div>
			<div class="pagination" v-if="total != 0">
				<div class="firstPage" v-if="total != 1">1</div>
				<div class="ellipses" v-if="total != 1">...</div>
				<div class="prev" v-if="page - 1 > 1">{{ page - 1 }}</div>
				<div class="current">{{ page }}</div>
				<div class="prev" v-if="page + 1 < total">{{ page + 1 }}</div>
				<div class="ellipses" v-if="total != 1">...</div>
				<div class="lastPage" v-if="total != 1">total</div>
			</div>
		</div>
		<div class="userEditForm" v-if="openEdit">
			<editUserForm
				:id="focusedId"
				:user-object="focusedUser"
				@update:closeOverlay="openEditForm"
				@user:updated="handleUserUpdate"
			></editUserForm>
		</div>
	</div>
</template>

<script>
import requests from '../../utils/requests';
import editUserForm from '../../components/editUserForm.vue';
export default {
	data() {
		return {
			users: null,
			page: 1,
			perPage: 10,
			total: 0,
			searchTerm: null,
			openEdit: false,
			focusedId: null,
			focusedUser: null,
		};
	},
	components: {
		editUserForm,
	},
	async mounted() {
		await this.getUsers();
	},
	methods: {
		date(s) {
			return new Date(s).toLocaleDateString();
		},
		async getUsers(page) {
			try {
				if (page) {
					this.page = page;
				}

				const query = `
        query GetUsers($page: Int!, $perPage: Int!) {
          allUsers(page: $page, perPage: $perPage) {
            total
            pages
            page
            perPage
            users {
              id
              firstName
              lastName
              email
              lastLogin
            }
          }
        }
      `;

				const resp = await requests(query, {
					variables: {
						page: this.page,
						perPage: this.perPage,
					},
				});

				console.log('Raw response:', resp); // Debug log

				// Correct response validation
				if (!resp?.data?.allUsers) {
					throw new Error('Invalid response structure');
				}

				const { users, total, pages } = resp.data.allUsers;

				// Validate data
				if (!Array.isArray(users)) {
					throw new Error('Users data is not an array');
				}

				this.users = users;
				this.total = total;
				this.pages = pages;
			} catch (error) {
				console.error('Failed to fetch users:', error);
				this.users = [];
				this.total = 0;
				this.error = 'Failed to load users. Please try again.';
			}
		},
		async search(page) {
			try {
				if (page) {
					this.page = page;
				}

				// Don't search if search term is empty
				if (!this.searchTerm?.trim()) {
					return this.getUsers(this.page);
				}

				const query = `
      query SearchUsers($search: String!, $page: Int!, $perPage: Int!) {
        searchUsers(search: $search, page: $page, perPage: $perPage) {
          total
          pages
          page
          perPage
          users {
            id
            firstName
            lastName
            email
            lastLogin
          }
        }
      }
    `;

				const resp = await requests(query, {
					variables: {
						search: this.searchTerm.trim(),
						page: this.page,
						perPage: this.perPage,
					},
				});

				// Validate response
				if (!resp?.data?.searchUsers) {
					throw new Error('Invalid search response structure');
				}

				const { users, total, page: currentPage } = resp.data.searchUsers;

				if (!Array.isArray(users)) {
					throw new Error('Search results are not in expected format');
				}

				this.users = users;
				this.total = total;
				this.page = currentPage;
			} catch (error) {
				console.error('Search failed:', error);
				this.users = [];
				this.total = 0;
				this.error = 'Search failed. Please try again.';
			}
		},
		openEditForm(user = null) {
			this.openEdit = !this.openEdit;
			if (user) {
				this.focusedId = parseInt(user.id, 10);
				this.focusedUser = user;
			}
		},
		async deleteUser(email) {
			if (!confirm(`Are you sure you want to delete the user ${email}?`))
				return;

			const token = localStorage.getItem('token');

			const query = `
		mutation DeleteUser($email: String!) {
			deleteUser(email: $email) {
				success
				message
			}
		}
	`;

			try {
				const response = await fetch('http://localhost:5001/graphql/', {
					method: 'POST',
					headers: {
						Authorization: `Bearer ${token}`,
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						query,
						variables: { email },
					}),
				});

				const result = await response.json();
				const { success, message } = result.data.deleteUser;

				if (success) {
					alert('User deleted successfully.');
					this.getUsers?.();
				} else {
					alert('Failed to delete user: ' + message);
				}
			} catch (error) {
				console.error('Error deleting user:', error);
				alert('Something went wrong while deleting the user.');
			}
		},
		async handleUserUpdate(updatedUser) {
			try {
				// Update the local users array with the updated user data
				const userIndex = this.users.findIndex(u => u.id === updatedUser.id)
				if (userIndex !== -1) {
					this.users[userIndex] = { ...this.users[userIndex], ...updatedUser }
				}
				
				// Refresh the users list to ensure sync with backend
				await this.getUsers(this.page)
				
			} catch (error) {
				console.error('Error handling user update:', error)
			}
		}
	},
};
</script>

<style scoped>
.userEditForm {
	position: absolute;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
}
.pagination {
	grid-row: 91/101;
	grid-column: 1/101;
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
	font-size: 18px;
	font-weight: 600;
}

.current {
	font-size: 22px;
	text-decoration: underline;
}
input[type='text'] {
	height: 100%;
	width: 30%;
	border: none;
	background-color: rgba(130, 110, 173, 0.6);
	border-radius: 20px;
	box-shadow: 0 0 6.2px rgb(0, 0, 0, 0.2);
}
.button {
	text-align: center;
	cursor: pointer;
	text-decoration: underline;
	color: limegreen;
	font-weight: 600;
}

.separator {
	padding: 0 5px;
	color: limegreen;
	font-weight: 600;
}
.dataBtns {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
}
.row {
	display: flex;
	flex-direction: row;
	align-items: center;
	height: 60px;
	background: #f8f4f4;
}
.tableData {
	grid-row: 10/91;
	grid-column: 1/101;
	display: flex;
	flex-direction: column;
	overflow-y: scroll;
}

.tableDataSearch {
	grid-row: 10/91;
	grid-column: 1/101;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	overflow-y: scroll;
	font-size: 28px;
	font-weight: 600;
}
.name {
	width: 10%;
}
.email {
	width: 30%;
}

.status {
	width: 15%;
}
.actBtns {
	width: 20%;
}
.title {
	grid-row: 1/10;
	grid-column: 2/100;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 30px;
	font-weight: 600;
}

.search {
	grid-row: 10/13; /* Adjusted from 8/11 to move down more */
	grid-column: 10/100;
	display: flex;
	justify-content: flex-start;
	position: relative;
}

input[type='text'] {
	padding: 0.5rem 1rem;
	font-size: 1rem;
	outline: none;
}

input[type='text']:focus {
	box-shadow: 0 0 6.2px rgba(200, 184, 187, 0.5);
}

.table {
    grid-row: 16/98; /* Expanded from 16/91 to 16/95 */
    grid-column: 10/91; /* Expanded from 10/91 to 5/95 */
    display: grid;
    grid-template-rows: repeat(100, 1%);
    grid-template-columns: repeat(100, 1%);
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 0 6.2px rgb(18, 13, 14);
}
.tableLabels {
	grid-row: 1/10;
	grid-column: 1/101;
	display: flex;
	flex-direction: row;
	align-items: center;
	background-color: white;
	box-shadow: 0 0 6.2px rgb(0, 0, 0, 0.5);
	z-index: 100;
}

.usersPage {
	width: 100%;
	height: 100%;
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}

.error-message {
	color: #dc3545;
	font-size: 0.875rem;
	margin-top: 0.5rem;
}

.active-status {
  color: rgba(73, 209, 255, 0.8); /* Purple for active users */
  font-weight: 600;
}

.inactive-status {
  color: rgba(255, 183, 121, 0.8); /* Red for inactive users */
  font-weight: 600;
}
</style>
