<template>
	<div class="dashLayout">
		<navBar />
		<router-view class="main" />
	</div>
</template>

<script>
import navBar from '../components/dashboard/navBar.vue';

export default {
	components: {
		navBar,
	},
};
</script>

<style scoped>
.dashLayout {
	grid-row: 1/101;
	grid-column: 1/101;
}

.main {
	grid-row: 7/101;
	grid-column: 1/101;
}
</style>
