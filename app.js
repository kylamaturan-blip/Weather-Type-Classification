import { db } from "./firebase.js";
import { collection, addDoc } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

// kuhaon ang form
const form = document.getElementById("studentForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault(); // para dili mo refresh

  // kuha data gikan sa input
  const name = document.getElementById("name").value;
  const course = document.getElementById("course").value;

  try {
    await addDoc(collection(db, "students"), {
      name: "Kyla Maturan",
      course: "BSCS",
      time: new Date()
    });

    alert("Na save na!");
    form.reset(); // clear input

  } catch (error) {
    console.error(error);
    alert("Error saving data!");
  }
});