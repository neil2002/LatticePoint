import { defineStore } from 'pinia';
import { firebaseAuth } from '../firebase.js';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  actions: {
    async signInWithGoogle() {
      this.loading = true;
      this.error = null;

      try {
        // Sign in with Firebase
        const firebaseUser = await firebaseAuth.signInWithGoogle();
        
        // Get Firebase token
        const token = await firebaseUser.getIdToken();

        // Send token to backend for verification and user creation/login
        const response = await axios.post('/api/auth/login', { 
          token,
          email: firebaseUser.email,
          displayName: firebaseUser.displayName
        });

        // Update store with user info from backend
        this.user = {
          uid: firebaseUser.uid,
          email: firebaseUser.email,
          displayName: firebaseUser.displayName,
          photoURL: firebaseUser.photoURL
        };
        this.isAuthenticated = true;
      } catch (error) {
        this.error = error.message;
        this.isAuthenticated = false;
      } finally {
        this.loading = false;
      }
    },

    async signOut() {
      this.loading = true;
      this.error = null;

      try {
        // Sign out from Firebase
        await firebaseAuth.signOutUser();
        
        // Call backend logout endpoint
        await axios.post('/api/auth/logout');

        // Reset store
        this.user = null;
        this.isAuthenticated = false;
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },

    initializeAuth() {
      firebaseAuth.onAuthStateChange((user) => {
        if (user) {
          this.user = {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL
          };
          this.isAuthenticated = true;
        } else {
          this.user = null;
          this.isAuthenticated = false;
        }
      });
    }
  }
});