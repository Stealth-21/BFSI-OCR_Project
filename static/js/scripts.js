document.addEventListener("DOMContentLoaded", function () {
    const registerToggle = document.getElementById("registerToggle");
    const loginToggle = document.getElementById("loginToggle");
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");
    const message = document.getElementById("message");
  
    // Toggle to show register form and hide login form
    registerToggle.addEventListener("click", function () {
      registerForm.style.display = "block";
      loginForm.style.display = "none";
      message.textContent = "";
    });
  
    // Toggle to show login form and hide register form
    loginToggle.addEventListener("click", function () {
      loginForm.style.display = "block";
      registerForm.style.display = "none";
      message.textContent = "";
    });
  
    // Example handler for login button
    document.getElementById("loginButton").addEventListener("click", function () {
      const email = document.getElementById("existingEmail").value;
      const password = document.getElementById("existingPassword").value;
      // Call an API or perform MongoDB login integration here.
      // For demonstration, we'll simply show a message.
      if (email && password) {
        message.textContent = "Login button clicked. Implement API integration.";
      } else {
        message.textContent = "Please enter both email and password.";
      }
    });
  
    // Example handler for register button
    document.getElementById("registerButton").addEventListener("click", function () {
      const email = document.getElementById("MailId").value;
      const password = document.getElementById("newPassword").value;
      // Call an API or perform MongoDB registration integration here.
      if (email && password) {
        message.textContent = "Register button clicked. Implement API integration.";
      } else {
        message.textContent = "Please enter both email and password.";
      }
    });
  
    // Example handler for forgot password button
    document.getElementById("forgotPassword").addEventListener("click", function () {
      message.textContent = "Forgot password functionality is not implemented yet.";
    });
  });  