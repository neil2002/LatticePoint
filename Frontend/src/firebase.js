import { initializeApp } from 'firebase/app';
import { 
  getAuth, 
  signInWithPopup, 
  GoogleAuthProvider, 
  signOut, 
  onAuthStateChanged 
} from 'firebase/auth';

console.log(import.meta.env.VITE_FIREBASE_API_KEY)
// Your Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCs-IPMLJr6NRQ1L4GG5HC3K_2OlIPYEvc",
  authDomain: "latticepointai.firebaseapp.com",
  projectId: "latticepointai",
  storageBucket: "latticepointai.firebasestorage.app",
  messagingSenderId: "745977797067",
  appId: "1:745977797067:web:c2f58449e58e528a30be4e"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

// Authentication methods
export const firebaseAuth = {
  async signInWithGoogle() {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      return result.user;
    } catch (error) {
      console.error('Google Sign-In Error', error);
      throw error;
    }
  },

  async signOutUser() {
    try {
      await signOut(auth);
    } catch (error) {
      console.error('Sign Out Error', error);
      throw error;
    }
  },

  onAuthStateChange(callback) {
    return onAuthStateChanged(auth, callback);
  }
};