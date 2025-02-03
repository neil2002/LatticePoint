<template>
<div>
    <h3 class="text-lg font-semibold mb-2">Data Table Widget</h3>
    <div class="overflow-x-auto">
    <table class="table w-full">
        <thead>
        <tr>
            <th v-for="header in rawData.headers" :key="header" class="px-4 py-2 text-left">
            {{ header }}
            </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(row, index) in rawData.rows" :key="index">
            <td v-for="(cell, cellIndex) in row" :key="cellIndex" class="px-4 py-2">
            {{ cell }}
            </td>
        </tr>
        </tbody>
    </table>
    </div>
</div>
</template>

<script>
export default {
name: 'TableWidget',
props: {
    widget: Object,
    rawData: Object,
},
};
</script>

<style scoped>
/* Additional styling if needed */
</style>
