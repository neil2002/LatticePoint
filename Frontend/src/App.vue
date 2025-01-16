<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">AI Data Analysis and Visualization</h1>
    <div class="space-y-6">
      <FileUpload 
        @data-processed="handleProcessedData" 
        @new-prompt="resetProcessedData" 
      />
      <Dashboard 
        v-if="processedData"
        :processedData="processedData"
      />
    </div>
  </div>
</template>

<script>
import FileUpload from './components/FileUpload.vue';
import Dashboard from './components/Dashboard.vue';

export default {
  components: {
    FileUpload,
    Dashboard,
  },
  data() {
    return {
      processedData: null,
    };
  },
  methods: {
    handleProcessedData(data) {
      this.processedData = data;
      console.log(this.processedData);
    },
    resetProcessedData() {
      this.processedData = null; // Reset the dashboard data
    },
  },
};
</script>
