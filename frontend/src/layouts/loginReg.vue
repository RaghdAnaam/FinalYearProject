<template>
	<div class="container">
		<img class="imgCont" src="../assets/icons/facestuff.png" alt="" />
		<router-view class="main" />
	</div>
</template>

<script>
export default {
	name: 'LogRegLayout',
};
</script>

<style scoped>
.container {
	grid-row: 1/101;
	grid-column: 1/101;
	display: grid;
	grid-template-rows: repeat(100, 1%);
	grid-template-columns: repeat(100, 1%);
}
.main {
	grid-row: 2/100;
	grid-column: 2/50;
	display: grid;
}

.imgCont {
	grid-row: 2/100;
	grid-column: 51/100;
	min-height: 100%;
	max-height: 100%;
	min-width: 100%;
	max-width: 100%;
	overflow: hidden;
}
</style>
