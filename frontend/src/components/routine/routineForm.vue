<template>
	<div>
		<div class="top">
			<h2>Create Routine</h2>
			<div class="closeBtn"><p @click="closeOverlay()">+</p></div>
		</div>
		<form @submit.prevent="submitRoutine">
			<div class="pair">
				<label>Routine Name:</label>
				<input v-model="routine.name" required />
			</div>
			<div class="pair">
				<label>Description:</label>
				<textarea v-model="routine.description"></textarea>
			</div>

			<h3>Products</h3>
			<div
				class="prodItem"
				v-for="(product, index) in routine.products"
				:key="index"
			>
				<input v-model="product.name" placeholder="Product Name" required />
				<select v-model="product.category" required>
					<option disabled value="">Select Category</option>
					<option
						v-for="category in categories"
						:key="category"
						:value="category"
					>
						{{ category }}
					</option>
				</select>
				<!-- Replace the input with select -->
				<select v-model="product.timeOfUse" required class="lastChild">
					<option disabled value="">Select Time</option>
					<option value="AM">AM</option>
					<option value="PM">PM</option>
					<option value="AM & PM">AM & PM</option>
				</select>
				<button class="removeBtn" type="button" @click="removeProduct(index)">
					Remove
				</button>
			</div>
			<button type="button" class="addProd" @click="addProduct">
				Add Product
			</button>
			<button type="submit" class="subForm">Submit</button>
		</form>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			routine: {
				name: '',
				description: '',
				products: [],
			},
			categories: [
				'Cleansers',
				'Exfoliators',
				'Toners',
				'Serums & Treatments',
				'Moisturizers',
				'Sunscreens',
				'Eye Creams',
				'Face Oils',
				'Masks',
				'Spot Treatments',
			],
		};
	},
	methods: {
		addProduct() {
			this.routine.products.push({ name: '', category: '', timeOfUse: '' });
		},
		removeProduct(index) {
			this.routine.products.splice(index, 1);
		},
		async submitRoutine() {
			const mutation = `
        mutation CreateRoutine($name: String!, $description: String, $products: [ProductInput]) {
          createRoutine(name: $name, description: $description, products: $products) {
            success
            routine {
              id
              name
              description
              products {
                id
                name
                timeOfUse
              }
            }
          }
        }
      `;

			const variables = {
				name: this.routine.name,
				description: this.routine.description,
				products: this.routine.products,
			};

			const token = localStorage.getItem('token');

			try {
				const response = await axios.post(
					'http://localhost:5001/graphql/',
					{
						query: mutation,
						variables,
					},
					{
						headers: {
							'Content-Type': 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);

				window.alert('Routine created successfully!');
				this.$emit('update:closeOverlay', true);
			} catch (error) {
				console.error('Error creating routine:', error);
			}
		},
		closeOverlay() {
			this.$emit('update:closeOverlay', true);
		},
	},
};
</script>

<style scoped>
.top {
	width: 100%;
	height: 10%;
	display: flex;
	flex-direction: row;
}

.top :is(h2) {
	width: 80%;
	height: 100%;
	margin-left: 10%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.top .closeBtn {
	width: 10%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.closeBtn :is(p) {
	margin: 0;
	font-size: 30px;
	color: black;
	transform: rotate(45deg);
	cursor: pointer;
}
.prodItem {
	margin: 1% 5%;
	width: 90%;
	padding: 0;
	background-color: white;
}

.prodItem :is(input) {
	width: 29%;
	padding: 5px 0;
	color: black;
	text-align: center;
}

.prodItem :is(input):first-child {
	border-radius: 8px 0 0 8px;
	border: 1px solid fuchsia;
	border-right: none;
}

.lastChild {
	border: 1px solid fuchsia;
	border-right: none;
}

.removeBtn {
	width: 13%;
	border: 1px solid fuchsia;
	background-color: fuchsia;
	padding: 5px 0;
	border-radius: 0 8px 8px 0;
	color: white;
	font-weight: 600;
}
.prodItem :is(select) {
	width: 29%;
	padding: 4.2px 0;
	border: 1px solid fuchsia;
	border-right: none;
	text-align: center;
	background-color: white;
	color: black;
	cursor: pointer;
}

.prodItem :is(select).lastChild {
	border: 1px solid fuchsia;
	border-right: none;
}

.addProd {
	margin-right: 5px;
	width: 100px;
	height: 25px;
	border-radius: 8px;
	border: none;
	background-color: pink;
	font-weight: 600;
}
.subForm {
	width: 100px;
	height: 25px;
	border-radius: 8px;
	border: none;
	background-color: purple;
	color: white;
	font-weight: 600;
	margin-left: 5px;
}
.pair {
	display: flex;
	flex-direction: row;
	width: 50%;
	height: 50px;
	margin: 0 25%;
	align-items: center;
}

.pair :is(label) {
    text-align: left;
    width: 40%;
    font-family: Arial, sans-serif;  /* Add this line */
    font-weight: 500;  /* Add this line for consistent weight */
}

.pair :is(input),
.pair :is(textarea) {
    width: 60%;
    height: 25px;
    border-radius: 8px;
    border: 1px solid fuchsia;
    font-family: Arial, sans-serif;  /* Add this line */
}
form div {
	margin-bottom: 10px;
}
</style>
