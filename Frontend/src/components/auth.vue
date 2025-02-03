<template>
<div class="auth-container">
    <div v-if="!authStore.isAuthenticated">
    <button 
        @click="handleGoogleSignIn" 
        :disabled="authStore.loading"
    >
        {{ authStore.loading ? 'Signing In...' : 'Sign In with Google' }}
    </button>
    <p v-if="authStore.error" class="error-message">
        {{ authStore.error }}
    </p>
    </div>
    <div v-else>
    <div class="user-info">
        <img 
        v-if="authStore.user?.photoURL" 
        :src="authStore.user.photoURL" 
        alt="Profile"
        class="profile-picture"
        />
        <p>Welcome, {{ authStore.user?.displayName }}</p>
    </div>
    <button 
        @click="handleSignOut" 
        :disabled="authStore.loading"
    >
        {{ authStore.loading ? 'Signing Out...' : 'Sign Out' }}
    </button>
    </div>
</div>
</template>

<script>
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';

export default {
setup() {
    const authStore = useAuthStore();

    const handleGoogleSignIn = async () => {
    try {
        await authStore.signInWithGoogle();
    } catch (error) {
        console.error('Sign in failed', error);
    }
    };

    const handleSignOut = async () => {
    try {
        await authStore.signOut();
    } catch (error) {
        console.error('Sign out failed', error);
    }
    };

    onMounted(() => {
    // Initialize auth state listener
    authStore.initializeAuth();
    });

    return {
    authStore,
    handleGoogleSignIn,
    handleSignOut
    };
}
}
</script>

<style scoped>
.auth-container {
display: flex;
flex-direction: column;
align-items: center;
padding: 20px;
}

.user-info {
display: flex;
align-items: center;
margin-bottom: 15px;
}

.profile-picture {
width: 50px;
height: 50px;
border-radius: 50%;
margin-right: 10px;
}

.error-message {
color: red;
margin-top: 10px;
}

button {
padding: 10px 15px;
background-color: #4285f4;
color: white;
border: none;
border-radius: 5px;
cursor: pointer;
}

button:disabled {
background-color: #ccc;
cursor: not-allowed;
}
</style>