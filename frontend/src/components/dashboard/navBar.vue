<template>
  <nav class="navbar">
    <div class="logo">
      <span class="icon">
        <img src="../../assets/icons/icons8-snowflake-100.png" alt="" />
      </span>
      <span class="brand">SkinVision</span>
    </div>
    <ul class="nav-links">
      <li><RouterLink :to="'/dashboard'">Dashboard</RouterLink></li>
      <li><RouterLink :to="'/dashboard/analysis'">Analysis</RouterLink></li>
      <li><RouterLink :to="'/dashboard/progress'">Progress</RouterLink></li>
      <li><RouterLink :to="'/dashboard/routines'">Routine</RouterLink></li>
    </ul>
    <div class="profile-icon" @click="togglePanel()">
      <span class="icon">👤</span>
      <span v-if="userName" class="user-name">&nbsp;{{ userName }}</span>
    </div>
    <div class="userPanel" v-if="openPanel">
      <div v-if="userName" class="user-info">
        <b>{{ userName }}</b>
        <hr style="margin: 5px 0;">
      </div>
      <div class="menu-item" @click="editProfile">Edit Profile</div>
      <div class="logout" @click="logout()">Logout</div>
    </div>

    <!-- Edit Profile Modal -->
    <EditProfileForm
      v-if="showEditProfile"
      :show="showEditProfile"
      @close="showEditProfile = false"
      @updated="handleProfileUpdate"
    />

    <!-- Success message -->
    <p v-if="updateMsg" class="update-success">{{ updateMsg }}</p>
  </nav>
</template>

<script>
import EditProfileForm from '../profile/editProfileForm.vue';
import { fetchCurrentUser } from '../../utils/userApi.js';

export default {
  name: 'navBar',
  components: { EditProfileForm },
  data() {
    return {
      openPanel: false,
      showEditProfile: false,
      userName: '',
      updateMsg: '', // For update notification
    };
  },
  async mounted() {
    // Always get the user's name at mount
    const user = await fetchCurrentUser();
    if (user) {
      this.userName = `${user.firstName} ${user.lastName}`;
    }
  },
  methods: {
    togglePanel() {
      this.openPanel = !this.openPanel;
    },
    logout() {
      this.$router.push('/login');
    },
    editProfile() {
      this.openPanel = false;
      this.showEditProfile = true;
    },
    async handleProfileUpdate(userData, message) {
      this.showEditProfile = false;
      // Always fetch new data after update!
      const user = await fetchCurrentUser();
      if (user) {
        this.userName = `${user.firstName} ${user.lastName}`;
      }
      // Show the update message if available
      if (message) {
        this.updateMsg = message;
        setTimeout(() => { this.updateMsg = ''; }, 3000);
      }
    },
  },
};
</script>
<style scoped>
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  width: 100%;
  display: flex;
  align-items: center;
  background: white;
  padding: 0 24px; /* slightly less padding */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  min-height: 54px; /* shorter navbar */
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 1.7rem;
  flex: 0 0 auto;
  margin-right: 24px;
}

.icon img {
  height: 28px !important;  /* smaller icon */
  width: 28px !important;
  margin-right: 7px;
}

.brand {
  font-size: 1.7rem;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 32px;
  margin: 0;
  padding: 0;
  align-items: center;
  flex: 1 1 0;
  justify-content: center;
}

.nav-links li {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-links a {
  position: relative;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  display: flex;
  align-items: center;
  padding: 5px 0;
  transition: color 0.2s;
}

.nav-links a:hover::after,
.nav-links a.router-link-exact-active::after {
  content: '';
  position: absolute;
  left: 0; right: 0; bottom: -2px;
  height: 3px;
  background: #C26EFF;
  border-radius: 2px;
}
.nav-links a:hover,
.nav-links a.router-link-exact-active {
  color: #C26EFF;
}

.profile-icon {
  min-width: 36px;
  max-width: 210px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  border-radius: 30px;
  background: #e6e6e6;
  cursor: pointer;
  padding: 0 8px;
  margin-right: 16px;      /* Pull profile icon away from right edge */
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.profile-icon .icon {
  font-size: 16px;
}

.user-name {
  font-size: 1rem;
  color: #6c43a6;
  margin-left: 3px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 130px;      /* Truncate long names gracefully */
  display: inline-block;
  vertical-align: middle;
}

.userPanel {
  position: absolute;
  top: 60px; right: 20px;
  width: 200px;
  padding: 10px 0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  background-color: pink;
  box-shadow: 0 0 6.2px rgb(0 0 0 / 20%);
  z-index: 1100;
}
.user-info {
  padding: 10px 20px 5px 20px;
  color: #6c43a6;
  text-align: center;
  font-size: 1rem;
}
.menu-item {
  padding: 10px 20px;
  cursor: pointer;
}
.menu-item:hover {
  background-color: #f5f5f5;
}
.logout {
  width: 90%; margin: 0 5%;
  font-weight: 600; padding: 10px 0;
  border-radius: 6px;
  color: #ff4444;
  border-top: 1px solid #eee;
  margin-top: 5px;
}
.logout:hover {
  background-color: purple;
  color: white;
}

.edit-profile-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

/* Responsive: */
@media (max-width: 900px) {
  .navbar {
    flex-direction: column;
    align-items: stretch;
    padding: 0 8px;
    min-height: 80px;
    gap: 8px;
  }
  .logo { font-size: 1.2rem; }
  .icon img { height: 20px !important; width: 20px !important; }
  .nav-links { flex-direction: column; gap: 7px; }
  .profile-icon { margin-right: 0; align-self: flex-end; }
}

.update-success {
  position: fixed;
  top: 70px;
  right: 30px;
  background: #4ade80;
  color: #18181b;
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.02rem;
  z-index: 1200;
  box-shadow: 0 2px 12px #1e293b18;
}

</style>
