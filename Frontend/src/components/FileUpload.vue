<template>
  <div class="space-y-6">
    <!-- File Upload Section -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="flex items-center justify-center w-full">
        <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
          <div class="flex flex-col items-center justify-center pt-5 pb-6">
            <svg class="w-8 h-8 mb-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
            </svg>
            <p class="mb-2 text-sm text-gray-500">
              <span class="font-semibold">Click to upload</span> or drag and drop
            </p>
            <p class="text-xs text-gray-500">CSV, Excel, or JSON files</p>
          </div>
          <input type="file" class="hidden" @change="handleFileUpload" accept=".csv,.xlsx,.xls,.json" />
        </label>
      </div>

      <!-- File Selection Info -->
      <div v-if="file" class="mt-4 flex items-center gap-2 text-sm text-gray-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <span>Selected file: <span class="font-medium">{{ file.name }}</span></span>
      </div>
    </div>

    <!-- Data Preview -->
    <div v-if="fileContent" class="bg-white rounded-lg shadow-md p-6 mb-6 overflow-x-auto">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Data Preview</h3>
      <div class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <thead>
            <tr class="bg-gray-100">
              <th v-for="header in headers" :key="header" class="px-4 py-2 text-left text-sm font-medium text-gray-900">
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in displayedRows" :key="index" class="border-t border-gray-200">
              <td v-for="(cell, cellIndex) in row" :key="cellIndex" class="px-4 py-2 text-sm text-gray-600">
                {{ cell }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Preview Info -->
      <div class="mt-4 text-sm text-gray-500">
        Showing {{ displayedRows.length }} of {{ rows.length }} rows
      </div>
    </div>

    <!-- Prompt Input Section -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Process Your Data</h3>
      <div class="space-y-4">
        <div class="space-y-2">
          <label class="text-sm text-gray-600">Enter your request:</label>
          <textarea 
            v-model="userPrompt" 
            placeholder="Describe what you want to do with your data (e.g., 'Show me a bar chart of sales by region' or 'Calculate the average revenue by product category')"
            class="textarea textarea-bordered w-full h-32 text-sm"
          ></textarea>
          <p class="text-xs text-gray-500">
            You can ask for data transformations or visualizations - the AI will automatically determine what you need.
          </p>
        </div>
        
        <button 
          @click="processData" 
          class="btn btn-primary w-full"
          :disabled="!file || !userPrompt || loading"
        >
          <span class="flex items-center gap-2">
            <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
            <div v-else class="loading loading-spinner loading-sm"></div>
            {{ loading ? 'Processing...' : 'Process Data' }}
          </span>
        </button>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <div class="loading loading-spinner loading-lg"></div>
        <p class="mt-4 text-gray-700">Processing your request...</p>
      </div>
    </div>
  </div>
</template>

<script>
import * as XLSX from 'xlsx';

export default {
  data() {
    return {
      file: null,
      fileContent: '',
      headers: [],
      rows: [],
      userPrompt: '',
      loading: false
    };
  },
  computed: {
    displayedRows() {
      return this.rows.slice(0, 5);
    }
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        const fileType = this.file.name.split('.').pop().toLowerCase();
        this.fileContent = reader.result;

        if (fileType === 'csv') {
          this.parseCSV(this.fileContent);
        } else if (['xls', 'xlsx'].includes(fileType)) {
          this.parseExcel(reader.result);
        } else if (fileType === 'json') {
          this.parseJSON(this.fileContent);
        } else {
          alert('Unsupported file type.');
        }
      };

      if (['xls', 'xlsx'].includes(this.file.name.split('.').pop().toLowerCase())) {
        reader.readAsArrayBuffer(this.file);
      } else {
        reader.readAsText(this.file);
      }
    },

    parseCSV(content) {
      const lines = content.split('\n');
      this.headers = lines[0].split(',');
      this.rows = lines.slice(1).map(line => line.split(','));
    },

    parseExcel(content) {
      const workbook = XLSX.read(content, { type: 'array' });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

      this.headers = jsonData[0];
      this.rows = jsonData.slice(1);
    },

    parseJSON(content) {
      const jsonData = JSON.parse(content);

      if (Array.isArray(jsonData)) {
        this.headers = Object.keys(jsonData[0]);
        this.rows = jsonData.map(obj => Object.values(obj));
      } else {
        alert('JSON file must contain an array of objects.');
      }
    },

    async processData() {
      if (!this.file || !this.userPrompt) {
        this.showError('Please upload a file and enter a prompt.');
        return;
      }

      this.triggerNewPrompt();

      this.loading = true;
      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('prompt', this.userPrompt);

      try {
        const response = await fetch('http://localhost:8000/process', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        this.$emit('data-processed', result);

        this.showSuccess('Data processed successfully!');
      } catch (error) {
        console.error('Error processing data:', error);
        this.showError('An error occurred while processing your request. Please try again.');
      } finally {
        this.loading = false;
      }
    },
    triggerNewPrompt() {
      this.$emit('new-prompt'); // Notify App.vue to reset the dashboard
    },
    showError(message) {
      alert(message);
    },

    showSuccess(message) {
      alert(message);
    }
  }
};
</script>
