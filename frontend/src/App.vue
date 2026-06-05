<template>
	<component :is="layout" class="test" />
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import LandingLayout from './layouts/landing.vue';
import LoginRegLayout from './layouts/loginReg.vue';
import DashboardLayout from './layouts/dashboardLayout.vue';
import AdminLayout from './layouts/adminLayout.vue';

export default {
	setup() {
		const route = useRoute();

		const layout = computed(() => {
			console.log('Current Layout:', route.meta.layout);
			if (route.meta.layout === 'landing') return LandingLayout;
			if (route.meta.layout === 'LogReg') return LoginRegLayout;
			if (route.meta.layout === 'Dashboard') return DashboardLayout;
			if (route.meta.layout === 'admin') return AdminLayout;
			return 'div';
		});

		return { layout };
	},
};
</script>

<style lang="css" scoped>
body {
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}
.test {
	grid-row: 1/101;
	grid-column: 1/101;
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}

#app {
	grid-row: 1/101;
	grid-column: 1/101;
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}

.main {
	grid-row: 1/101;
	grid-column: 1/101;
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}
</style>
