<template>
    <div class="hero min-h-screen bg-base-200">
      <div class="hero-content flex-col">
        <div class="text-center lg:text-left">
          <h1 class="text-5xl font-bold mb-5">Login</h1>
        </div>
        <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
          <div class="card-body">
            <div class="form-control">
              <button 
                @click="handleGoogleSignIn" 
                :disabled="authStore.loading"
                class="btn btn-primary"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-6 w-6 mr-2" 
                  viewBox="0 0 24 24"
                >
                  <path d="M22.56 12.25c0-.78-.07-1.53-.19-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.75h3.57c2.08-1.92 3.28-4.74 3.28-8.07z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-1 7.28-2.69l-3.57-2.75c-.99.69-2.26 1.1-3.71 1.1-2.87 0-5.3-1.94-6.16-4.54H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.12c-.22-.66-.35-1.36-.35-2.12s.13-1.46.35-2.12V7.04H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.96l2.66-2.84z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.46 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.04l3.66 2.84c.86-2.6 3.3-4.5 6.16-4.5z" fill="#EA4335"/>
                </svg>
                {{ authStore.loading ? 'Signing In...' : 'Sign In with Google' }}
              </button>
            </div>
            <div 
              v-if="authStore.error" 
              class="alert alert-error mt-4"
            >
              <div class="flex-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="w-6 h-6 mx-2 stroke-current">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path>
                </svg>
                <label>{{ authStore.error }}</label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        authStore: this.$store.auth
      }
    },
    methods: {
      async handleGoogleSignIn() {
        try {
          await this.authStore.signInWithGoogle()
          this.$router.push('/dashboard')
        } catch (error) {
          console.error('Login failed', error)
        }
      }
    }
  }
  </script>