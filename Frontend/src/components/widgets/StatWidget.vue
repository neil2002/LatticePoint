<template>
<div>
    <h3 class="text-lg font-semibold mb-2">Statistical Insight Widget</h3>
    <div v-if="processedData && processedData.data && processedData.data[0]">
    <div v-for="(value, key) in processedData.data[0]" :key="key" class="mb-1">
        <strong>{{ key }}:</strong> {{ value }}
    </div>
    </div>
    <div v-else>
    No statistical data available.
    </div>
</div>
</template>

<script>
export default {
name: 'StatWidget',
props: {
    widget: Object,
    processedData: Object,
},
};
</script>

<style scoped>
/* Additional styling if needed */
</style>
