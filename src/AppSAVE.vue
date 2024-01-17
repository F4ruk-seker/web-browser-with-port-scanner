<script setup>
import axios from "axios";
import {ref} from "vue";

const customer_data = ref(null)

async function fetch_all_data() {
  const response = await axios.get('')
  customer_data.value = response.data
  console.log(customer_data.value)
}

async function get_detail(obj){

}

fetch_all_data()
</script>

<template>
<section>
  <span v-if="!customer_data">LOADING</span>
  <button v-else @click="get_detail" v-for="customer in customer_data">{{ customer }}</button>
</section>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
