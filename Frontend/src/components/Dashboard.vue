<template>
  <div class="card bg-base-100 shadow-xl">
    <div v-if="isDataValid" class="card-body">
      <h2 class="card-title">{{ chartTitle }}</h2>
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
    <!-- Statistical Results -->
    <StatisticalResults
      v-else-if="isStatistical"
      :statisticalData="processedData.data[0]"
      :statisticalType="processedData.statistical_type"
    />
    <div v-else>
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-bold mb-4">Data Table</h3>
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr>
                <th v-for="column in dataColumns" :key="column" class="px-4 py-2 text-left">
                  {{ column }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in transformedData" :key="index">
                <td v-for="column in dataColumns" :key="column" class="px-4 py-2">
                  {{ row[column] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import { nextTick } from 'vue';
import StatisticalResults from './StatisticalResults.vue';

export default {
  props: {
    processedData: {
      type: Object,
      required: true,
      validator(value) {
        return value?.visualization?.data && value?.visualization?.type;
      }
    }
  },

  data() {
    return {
      chartInstance: null
    };
  },

  computed: {
    isDataValid() {
      return this.processedData?.visualization?.data?.datasets?.[0]?.data?.length > 0;
    },

    isStatistical() {
      return this.processedData?.type === 'statistical';
    }, 
    
    chartTitle() {
      return this.processedData?.visualization?.options?.plugins?.title?.text || 'Sales Data';
    },

    transformedData() {
      return this.processedData?.data || []
    },
    dataColumns() {
      return this.transformedData.length > 0 ? Object.keys(this.transformedData[0]) : []
    },

  },

  watch: {
    'processedData.visualization': {
      handler(newVal) {
        nextTick(() => {
          this.updateChart();
        });
      },
      deep: true
    }
  },

  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
      }).format(value);
    },

    async updateChart() {
      if (this.chartInstance) {
        this.chartInstance.destroy();
        this.chartInstance = null;
      }

      if (!this.isDataValid) return;

      try {
        const ctx = this.$refs.chartCanvas?.getContext('2d');
        if (!ctx) return;

        // Deep clone the configuration
        const chartConfig = JSON.parse(JSON.stringify(this.processedData.visualization));
        
        // Enhance the configuration with additional options
        chartConfig.options = {
          ...chartConfig.options,
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            ...chartConfig.options.plugins,
            tooltip: {
              callbacks: {
                label: (context) => {
                  return `Revenue: ${this.formatCurrency(context.raw)}`;
                }
              }
            }
          },
          scales: {
            ...chartConfig.options.scales,
            y: {
              ...chartConfig.options.scales.y,
              ticks: {
                callback: (value) => this.formatCurrency(value)
              }
            }
          }
        };

        this.chartInstance = new Chart(ctx, chartConfig);
      } catch (error) {
        console.error('Error creating chart:', error);
        this.$emit('chart-error', error);
      }
    }
  },

  mounted() {
    this.updateChart();
  },

  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
      this.chartInstance = null;
    }
  }
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>