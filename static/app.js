let currentToken = "";

const loginForm = document.getElementById("login-form");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const tokenField = document.getElementById("token");
const loginStatus = document.getElementById("login-status");
const protectedStatus = document.getElementById("protected-status");
const protectedResponse = document.getElementById("protected-response");
const clearTokenButton = document.getElementById("clear-token");
const callProtectedButton = document.getElementById("call-protected");

function setStatus(element, message, type = "") {
  element.textContent = message;
  element.className = `status ${type}`.trim();
}

function syncToken(token) {
  currentToken = token;
  tokenField.value = token;
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus(loginStatus, "Signing in...");
  protectedResponse.value = "";

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: usernameInput.value,
        password: passwordInput.value,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Login failed.");
    }

    syncToken(data.token);
    setStatus(loginStatus, `Login successful. Token expires in ${data.expires_in_minutes} minutes.`, "success");
  } catch (error) {
    syncToken("");
    setStatus(loginStatus, error.message, "error");
  }
});

clearTokenButton.addEventListener("click", () => {
  syncToken("");
  protectedResponse.value = "";
  setStatus(loginStatus, "Token cleared.");
  setStatus(protectedStatus, "");
});

callProtectedButton.addEventListener("click", async () => {
  setStatus(protectedStatus, "Calling protected endpoint...");
  protectedResponse.value = "";

  try {
    const response = await fetch("/protected", {
      headers: currentToken ? { Authorization: `Bearer ${currentToken}` } : {},
    });

    const data = await response.json();
    protectedResponse.value = JSON.stringify(data, null, 2);

    if (!response.ok) {
      throw new Error(data.error || "Protected request failed.");
    }

    setStatus(protectedStatus, "Protected request succeeded.", "success");
  } catch (error) {
    setStatus(protectedStatus, error.message, "error");
  }
});
