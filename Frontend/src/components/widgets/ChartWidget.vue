<template>
<div>
    <div class="p-4 border-b">
    <!-- <div class="grid grid-cols-2 gap-4 mb-4">
        <div>
        <label class="block text-sm font-medium mb-1">X-Axis Column</label>
        <select 
            :value="widget.config.xColumn" 
            class="w-full p-2 border rounded"
            @change="updateXColumn($event)"
        >
            <option 
            v-for="(header, index) in rawData.headers" 
            :key="index" 
            :value="index"
            >
            {{ header }}
            </option>
        </select>
        </div>
        <div>
        <label class="block text-sm font-medium mb-1">Y-Axis Columns</label>
        <select 
            :value="widget.config.yColumns" 
            class="w-full p-2 border rounded" 
            multiple
            @change="updateYColumns($event)"
        >
            <option 
            v-for="(header, index) in rawData.headers" 
            :key="index" 
            :value="index"
            :disabled="!isNumericColumn(index)"
            >
            {{ header }} {{ !isNumericColumn(index) ? '(non-numeric)' : '' }}
            </option>
        </select>
        </div>
    </div> -->
    </div>
    <div class="chart-container" ref="chartContainer">
    <canvas ref="chartCanvas"></canvas>
    </div>
</div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
name: 'ChartWidget',

props: {
    widget: {
    type: Object,
    required: true
    },
    rawData: {
    type: Object,
    required: true
    }
},

data() {
    return {
    chartInstance: null,
    resizeObserver: null
    };
},

created() {
    // Initialize config if not present
    if (!this.widget.config.xColumn) {
    this.initializeConfig();
    }
},

mounted() {
    this.initializeChart();
    this.setupResizeObserver();
},

beforeUnmount() {
    this.cleanup();
},

watch: {
    'widget.config': {
    deep: true,
    handler(newConfig) {
        if (this.chartInstance) {
        this.updateChart();
        }
    }
    },
    rawData: {
    deep: true,
    handler() {
        this.initializeConfig();
        this.updateChart();
    }
    }
},

methods: {
    initializeConfig() {
    // Find first numeric column for Y-axis
    const firstNumericColumn = this.rawData.headers.findIndex((_, index) => 
        this.isNumericColumn(index)
    );

    const config = {
        ...this.widget.config,
        xColumn: 0,
        yColumns: firstNumericColumn !== -1 ? [firstNumericColumn] : []
    };

    this.$emit('update:widget', {
        ...this.widget,
        config
    });
    },

    updateXColumn(event) {
    const xColumn = parseInt(event.target.value);
    this.$emit('update:widget', {
        ...this.widget,
        config: {
        ...this.widget.config,
        xColumn
        }
    });
    },

    updateYColumns(event) {
    const selectedOptions = Array.from(event.target.selectedOptions);
    const yColumns = selectedOptions.map(option => parseInt(option.value));
    this.$emit('update:widget', {
        ...this.widget,
        config: {
        ...this.widget.config,
        yColumns
        }
    });
    },

    isNumericColumn(columnIndex) {
    return this.rawData.rows.some(row => 
        !isNaN(parseFloat(row[columnIndex])) && row[columnIndex] !== ''
    );
    },

    initializeChart() {
    if (!this.rawData?.rows?.length) return;

    const ctx = this.$refs.chartCanvas.getContext('2d');
    const { labels, datasets } = this.prepareChartData();

    if (this.chartInstance) {
        this.chartInstance.destroy();
    }

    this.chartInstance = new Chart(ctx, {
        type: this.widget.config.chartType || 'bar',
        data: {
        labels,
        datasets
        },
        options: this.getChartOptions()
    });
    },

    prepareChartData() {
    const xColumn = this.widget.config.xColumn || 0;
    const yColumns = this.widget.config.yColumns || [];
    
    const labels = this.rawData.rows.map(row => row[xColumn]);
    
    const datasets = yColumns.map((columnIndex, datasetIndex) => ({
        label: this.rawData.headers[columnIndex],
        data: this.rawData.rows.map(row => parseFloat(row[columnIndex]) || 0),
        backgroundColor: this.getColor(datasetIndex),
        borderColor: this.getColor(datasetIndex),
        borderWidth: 1,
        fill: this.widget.config.chartType === 'line' ? false : true
    }));

    return { labels, datasets };
    },

    getChartOptions() {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
        legend: {
            position: 'bottom'
        },
        tooltip: {
            mode: 'index',
            intersect: false
        }
        },
        scales: {
        y: {
            beginAtZero: true
        }
        },
        animation: {
        duration: 500
        }
    };
    },

    getColor(index) {
    const colors = [
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 99, 132, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(153, 102, 255, 0.8)',
        'rgba(255, 159, 64, 0.8)'
    ];
    return colors[index % colors.length];
    },

    updateChart() {
    this.initializeChart();
    },

    setupResizeObserver() {
    this.resizeObserver = new ResizeObserver(() => {
        if (this.chartInstance) {
        this.chartInstance.resize();
        }
    });
    this.resizeObserver.observe(this.$refs.chartContainer);
    },

    cleanup() {
    if (this.chartInstance) {
        this.chartInstance.destroy();
    }
    if (this.resizeObserver) {
        this.resizeObserver.disconnect();
    }
    }
}
};
</script>

<style scoped>
.chart-container {
position: relative;
height: 300px;
width: 100%;
padding: 1rem;
}
</style>