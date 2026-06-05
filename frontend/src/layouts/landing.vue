<template>
	<div class="container">
		<header class="header">
			<div class="logo">
				<img src="../assets/icons/icons8-snowflake-100.png" alt="" />
				<h1>SkinVision</h1>
			</div>
			<nav>
				<router-link class="link" to="/login">Login</router-link>
				<router-link class="link" to="/register">Register</router-link>
			</nav>
		</header>
		<router-view class="main" />
	</div>
</template>

<script>
export default {
	name: 'LandingLayout',
};
</script>

<style lang="css" scoped>
.logo {
	height: 100%;
	padding-left: 2.5%;
	width: 82.5%;
	align-items: center;
	display: flex;
}

.logo img {
	width: 45px;
	height: 45px;
}
.header {
	grid-row: 1/10;
	grid-column: 1/101;
	border-bottom: 1px solid lightgrey;
	display: flex;
	flex-direction: row;
}

.container {
	grid-row: 1/101;
	grid-column: 1/101;
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}

.header h1 {
	width: 100%;
	text-align: left;
}

.header nav {
	width: 10%;
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
}

.header nav .link {
	width: 50%;
	margin: 0;
	text-decoration: none;
	color: black;
}

.main {
	grid-row: 15/100;
	grid-column: 1/100;
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}
</style>
