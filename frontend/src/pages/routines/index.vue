<template>
  <div class="routine-container" v-if="!routineViewOpen">
    <h1>My Routine</h1>
    <p>
      Your routine is based on your analysis. You can edit it to add new
      products.
    </p>

    <ul>
      <li
        v-for="routine in routines"
        :key="routine.id"
        class="routine-item"
      >
        <strong>{{ routine.name }}</strong>
        <span class="actions">
          <a @click.prevent="toggleViewRoutine(routine)">View</a>
          <a @click.prevent="editRoutine(routine)">Edit</a>
          <a @click.prevent="deleteRoutine(routine.id)">Delete</a>
        </span>
      </li>
    </ul>

    <button class="add-btn" @click="addNewRoutine">Add New Routine</button>
    <div v-if="addRoutine" class="addRoutineOverlay">
      <routineForm @update:closeOverlay="closeNewRoutine" />
    </div>
  </div>

  <div class="routine-container view" v-if="routineViewOpen">
    <div class="top">
      <div class="title">{{ focusedRoutine.name }}</div>
      <div class="close">
        <p @click="toggleViewRoutine('remove')">+</p>
      </div>
    </div>

    <div class="description">
      <div class="descTitle">Description</div>
      <div class="descText">{{ focusedRoutine.description }}</div>
    </div>

    <div class="products">
      <div class="prodTitle">Products</div>
      <div
        class="prodItem"
        v-for="(item, idx) in focusedRoutine.products"
        :key="idx"
      >
        <div>{{ item.name }}</div>
        <div>{{ item.category }}</div>
        <div>{{ item.time_of_use }}</div>
        <div class="removeProd" @click="removeFromRoutine(item.id)">
          remove
        </div>
      </div>
    </div>

    <div class="addProductForm" v-if="showProductForm">
      <h3>Add New Product</h3>
      <div class="formGroup">
        <label>Name</label>
        <input
          v-model="newProduct.name"
          placeholder="e.g. Niacinamide Serum"
        />
      </div>
      <div class="formGroup">
        <label>Category</label>
        <select v-model="newProduct.category" required>
          <option disabled value="">Select Category</option>
          <option
            v-for="category in categories"
            :key="category"
            :value="category"
          >
            {{ category }}
          </option>
        </select>
      </div>
      <div class="formGroup">
        <label>Time of Use</label>
        <select v-model="newProduct.time_of_use" required>
          <option disabled value="">Select time</option>
          <option>AM</option>
          <option>PM</option>
          <option>AM & PM</option>
        </select>
      </div>
      <div class="formActions">
        <button @click="submitNewProduct">Submit</button>
        <button @click="showProductForm = false">Cancel</button>
      </div>
    </div>

    <div class="buttonDiv">
      <div class="addBtn" @click="showProductForm = true">Add Product</div>
      <div
        class="deleteBtn"
        @click="deleteRoutine(focusedRoutine.id)"
      >Delete Routine</div>
    </div>
  </div>

  <div v-if="showEditForm" class="editRoutineOverlay">
    <div class="edit-form">
      <div class="edit-form-header">
        <h3>Edit Routine</h3>
        <span class="close-edit" @click="closeEditForm">×</span>
      </div>
      <div class="formGroup">
        <label>Name</label>
        <input
          v-model="editingRoutine.name"
          placeholder="Routine name"
        />
      </div>
      <div class="formGroup">
        <label>Description</label>
        <textarea
          v-model="editingRoutine.description"
          placeholder="Routine description"
        ></textarea>
      </div>
      <div class="formActions">
        <button class="save-btn" @click="saveEditedRoutine">
          Save Changes
        </button>
        <button class="cancel-btn" @click="closeEditForm">
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import routineForm from '../../components/routine/routineForm.vue'
import requests from '../../utils/requests'

const GQL_URL = 'https://skinvision-backend-2pho.onrender.com/graphql/'

