<template>
<div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Dashboard Builder</h1>
    
    <!-- Main Layout -->
    <div class="flex gap-4">
    <!-- Widget Selection Sidebar -->
    <div class="w-1/4 bg-white rounded-lg shadow p-4">
        <h2 class="text-xl font-semibold mb-4">Add Widgets</h2>
        <div class="space-y-2">
        <button 
            v-for="widget in availableWidgets" 
            :key="widget.type"
            class="flex items-center w-full p-2 rounded hover:bg-gray-100 transition-colors"
            @click="addWidget(widget.type)"
        >
            <component :is="widget.icon" class="w-5 h-5 mr-2" />
            {{ widget.label }}
        </button>
        </div>

        <!-- Widget Configuration -->
        <div v-if="selectedWidget" class="mt-4 border-t pt-4">
        <h3 class="font-semibold mb-2">Widget Settings</h3>
        <div class="space-y-4">
            <!-- Basic Settings -->
            <div>
            <label class="block text-sm font-medium mb-1">Title</label>
            <input 
                v-model="selectedWidget.config.title"
                class="w-full p-2 border rounded"
                @change="updateWidget(selectedWidget)"
            />
            </div>

            <!-- Chart Specific Settings -->
            <template v-if="selectedWidget.type === 'chart'">
            <!-- Chart Type -->
            <div>
                <label class="block text-sm font-medium mb-1">Chart Type</label>
                <select 
                v-model="selectedWidget.config.chartType"
                class="w-full p-2 border rounded"
                @change="updateWidget(selectedWidget)"
                >
                <option value="bar">Bar Chart</option>
                <option value="line">Line Chart</option>
                <option value="pie">Pie Chart</option>
                <option value="scatter">Scatter Plot</option>
                <option value="radar">Radar Chart</option>
                </select>
            </div>

            <!-- X-Axis Configuration -->
            <div>
                <label class="block text-sm font-medium mb-1">X-Axis Column</label>
                <select 
                v-model="selectedWidget.config.xColumn"
                class="w-full p-2 border rounded"
                @change="updateWidget(selectedWidget)"
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

            <!-- Y-Axis Configuration -->
            <div>
                <label class="block text-sm font-medium mb-1">Y-Axis Columns</label>
                <select 
                v-model="selectedWidget.config.yColumns"
                class="w-full p-2 border rounded" 
                multiple
                size="5"
                @change="updateWidget(selectedWidget)"
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
                <p class="text-sm text-gray-500 mt-1">Hold Ctrl/Cmd to select multiple columns</p>
            </div>

            <!-- Chart Size Settings -->
            <div>
                <label class="block text-sm font-medium mb-1">Widget Size</label>
                <select 
                v-model="selectedWidget.config.size"
                class="w-full p-2 border rounded"
                @change="updateWidget(selectedWidget)"
                >
                <option value="1">Small</option>
                <option value="2">Medium</option>
                <option value="3">Large</option>
                <option value="4">Full Width</option>
                </select>
            </div>
            </template>
        </div>
        </div>
    </div>

    <!-- Dashboard Area -->
    <div class="w-3/4">
        <div v-if="!dashboardWidgets.length" 
        class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <p class="text-gray-500">Drag widgets here or use the sidebar to add them</p>
        </div>
        
        <div v-else class="grid grid-cols-4 gap-4">
        <div
            v-for="widget in dashboardWidgets"
            :key="widget.id"
            class="bg-white rounded-lg shadow relative transition-all duration-200"
            :class="[
            getWidgetSizeClass(widget),
            {'ring-2 ring-blue-500': selectedWidget?.id === widget.id}
            ]"
            @click="selectWidget(widget)"
        >
            <!-- Widget Header -->
            <div class="p-3 border-b flex justify-between items-center">
            <h3 class="font-semibold">{{ widget.config.title }}</h3>
            <div class="flex gap-2">
                <button 
                @click.stop="removeWidget(widget.id)" 
                class="p-1 text-red-500 hover:text-red-700 rounded"
                >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                </button>
            </div>
            </div>
            
            <!-- Widget Content -->
            <div class="p-4">
            <component 
                :is="getWidgetComponent(widget)" 
                :widget="widget" 
                :rawData="rawData" 
                @update:widget="updateWidget"
            />
            </div>
        </div>
        </div>
    </div>
    </div>
