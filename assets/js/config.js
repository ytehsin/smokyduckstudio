/* =========================================================
   smokyDuck — SITE SETTINGS
   This is the ONLY file you need to edit to switch things on.
   Leave a value as "" and the related button/feature hides itself.
   ========================================================= */
window.SD_CONFIG = {
  email: "hello@smokyduckstudio.com",

  // WhatsApp Business number: country code + number, digits only.
  // Example for India: "919812345678"   (no +, no spaces)
  whatsapp: "918866666447",

  // Paste your Google Apps Script "Web app" URL here (see automation/SETUP.md).
  // Until it is set, forms open the visitor's email app with everything pre-filled.
  formEndpoint: "https://script.google.com/macros/s/AKfycbxIJkkegfcl6_HYZ5eCyGjXnQwarw1Th9mix9rZcXny0qE6uall4o1wSbalaFr7xXQd/exec",

  // Google Analytics 4 measurement ID, e.g. "G-ABC123XYZ".
  // Loads ONLY after the visitor accepts analytics cookies.
  ga4: "",

  // Social profile URLs. Empty = link hidden.
  social: {
    instagram: "",
    linkedin: "",
    youtube: "",
    facebook: "",
    x: ""
  }
};
