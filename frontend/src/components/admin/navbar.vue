<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h1>
        <span class="logo-icon">
          <img src="../../assets/icons/icons8-snowflake-100.png" alt="Logo" />
        </span>
        SkinVision
      </h1>
    </div>
    <!-- Move Admin section here, above the menu -->
    <div class="admin-section">
      <div class="admin-label">
        <span class="icon admin-icon">👤</span>
        <span>Admin</span>
      </div>
    </div>
    <ul class="sidebar-menu">
      <li :class="{ active: $route.path === '/admin/dashboard' }">
        <img src="../../assets/icons/icons8-speedometer-100.png" alt="Dashboard" />
        <router-link to="/admin/dashboard">Dashboard</router-link>
      </li>
      <li :class="{ active: $route.path === '/admin/users' }">
        <img src="../../assets/icons/icons8-users-100.png" alt="Users" />
        <router-link to="/admin/users">Users</router-link>
      </li>
    </ul>
    <div class="sidebar-footer">
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/admin/login');
    },
  },
};
</script>

<style scoped>
.sidebar {
  background: linear-gradient(135deg, #6a82fb 0%, #fc5c7d 100%);
  min-height: 100vh;
  width: 270px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Changed from flex-start to space-between */
  box-shadow: 2px 0 16px rgba(252, 92, 125, 0.07);
  border-radius: 0 2rem 2rem 0;
}

.sidebar-header {
  text-align: center;
  padding: 0.5rem 0 0;
  margin-bottom: 0; /* Remove bottom margin */
}

.sidebar-header h1 {
  font-size: 2rem;
  color: #fff;
  font-weight: bold;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
  margin-bottom: 0;
}

.logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(255,255,255,0.15);
  margin-right: 0.5rem;
  box-shadow: 0 2px 12px rgba(252, 92, 125, 0.13);
}
.logo-icon img {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

/* Menu Styles */
.sidebar-menu {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Increased gap between menu items */
}

.sidebar-menu li {
  width: 90%;
  margin: 0 auto;
  height: 35px;
  display: flex;
  align-items: center;
  margin-bottom: 0.6rem; /* Added additional spacing between items */
}

.sidebar-menu li img {
  width: 24px;
  height: 24px;
  margin-left: 20px;
  margin-right: 10px;
}

.sidebar-menu li a {
  margin-left: 0;
  text-decoration: none;
  color: #fff;
  font-size: 1.08rem;
  font-weight: 500;
  transition: color 0.15s;
  padding: 0.4rem 0.6rem;
  border-radius: 1rem;
  width: 100%;
  display: block;
}

/* Active and Hover States */
.sidebar-menu li.active {
  background: rgba(51, 48, 51, 0.28);
}

.sidebar-menu li.active a,
.sidebar-menu li:hover a {
  color: #fff;
}

.sidebar-menu li:hover {
  background: rgba(18, 13, 14, 0.18);
}

/* Admin section with gap */
.admin-section {
  margin-top: 0.5rem;
  margin-bottom: 1.5rem; /* Increased gap between admin and menu */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.admin-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  color: #fff;
  font-weight: 500;
  opacity: 0.90;
  font-size: 1.09rem;
}

.icon.admin-icon {
  font-size: 1.3rem;
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  padding: 2px 5px;
  margin-right: 2px;
}

/* Footer Styles */
.sidebar-footer {
  margin-top: auto; /* Push to bottom */
  padding-bottom: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.sidebar-footer button {
  background: #350fbc;
  color: #fff;
  border: none;
  padding: 0.85rem 2.7rem;
  border-radius: 2rem;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: bold;
  box-shadow: 0 2px 16px rgba(252, 92, 125, 0.15);
  transition: background 0.2s;
}

.sidebar-footer button:hover {
  background: #614be1;
}
</style>
