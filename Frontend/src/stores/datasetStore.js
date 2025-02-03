import { defineStore } from 'pinia';

export const useDatasetStore = defineStore('csvStore', {
    state: () => ({
        headers: [],
        rows: [],
    }),
    actions: {
        setRawData(headers, rows) {
            this.headers = headers;
            this.rows = rows;
            console.log("hello")
            // Optionally, save to sessionStorage
            sessionStorage.setItem("State", JSON.stringify({
                headers: this.headers,
                rows: this.rows,
            }));
        },
        loadRawData() {
            const savedState = JSON.parse(sessionStorage.getItem("State"));
            if (savedState) {
                this.headers = savedState.headers;
                this.rows = savedState.rows;
            }
        },
    },
});

