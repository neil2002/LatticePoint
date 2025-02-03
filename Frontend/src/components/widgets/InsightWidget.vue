<template>
<div>
    <h3 class="text-lg font-semibold mb-2">Insight Widget</h3>
    <div>
    <p><strong>Total Records:</strong> {{ rawData.rows.length }}</p>
    <p><strong>Columns:</strong> {{ rawData.headers.join(', ') }}</p>
    <!-- Additional insights can be added here -->
    </div>
</div>
</template>

<script>
export default {
name: 'InsightWidget',
props: {
    widget: Object,
    rawData: Object,
},
};
</script>

<style scoped>
/* Additional styling if needed */
</style>
