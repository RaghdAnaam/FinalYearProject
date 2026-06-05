// HeroSection.vue
<template>
    <section class="hero">
        <h2>Start Monitoring Your Skin Health!</h2>
        <p>Access tools for better skin diagnosis.</p>
        <div class="button-container">
            <router-link class="register" :to="'/register'">Register</router-link>
            <router-link class="login" :to="'login'">Log In</router-link>
        </div>
    </section>
</template>

<script>
export default {
    name: 'HeroSection'
};
</script>

<style lang="css" scoped>
.hero {
    position: relative;
    background-image: url('../assets/herobg.jpeg');
    background-size: 100% auto;
    background-repeat: no-repeat;
    background-position: left top;
    grid-row: 15/70;
    grid-column: 10/90;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 4rem 2rem;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(134, 127, 140, 0.5);
    border-radius: 10px;
}

.hero h2 {
    position: relative;
    z-index: 1;
    color: white;
    font-size: 48px;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    margin-bottom: 1rem;
    text-align: center;
}

.hero p {
    position: relative;
    z-index: 1;
    color: white;
    font-size: 28px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    margin-bottom: 2rem;
    text-align: center;
}

.button-container {
    position: relative;
    z-index: 1;
    display: flex;
    gap: 20px;
    justify-content: center;
}

.register {
    background-color: #C26EFF;
    padding: 12px 32px;
    border-radius: 20px;
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    transition: background-color 0.3s ease;
}

.register:hover {
    background-color: #a64dff;
}

.login {
     background-color: #C26EFF;
    padding: 12px 32px;
    border-radius: 20px;
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    transition: background-color 0.3s ease;
}

.login:hover {
    background-color: #a64dff;
    
}
</style>