export default {
  components: { routineForm },
  data() {
    return {
      routines: [],
      addRoutine: false,
      routineViewOpen: false,
      focusedRoutine: null,
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
        'Spot Treatments'
      ],
      showProductForm: false,
      newProduct: { name: '', category: '', time_of_use: '' },
      showEditForm: false,
      editingRoutine: { id: null, name: '', description: '' },
    }
  },
  mounted() {
    this.fetchRoutines()
  },
  methods: {
    // 1) Create Routine (in your routineForm component)
    // — leave as is.

    // 2) Add Product → use variables:
    async submitNewProduct() {
      if (!this.newProduct.name || !this.newProduct.category || !this.newProduct.time_of_use) {
        alert('Please fill in all fields');
        return;
      }

      const mutation = `
        mutation AddProductToRoutine(
          $routineId: Int!,
          $name: String!,
          $category: String!,
          $timeOfUse: String!
        ) {
          addProductToRoutine(
            routineId: $routineId,
            name: $name,
            category: $category,
            timeOfUse: $timeOfUse
          ) {
            success
            routine {
              id
              name
              products {
                id
                name
                category
                timeOfUse
              }
            }
          }
        }
      `;

      try {
        const response = await axios.post(
          GQL_URL,
          {
            query: mutation,
            variables: {
              routineId: Number(this.focusedRoutine.id),
              name: this.newProduct.name.trim(),
              category: this.newProduct.category,
              timeOfUse: this.newProduct.time_of_use // Map time_of_use to timeOfUse
            }
          },
          { headers: this.authHeaders() }
        );

        console.log('Response:', response.data);

        if (response.data.errors) {
          throw new Error(response.data.errors[0].message);
        }

        if (response.data.data.addProductToRoutine.success) {
          this.focusedRoutine.products = response.data.data.addProductToRoutine.routine.products;
          this.newProduct = { name: '', category: '', time_of_use: '' };
          this.showProductForm = false;
        }
      } catch (error) {
        console.error('Error adding product:', error);
        alert('Failed to add product: ' + (error.response?.data?.errors?.[0]?.message || error.message));
      }
    },

    // 3) Update Routine → variables-based
    async saveEditedRoutine() {
      if (!this.editingRoutine.name.trim()) {
        return alert('Name is required.')
      }

      const mutation = `
        mutation EditRoutine($id: ID!, $name: String!, $description: String) {
          editRoutine(id: $id, name: $name, description: $description) {
            success
            routine {
              id
              name
              description
            }
          }
        }
      `

      try {
        console.log('Sending mutation with variables:', {
          id: this.editingRoutine.id,
          name: this.editingRoutine.name,
          description: this.editingRoutine.description
        });

        const resp = await axios.post(
          GQL_URL,
          {
            query: mutation,
            variables: {
              id: String(this.editingRoutine.id),
              name: this.editingRoutine.name.trim(),
              description: this.editingRoutine.description?.trim() || ''
            }
          },
          {
            headers: this.authHeaders()
          }
        )

        console.log('Response:', resp.data);

        if (resp.data.errors) {
          throw new Error(resp.data.errors[0].message)
        }

        if (resp.data.data.editRoutine.success) {
          await this.fetchRoutines()
          this.closeEditForm()
          alert('Routine updated successfully!')
        }
      } catch (err) {
        console.error('Update error:', err.response?.data || err)
        alert('Failed to update: ' + (err.response?.data?.errors?.[0]?.message || err.message))
      }
    },

    // 4) Delete Routine (also variables-based)
    async deleteRoutine(id) {
      if (!confirm('Delete this routine?')) return
      const mutation = `
        mutation DeleteRoutine($id: Int!) {
          deleteRoutine(id: $id) { success }
        }
      `
      try {
        const resp = await axios.post(GQL_URL,
          { query: mutation, variables: { id: Number(id) } }, // ✅ send as number
          { headers: this.authHeaders() }
        )
        if (resp.data.errors) {
          console.error('GraphQL error:', resp.data.errors[0]);
          alert(resp.data.errors[0].message); // This will show the backend error
          throw resp.data.errors[0];
        }
        if (resp.data.data.deleteRoutine.success) {
          this.routineViewOpen = false
          this.fetchRoutines()
        }
      } catch (err) {
        console.error(err)
        alert('Could not delete routine.')
      }
    },

    // 5) Fetch
    async fetchRoutines() {
      const query = `
        query { myRoutines {
          id name description
          products { id name category timeOfUse }
        }}`
      try {
        const resp = await axios.post(GQL_URL,
          { query },
          { headers: this.authHeaders() }
        )
        this.routines = resp.data.data.myRoutines
      } catch (err) {
        console.error(err)
      }
    },

    // Helpers & UI toggles
    authHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}`, 'Content-Type': 'application/json' }
    },
    toggleViewRoutine(r) { this.routineViewOpen = !this.routineViewOpen; this.focusedRoutine = r==='remove'?null:r },
    editRoutine(r) { this.editingRoutine = { ...r }; this.showEditForm=true },
    closeEditForm() { this.showEditForm=false; this.editingRoutine={id:null,name:'',description:''} },
    addNewRoutine() { this.addRoutine=true },
    closeNewRoutine() { this.addRoutine=false; this.fetchRoutines() },
    async removeFromRoutine(productId) {
      if (!confirm('Remove this product?')) return;

      const mutation = `
        mutation RemoveProduct($routineId: Int!, $productId: Int!) {
          removeProductFromRoutine(routineId: $routineId, productId: $productId) {
            success
            routine {
              id
              products {
                id
                name
                category
                timeOfUse
              }
            }
          }
        }
      `;

      try {
        const response = await axios.post(
          GQL_URL,
          {
            query: mutation,
            variables: {
              routineId: Number(this.focusedRoutine.id),
              productId: Number(productId)
            }
          },
          { headers: this.authHeaders() }
        );

        if (response.data.errors) {
          throw new Error(response.data.errors[0].message);
        }

        if (response.data.data.removeProductFromRoutine.success) {
          // Update the local products list
          this.focusedRoutine.products = response.data.data.removeProductFromRoutine.routine.products;
        }
      } catch (error) {
        console.error('Error removing product:', error);
        alert('Failed to remove product: ' + (error.response?.data?.errors?.[0]?.message || error.message));
      }
    },
  }
}
</script>


<style>
.addProductForm {
	position: relative;
	width: 80%;
	margin: 20px auto;
	margin-top: -55% !important;
	padding: 15px;
	background-color: #f9f9f9;
	border: 1px solid #ccc;
	border-radius: 10px;
	box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
	z-index: 900;
}
.formGroup {
	margin-bottom: 10px;
	display: flex;
	flex-direction: column;
}
.formGroup label {
	font-weight: 600;
}
.formGroup input,
.formGroup select {
	padding: 8px;
	border-radius: 5px;
	border: 1px solid #ccc;
}
.formActions {
	display: flex;
	justify-content: space-between;
	margin-top: 10px;
}
.buttonDiv {
	width: 100%;
	height: 10%;
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
}

.addBtn {
	background-color: purple;
	color: white;
	font-weight: 600;
	padding: 5px 20px;
	border-radius: 15px;
	cursor: pointer;
	margin-right: 5px;
}

.deleteBtn {
	background-color: red;
	color: white;
	font-weight: 600;
	padding: 5px 20px;
	border-radius: 15px;
	cursor: pointer;
	margin-left: 5px;
}
.removeProd {
	background-color: purple;
	color: white;
	font-weight: 600;
	padding: 5px 20px;
	border-radius: 15px;
	cursor: pointer;
}
.prodItem {
	width: 98%;
	height: 45px;
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	background-color: rgb(128, 0, 128, 0.1);
	border-radius: 8px;
	padding: 0 1%;
}
.prodTitle {
	width: 100%;
	height: 10%;
	display: flex;
	align-items: center;
	font-size: 18px;
	font-weight: 600;
	color: black;
	text-align: left;
	 margin-bottom: 12px; 
}
.products {
    width: 90%;  /* Increased from 85% to 90% */
    padding: 1%;
    height: 45%;
    margin: 1% 5%;  /* Decreased from 7% to 5% to allow more width */
    background-color: rgb(255, 192, 203, 0.6);
    border-radius: 10px;
    overflow-y: auto;
}

.description {
    width: 90%;  /* Increased from 85% to 90% */
    margin: 0 5%;  /* Decreased from 7% to 5% to allow more width */
    padding: 1%;
    height: 20%;
    background-color: rgb(255, 192, 203, 0.5);
    border-radius: 8px;
}
.descTitle {
	font-size: 18px;
	font-weight: 600;
	color: black;
	text-align: left;
	 margin-bottom: 12px; 
}

.descText {
	font-size: 14px;
	color: black;
	text-align: left;
}

.top {
	height: 15%;
	width: 100%;
	display: flex;
	flex-direction: row;
	align-items: center;
}

.top .title {
	width: 80%;
	margin-left: 10%;
	font-size: 24px;
	color: black;
	font-weight: 600;
}

.top .close {
	width: 10%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.top .close :is(p) {
	margin: 0;
	width: 30px;
	height: 30px;
	font-size: 40px;
	font-weight: 500;
	transform: rotate(45deg);
	border-radius: 50%;
	border: 2px solid black;
	display: flex;
	align-items: center;
	justify-content: center;
	color: black;
	cursor: pointer;
}
.view {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 0 6.2px rgb(0, 0, 0, 0.2);
    padding-left: 160px;
    padding-right: 80px;
    max-width: 780px;
    margin: 50px auto;
    margin-left: 260px;  /* Add this line to move card to the right */
    /* OR use transform */
    transform: translateX(50px);  /* Alternative approach */
}
li strong {
	width: 60%;
	text-align: left;
}
li {
	height: 45px;
	width: 100%;
	display: flex;
	flex-direction: row;
	align-items: center;
}
.addRoutineOverlay {
	position: absolute;
	background-color: white;
	border-radius: 10px;
	box-shadow: 0 0 6.2px rgb(0, 0, 0, 0.2);
	width: 60%;
	height: 80%;
	top: 100px;
	left: 20%;
}


.editRoutineOverlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.edit-form {
    background: white;
    padding: 24px;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.edit-form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.close-edit {
    font-size: 24px;
    cursor: pointer;
    color: #666;
}

.edit-form textarea {
    min-height: 100px;
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
    width: 100%;
    font-family: inherit;
    resize: vertical;
}

.save-btn {
    background: #6c5ce7;
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}

.cancel-btn {
    background: #666;
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 6px;
    cursor: pointer;
    margin-left: 10px;
}
.routine-container {
	grid-row: 30/80;
	grid-column: 10/80;
	margin: 0 20%;
	font-family: Arial, sans-serif;
	padding-left: 80px; 
}
.routine-container h1 {
  font-size: 28px;
  font-weight: bold;
  display: inline-block;
  border-bottom: 3px solid #6c5ce7;  /* lilac accent */
  padding-bottom: 4px;
  margin-bottom: 12px;
}
h1 {
	font-size: 24px;
	font-weight: bold;
}
p {
	color: #666;
}
ul { 
  list-style: none; 
  padding: 0; 
  margin: 24px 0; 
}
.routine-item {
  background: rgb(174, 197, 214);
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.routine-item strong {
  font-size: 16px;
  text-align: left;
}
.actions a {
  color: #e2660d;
  margin: 0 6px;
  font-weight: 600;
  text-decoration: none;
}
.actions a:hover {
  text-decoration: underline;
}

.category,
.time-of-use {
	font-size: 14px;
	color: #9b59b6;
}

.add-btn {
  background-color: #6c5ce7;
  color: white;
  padding: 10px 24px;
  border: none;
  border-radius: 24px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color .2s;
}
.add-btn:hover {
  background-color: #5941a9;
}

</style>
