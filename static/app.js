const signupForm = document.querySelector("#signup");
const signinForm = document.querySelector("#signin");
const authWindow = document.querySelector("#auth-window");
const chatWindow = document.querySelector("#chat-window");
const sendButton = document.querySelector("#send");
const userInput = document.querySelector("#user-input");


async function digestMessage(message) {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  return await window.crypto.subtle.digest("SHA-256", data);
}

function revealChatWindow() {
    authWindow.style.display = "none";
    chatWindow.style.display = "flex";
}

signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = signupForm["username"].value;
    const email = signupForm["email"].value;
    const password = signupForm["password"].value;
    const hashedPasswordHex = Array.from(
        new Uint8Array(await digestMessage(password))
    ).map(b => b.toString(16).padStart(2, '0')).join('');
    const passwordHexStr = hashedPasswordHex.toString();
    const resp = await fetch("/api/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: passwordHexStr,
        }),
    });
    const data = await resp.json();
    if (resp.ok) {
        revealChatWindow();
    } else {
        alert(`Error: ${data.error}`);
    }
});

signinForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = signinForm["email"].value;
    const password = signinForm["password"].value;
    const hashedPasswordHex = Array.from(
        new Uint8Array(await digestMessage(password))
    ).map(b => b.toString(16).padStart(2, '0')).join('');
    const passwordHexStr = hashedPasswordHex.toString();
    const resp = await fetch("/api/signin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: null,
            email: email,
            password: passwordHexStr,
        }),
    });
    const data = await resp.json();
    if (resp.ok) {
        revealChatWindow();
    } else {
        alert(`Error: ${data.error}`);
    }
});

sendButton.addEventListener("click", async (e) => {
    e.preventDefault();
    const message = userInput.value;
    const resp = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message: message,
        }),
    });
    const data = await resp.json();
    if (resp.ok) {
        const messageElement = document.createElement("div");
        messageElement.innerText = message;
        document.querySelector("#messages").appendChild(messageElement);
    } else {
        alert(`Error: ${data.error}`);
    }
});