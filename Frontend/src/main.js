import './assets/main.css'
import { createPinia } from 'pinia';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './firebase.js'


const app = createApp(App)
const pinia = createPinia(); // Create a Pinia instance

app.use(pinia);
app.use(router)

// Add store to global properties for Options API access
app.config.globalProperties.$store = {
    auth: {
      signInWithGoogle() {
        return this.auth.signInWithGoogle()
      },
      signOut() {
        return this.auth.signOut()
      },
      ...pinia.state.value.auth
    }
  }


app.mount('#app')

