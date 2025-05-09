// Show login modal
document.getElementById('login-btn').addEventListener('click', () => {
    document.getElementById('login-modal').style.display = 'block';
  });
  
  // Close modal
  document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('login-modal').style.display = 'none';
  });
  
  // Handle local login
  const loginForm = document.getElementById('loginForm');
  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const storedUser = JSON.parse(localStorage.getItem('jiaUser'));
  
    if (storedUser && storedUser.username === username && storedUser.password === password) {
      localStorage.setItem('loggedInUser', JSON.stringify({ name: storedUser.name }));
      showLoggedInUser(storedUser.name);
      document.getElementById('login-modal').style.display = 'none';
    } else {
      alert("Invalid username or password");
    }
  });
  
  // Show signup form instead
  document.getElementById('signup-link').addEventListener('click', () => {
    window.location.href = "signup.html"; // or we can add a signup modal too
  });
  
  // Handle Google Sign-In
  function handleCredentialResponse(response) {
    const data = parseJwt(response.credential);
    const username = data.email.split('@')[0];
  
    localStorage.setItem('loggedInUser', JSON.stringify({ name: username }));
    showLoggedInUser(username);
    document.getElementById('login-modal').style.display = 'none';
  }
  
  // Decode Google JWT token
  function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(c =>
      '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    ).join(''));
  
    return JSON.parse(jsonPayload);
  }
  
  // If already logged in
  function showLoggedInUser(name) {
    document.getElementById('login-btn').style.display = 'none';
    document.getElementById('user-name').style.display = 'inline-block';
    document.getElementById('user-name').textContent = `Hello, ${name}`;
  }
  
  // Check login on page load
  window.onload = () => {
    const user = JSON.parse(localStorage.getItem('loggedInUser'));
    if (user) {
      showLoggedInUser(user.name);
    }
  };
  