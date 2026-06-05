<template>
	<div class="adminLayout">
		<navBar class="nav" />
		<router-view class="main" />
	</div>
</template>

<script>
import navBar from '../components/admin/navbar.vue';

export default {
	components: {
		navBar,
	},
};
</script>

<style scoped>
.adminLayout {
	grid-row: 1/101;
	grid-column: 1/101;
}
.nav {
	grid-row: 1/101;
	grid-column: 1/15;
}
.main {
	grid-row: 1/101;
	grid-column: 15/101;
}
</style>
