// Import Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

// Your Firebase config (paste yours here)
const firebaseConfig = {
  apiKey: "AIzaSyCOuRxcty7SO6qHN47yLYyqtKCZWgHhyfA",
  authDomain: "weathernet-27dc9.firebaseapp.com",
  projectId: "weathernet-27dc9",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(app);

// Export database
export { db };