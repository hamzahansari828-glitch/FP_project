// Toggle password visibility
function showPassword() {
    const password = document.getElementById("password");
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}

// NEW NATIVE BIOMETRIC LOGIC (AUTHENTICATION MODE)
async function triggerBiometricLogin() {
    // Check if the device has a fingerprint/face scanner available
    if (!window.PublicKeyCredential) {
        alert("Biometrics are not supported on this device or browser.");
        return;
    } 

    try { 
        // Configuration for direct login (verification)
        const publicKeyCredentialRequestOptions = {
            challenge: Uint8Array.from("random-demo-challenge", c => c.charCodeAt(0)),
            rpId: window.location.hostname,
            userVerification: "required",
            timeout: 60000
        };

        // Pause voice assistant while OS takes over
        window.speechSynthesis.cancel();
        
        // navigator.credentials.GET bypasses the save prompt and goes straight to Windows Hello
        const credential = await navigator.credentials.get({
            publicKey: publicKeyCredentialRequestOptions
        });

        // If the fingerprint scan is successful, speak and redirect
        if (credential) {
            // Wake the assistant back up for the next page
            sessionStorage.setItem("voice_assistant_active", "true");
            
            // Announce success
            const utterance = new SpeechSynthesisUtterance("Biometrics verified. Moving forward.");
            
            // Wait for the announcement to finish, then redirect to Home
            utterance.onend = () => {
                window.location.href = "/home";
            };
            
            // Fallback just in case audio fails, so the user doesn't get stuck
            utterance.onerror = () => {
                window.location.href = "/home";
            };

            window.speechSynthesis.speak(utterance);
        }
    } catch (err) {
        console.error("Biometric scan failed or cancelled:", err);
    }
} 