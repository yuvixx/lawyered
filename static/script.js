const signupForm = document.querySelector("#signup");


async function digestMessage(message) {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  return await window.crypto.subtle.digest("SHA-256", data);
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
        alert("Signup successful");
    } else {
        alert(`Error: ${data.error}`);
    }
});