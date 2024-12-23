// Signup form validation
document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', function (e) {
      const username = this.username.value.trim();
      const email = this.email.value.trim();
      const password = this.password.value.trim();

      // Validate username
      if (!/^[a-zA-Z0-9]+$/.test(username) || username.length < 4 || username.length > 15) {
        alert('Username must be 4-15 characters long and contain only letters and numbers.');
        e.preventDefault();
        return;
      }

      // Validate email
      if (!/^[^\\s@]+@[^\s@]+\\.[^\s@]+$/.test(email)) {
        alert('Please enter a valid email address.');
        e.preventDefault();
        return;
      }

      // Validate password
      if (password.length < 8 || password.length > 20) {
        alert('Password must be 8-20 characters long.');
        e.preventDefault();
        return;
      }
    });
  }

  // Login form validation
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      const username = this.username.value.trim();
      const password = this.password.value.trim();

      // Validate username
      if (!username) {
        alert('Please enter your username.');
        e.preventDefault();
        return;
      }

      // Validate password
      if (!password) {
        alert('Please enter your password.');
        e.preventDefault();
        return;
      }
    });
  }
});