</div>
</template>

<script>
import { defineComponent } from 'vue';
import ChartWidget from './widgets/ChartWidget.vue';
import TableWidget from './widgets/TableWidget.vue';
import InsightWidget from './widgets/InsightWidget.vue';
import StatWidget from './widgets/StatWidget.vue';

export default defineComponent({
name: 'DashboardBuilder',

components: {
    ChartWidget,
    TableWidget,
    InsightWidget,
    StatWidget
},

data() {
    return {
    dashboardWidgets: [],
    selectedWidget: null,
    rawData: null,
    availableWidgets: [
        { type: 'chart', label: 'Chart Widget', icon: 'i-tabler-chart-bar' },
        { type: 'table', label: 'Data Table', icon: 'i-tabler-table' },
        { type: 'insight', label: 'Insight Card', icon: 'i-tabler-bulb' },
        { type: 'stat', label: 'Statistics', icon: 'i-tabler-calculator' }
    ]
    };
},

created() {
    this.loadDashboard();
},

methods: {
    isNumericColumn(columnIndex) {
    return this.rawData.rows.some(row => 
        !isNaN(parseFloat(row[columnIndex])) && row[columnIndex] !== ''
    );
    },

    loadDashboard() {
    // Load raw data
    const storedData = sessionStorage.getItem("State");
    if (storedData) {
        try {
        const parsedData = JSON.parse(storedData);
        if (parsedData && Array.isArray(parsedData.headers) && Array.isArray(parsedData.rows)) {
            this.rawData = parsedData;
        } else {
            throw new Error('Invalid data structure');
        }
        } catch (error) {
        console.error('Error loading data:', error);
        alert('Error loading dataset. Please try again.');
        this.$router.push({ name: 'DataProcessor' });
        }
    } else {
        alert('No data found. Please upload a dataset first.');
        this.$router.push({ name: 'DataProcessor' });
    }

    // Load saved dashboard layout
    const savedLayout = localStorage.getItem('dashboardLayout');
    if (savedLayout) {
        try {
        this.dashboardWidgets = JSON.parse(savedLayout);
        } catch (error) {
        console.error('Error loading dashboard layout:', error);
        }
    }
    },

    addWidget(type) {
    // Find first numeric column for Y-axis if it's a chart
    let yColumns = [];
    if (type === 'chart') {
        const firstNumericColumn = this.rawData.headers.findIndex((_, index) => 
        this.isNumericColumn(index)
        );
        if (firstNumericColumn !== -1) {
        yColumns = [firstNumericColumn];
        }
    }

    const widget = {
        id: `widget-${Date.now()}`,
        type,
        config: {
        title: `New ${type.charAt(0).toUpperCase() + type.slice(1)} Widget`,
        size: '2', // Default to medium size
        chartType: type === 'chart' ? 'bar' : null,
        xColumn: 0, // Default to first column
        yColumns: yColumns,
        }
    };
    this.dashboardWidgets.push(widget);
    this.saveDashboard();
    this.selectWidget(widget);
    },

    removeWidget(widgetId) {
    this.dashboardWidgets = this.dashboardWidgets.filter(w => w.id !== widgetId);
    if (this.selectedWidget?.id === widgetId) {
        this.selectedWidget = null;
    }
    this.saveDashboard();
    },

    selectWidget(widget) {
    this.selectedWidget = widget;
    },

    updateWidget(widget) {
    const index = this.dashboardWidgets.findIndex(w => w.id === widget.id);
    if (index !== -1) {
        this.dashboardWidgets[index] = { ...widget };
        this.saveDashboard();
    }
    },

    getWidgetComponent(widget) {
    const componentMap = {
        chart: 'ChartWidget',
        table: 'TableWidget',
        insight: 'InsightWidget',
        stat: 'StatWidget'
    };
    return componentMap[widget.type] || 'div';
    },

    getWidgetSizeClass(widget) {
    const sizeMap = {
        '1': 'col-span-1', // Small
        '2': 'col-span-2', // Medium
        '3': 'col-span-3', // Large
        '4': 'col-span-4'  // Full Width
    };
    return sizeMap[widget.config.size || '2'];
    },

    saveDashboard() {
    localStorage.setItem('dashboardLayout', JSON.stringify(this.dashboardWidgets));
    }
}
});
</script>