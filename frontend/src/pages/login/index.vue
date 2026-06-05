<template>
	<div class="formHolder">
		<loginForm></loginForm>
	</div>
</template>

<script>
import loginForm from '../../components/login/loginForm.vue';
export default {
	components: {
		loginForm,
	},
};
</script>

<style scoped>
.formHolder {
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}
</style>
