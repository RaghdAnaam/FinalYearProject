<template>
	<div class="formHolder">
		<RegistrationForm></RegistrationForm>
	</div>
</template>

<script>
import RegistrationForm from '../../components/registration/registrationForm.vue';
export default {
	components: {
		RegistrationForm,
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
