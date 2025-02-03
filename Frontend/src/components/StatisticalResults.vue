<!-- StatisticalResults.vue -->
<template>
<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
    <h2 class="card-title">Statistical Analysis Results</h2>
    
    <!-- Correlation Matrix -->
    <div v-if="isCorrelation" class="space-y-4">
        <h3 class="text-lg font-medium">Correlation Matrix</h3>
        <div class="overflow-x-auto">
        <table class="table w-full">
            <thead>
            <tr>
                <th v-for="(col, index) in correlationColumns" 
                    :key="index" 
                    class="px-4 py-2 text-left">
                {{ col }}
                </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(row, rowIndex) in correlationMatrix" :key="rowIndex">
                <td v-for="(value, colIndex) in row" 
                    :key="colIndex" 
                    class="px-4 py-2"
                    :class="getCellColor(value)">
                {{ formatValue(value) }}
                </td>
            </tr>
            </tbody>
        </table>
        </div>
    </div>

    <!-- T-Test Results -->
    <div v-if="isTTest" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-50 p-4 rounded">
            <p class="text-sm font-medium">T-Statistic</p>
            <p class="text-2xl">{{ formatValue(statisticalData.t_statistic) }}</p>
        </div>
        <div class="bg-gray-50 p-4 rounded">
            <p class="text-sm font-medium">P-Value</p>
            <p class="text-2xl">{{ formatValue(statisticalData.p_value) }}</p>
        </div>
        </div>
        <p class="text-sm text-gray-600" v-if="statisticalData.p_value !== undefined">
        {{ interpretPValue(statisticalData.p_value) }}
        </p>
    </div>

    <!-- Chi-Square Results -->
    <div v-if="isChiSquare" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-50 p-4 rounded">
            <p class="text-sm font-medium">Chi-Square Statistic</p>
            <p class="text-2xl">{{ formatValue(statisticalData.chi_square) }}</p>
        </div>
        <div class="bg-gray-50 p-4 rounded">
            <p class="text-sm font-medium">P-Value</p>
            <p class="text-2xl">{{ formatValue(statisticalData.p_value) }}</p>
        </div>
        </div>
        <p class="text-sm">Degrees of Freedom: {{ statisticalData.dof }}</p>
        <p class="text-sm text-gray-600" v-if="statisticalData.p_value !== undefined">
        {{ interpretPValue(statisticalData.p_value) }}
        </p>
    </div>
    </div>
</div>
</template>

<script>
export default {
name: 'StatisticalResults',

props: {
    statisticalData: {
    type: Object,
    required: true
    },
    statisticalType: {
    type: String,
    required: true
    }
},

computed: {
    isCorrelation() {
    return this.statisticalType === 'correlation';
    },
    
    isTTest() {
    return this.statisticalType === 'ttest';
    },
    
    isChiSquare() {
    return this.statisticalType === 'chi_square';
    },
    
    correlationMatrix() {
    if (!this.isCorrelation || !this.statisticalData.correlation_matrix) return [];
    return this.statisticalData.correlation_matrix;
    },
    
    correlationColumns() {
    if (!this.isCorrelation || !this.statisticalData.correlation_matrix) return [];
    return Object.keys(this.statisticalData.correlation_matrix[0]);
    }
},

methods: {
    formatValue(value) {
    if (typeof value !== 'number') return value;
    return value.toFixed(4);
    },
    
    getCellColor(value) {
    if (typeof value !== 'number') return '';
    if (value === 1) return 'bg-blue-100';
    if (value > 0.7) return 'bg-blue-50';
    if (value < -0.7) return 'bg-red-50';
    return '';
    },
    
    interpretPValue(pValue) {
    const alpha = 0.05;
    if (pValue < alpha) {
        return `Statistically significant (p < ${alpha})`;
    }
    return `Not statistically significant (p > ${alpha})`;
    }
}
};
</script>

<style scoped>
.table td, .table th {
@apply border px-4 py-2 text-sm;
}

.table th {
@apply bg-gray-50;
}
</style>