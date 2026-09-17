import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyBolaY9Ej3M-EXB-_zHSJEDAwdenp2uIaU",
  authDomain: "dravya-guna-97.firebaseapp.com",
  projectId: "dravya-guna-97",
  storageBucket: "dravya-guna-97.firebasestorage.app",
  messagingSenderId: "84513350587",
  appId: "1:84513350587:web:a2a77be972725efe61da9e",
  measurementId: "G-PCL9S31RW9"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const form = document.querySelector(".review-form");
const status = document.querySelector(".review-status");
const submit = document.querySelector(".review-submit");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (submit) submit.disabled = true;
    if (status) { status.className = "review-status"; status.textContent = "Sending feedback…"; status.style.display = "block"; }

    const data = new FormData(form);
    const name = String(data.get("name") || "").trim();
    const email = String(data.get("email") || "").trim();
    const review = String(data.get("review") || data.get("message") || "").trim();

    if (!name || !review) {
      if (status) { status.className = "review-status error"; status.textContent = "Please enter your name and feedback."; }
      if (submit) submit.disabled = false;
      return;
    }

    try {
      await addDoc(collection(db, "reviews"), {
        name,
        email,
        review,
        page: window.location.href,
        path: window.location.pathname,
        userAgent: navigator.userAgent,
        createdAt: serverTimestamp()
      });

      form.reset();
      if (status) { status.className = "review-status success"; status.textContent = "Thank you! Your feedback has been submitted successfully."; }
    } catch (error) {
      console.error("Firebase feedback submission failed:", error);
      if (status) { status.className = "review-status error"; status.textContent = "Unable to submit feedback right now. Please try again."; }
    } finally {
      if (submit) submit.disabled = false;
    }
  });
}
