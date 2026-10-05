/*(function () {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        console.warn("Speech Recognition API not supported in this browser.");
        return;
    }

    let recognition = null;
    let isListening = false;
    let isSpeaking = false;
    
    // Persist active state across page loads
    let isAssistantActive = sessionStorage.getItem("voice_assistant_active") === "true";

    function initRecognition() {
        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.continuous = false; 
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            isListening = true;
            updateIndicator(true);
        };

        recognition.onend = () => {
            isListening = false;
            updateIndicator(false);
            if (!isSpeaking) {
                setTimeout(startListening, 300);
            }
        };

        recognition.onerror = (event) => {
            isListening = false;
            updateIndicator(false);
            if (event.error !== "no-speech" && event.error !== "aborted" && !isSpeaking) {
                setTimeout(startListening, 1000);
            }
        };

        recognition.onresult = async (event) => {
            const transcript = event.results[0][0].transcript.trim();
            console.log("🗣 User said:", transcript);
            await handleCommand(transcript);
        };
    }

    function startListening() {
        if (isListening || isSpeaking || !recognition) return;
        try {
            recognition.start();
        } catch (e) {}
    }

    function stopListening() {
        if (!isListening || !recognition) return;
        try {
            recognition.abort();
        } catch (e) {}
        isListening = false;
        updateIndicator(false);
    }

    // Mutes microphone while AI speaks to prevent feedback loops
    function speak(text, callback = null) {
        if (!text) {
            if (callback) callback();
            return;
        }

        isSpeaking = true;
        stopListening();
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.lang = "en-US";

        utterance.onend = () => {
            isSpeaking = false;
            if (callback) callback();
            setTimeout(startListening, 400); 
        };

        utterance.onerror = () => {
            isSpeaking = false;
            if (callback) callback();
            setTimeout(startListening, 400);
        };

        window.speechSynthesis.speak(utterance);
    }

    async function handleCommand(commandText) {
        try {
            const res = await fetch("/api/voice-command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    command: commandText,
                    is_active: isAssistantActive,
                    current_page: window.location.pathname
                })
            });

            const data = await res.json();
            
            if (typeof data.is_active !== "undefined") {
                isAssistantActive = data.is_active;
                sessionStorage.setItem("voice_assistant_active", isAssistantActive);
            }

            if (data.message) {
                speak(data.message, () => executeAction(data));
            } else {
                executeAction(data);
            }
        } catch (err) {
            console.error("Assistant Error:", err);
            speak("Network error. Cannot reach assistant.");
        }
    }

    // 4. Action Handler
    function executeAction(data) {
        switch (data.action) {
            case "navigate":
                if (data.url && window.location.pathname !== data.url) {
                    window.location.href = data.url;
                }
                break;
            case "history_back":
                window.history.back();
                break;
            case "page_action":
                if (data.target) {
                    // SPECIAL CASE: The SOS Button requires a 3-second hold. 
                    // Virtual clicks fail, so we bypass it and trigger the alarm directly.
                    if (data.target === "sosBtn" && typeof window.triggerSOS === "function") {
                        window.triggerSOS();
                    } else {
                        // Standard click for all other buttons (Call, Scan, Upload, Read Aloud)
                        const el = document.getElementById(data.target);
                        if (el) el.click();
                    }
                }
                break;
            case "sleep":
                isAssistantActive = false;
                sessionStorage.setItem("voice_assistant_active", "false");
                break;
            default:
                break;
        }
    }

    // Visual Indicator for Deaf/Hard of Hearing or Debugging
    function createIndicator() {
        const dot = document.createElement("div");
        dot.id = "voice-indicator";
        Object.assign(dot.style, {
            position: "fixed", bottom: "20px", right: "20px",
            width: "20px", height: "20px", borderRadius: "50%",
            backgroundColor: "#9ca3af", zIndex: "9999",
            boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
            transition: "all 0.3s ease"
        });
        document.body.appendChild(dot);
    }

    function updateIndicator(active) {
        const dot = document.getElementById("voice-indicator");
        if (!dot) return;
        if (isSpeaking) {
            dot.style.backgroundColor = "#2563eb"; // Blue: Speaking
            dot.style.transform = "scale(1.2)";
        } else if (active) {
            dot.style.backgroundColor = isAssistantActive ? "#16a34a" : "#f59e0b"; // Green: Active, Yellow: Awaiting Wake Word
            dot.style.transform = "scale(1.1)";
        } else {
            dot.style.backgroundColor = "#9ca3af"; // Gray: Idle
            dot.style.transform = "scale(1.0)";
        }
    }

    function announceScreen() {
        const path = window.location.pathname;
        const pageNames = {
            "/home": "Home dashboard",
            "/setting": "App Settings",
            "/Snavigation": "Smart Navigation",
            "/documentR": "Document Reader",
            "/documentS": "Document Summary",
            "/profile": "User Profile",
            "/sos": "Emergency SOS"
        };
        const title = pageNames[path];
        if (title && isAssistantActive) {
            speak(`${title}.`);
        }
    }

    window.addEventListener("DOMContentLoaded", () => {
        createIndicator();
        initRecognition();

        // Browsers require a user interaction before Audio/Speech APIs can run
        const unlockAudio = () => {
            if (!isListening && !isSpeaking) {
                startListening();
                announceScreen();
            }
            window.removeEventListener("click", unlockAudio);
            window.removeEventListener("keydown", unlockAudio);
            window.removeEventListener("touchstart", unlockAudio);
        };

        window.addEventListener("click", unlockAudio);
        window.addEventListener("keydown", unlockAudio);
        window.addEventListener("touchstart", unlockAudio);

        if (isAssistantActive) {
            setTimeout(startListening, 500);
        }
    });
})();*/ 

(function () {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        console.warn("Speech Recognition API not supported in this browser.");
        return;
    }

    let recognition = null;
    let isListening = false;
    let isSpeaking = false;
    
    // Persist active state across page loads
    let isAssistantActive = sessionStorage.getItem("voice_assistant_active") === "true";
    
    // NEW: Session state to handle multi-turn conversations (like Login)
    let sessionState = {};

    function initRecognition() {
        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.continuous = false; 
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = () => {
            isListening = true;
            updateIndicator(true);
        };

        recognition.onend = () => {
            isListening = false;
            updateIndicator(false);
            if (!isSpeaking) {
                setTimeout(startListening, 300);
            }
        };

        recognition.onerror = (event) => {
            isListening = false;
            updateIndicator(false);
            if (event.error !== "no-speech" && event.error !== "aborted" && !isSpeaking) {
                setTimeout(startListening, 1000);
            }
        };

        recognition.onresult = async (event) => {
            const transcript = event.results[0][0].transcript.trim();
            console.log("🗣 User said:", transcript);
            await handleCommand(transcript);
        };
    }

    function startListening() {
        if (isListening || isSpeaking || !recognition) return;
        try {
            recognition.start();
        } catch (e) {}
    }

    function stopListening() {
        if (!isListening || !recognition) return;
        try {
            recognition.abort();
        } catch (e) {}
        isListening = false;
        updateIndicator(false);
    }

    function speak(text, callback = null) {
        if (!text) {
            if (callback) callback();
            return;
        }

        isSpeaking = true;
        stopListening();
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.lang = "en-US";

        utterance.onend = () => {
            isSpeaking = false;
            if (callback) callback();
            setTimeout(startListening, 400); 
        };

        utterance.onerror = () => {
            isSpeaking = false;
            if (callback) callback();
            setTimeout(startListening, 400);
        };

        window.speechSynthesis.speak(utterance);
    }

    async function handleCommand(commandText) {
        try {
            const res = await fetch("/api/voice-command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    command: commandText,
                    is_active: isAssistantActive,
                    current_page: window.location.pathname,
                    session_state: sessionState // Send memory to Python
                })
            });

            const data = await res.json();
            
            // Update Activity State
            if (typeof data.is_active !== "undefined") {
                isAssistantActive = data.is_active;
                sessionStorage.setItem("voice_assistant_active", isAssistantActive);
            }

            // Update Conversational Memory
            if (data.session_state) {
                sessionState = data.session_state;
            }

            // Speak and Execute
            if (data.message) {
                speak(data.message, () => executeAction(data));
            } else {
                executeAction(data);
            }
        } catch (err) {
            console.error("Assistant Error:", err);
            speak("Network error. Cannot reach assistant.");
        }
    }

    function executeAction(data) {
        switch (data.action) {
            case "navigate":
                if (data.url && window.location.pathname !== data.url) {
                    window.location.href = data.url;
                }
                break;
            case "history_back":
                window.history.back();
                break;
            case "page_action":
                if (data.target === "sosBtn" && typeof window.triggerSOS === "function") {
                    window.triggerSOS();
                } else {
                    const el = document.getElementById(data.target);
                    if (el) el.click();
                }
                break;
            case "sleep":
                isAssistantActive = false;
                sessionStorage.setItem("voice_assistant_active", "false");
                break;
            
            // --- NEW: CONVERSATIONAL & FORM ACTIONS ---
            case "speak_and_listen":
                // The speak() function already re-opens the mic, so we just force it explicitly here
                startListening();
                break;
            case "fill_and_listen":
                // Finds input by name (e.g. name="email") and fills it
                const inputs = document.getElementsByName(data.target);
                if (inputs.length > 0) inputs[0].value = data.val;
                startListening();
                break;
            case "fill_and_submit":
                // Fills the password and submits the form
                const passInputs = document.getElementsByName(data.target);
                if (passInputs.length > 0) passInputs[0].value = data.val;
                const form = document.querySelector("form");
                if (form) form.submit();
                break;
        }
    }

    function createIndicator() {
        const dot = document.createElement("div");
        dot.id = "voice-indicator";
        Object.assign(dot.style, {
            position: "fixed", bottom: "20px", right: "20px",
            width: "20px", height: "20px", borderRadius: "50%",
            backgroundColor: "#9ca3af", zIndex: "9999",
            boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
            transition: "all 0.3s ease"
        });
        document.body.appendChild(dot);
    }

    function updateIndicator(active) {
        const dot = document.getElementById("voice-indicator");
        if (!dot) return;
        if (isSpeaking) {
            dot.style.backgroundColor = "#2563eb"; // Blue: Speaking
            dot.style.transform = "scale(1.2)";
        } else if (active) {
            dot.style.backgroundColor = isAssistantActive ? "#16a34a" : "#f59e0b"; // Green: Active
            dot.style.transform = "scale(1.1)";
        } else {
            dot.style.backgroundColor = "#9ca3af"; // Gray: Idle
            dot.style.transform = "scale(1.0)";
        }
    }

    function announceScreen() {
        const path = window.location.pathname;
        const pageNames = {
            "/login": "Login Screen. Say 'start login' to enter your credentials.",
            "/home": "Home dashboard",
            "/setting": "App Settings",
            "/Snavigation": "Smart Navigation",
            "/documentR": "Document Reader",
            "/documentS": "Document Summary",
            "/profile": "User Profile",
            "/sos": "Emergency SOS"
        };
        const title = pageNames[path];
        if (title && isAssistantActive) {
            speak(`${title}.`);
        }
    }

    window.addEventListener("DOMContentLoaded", () => {
        createIndicator();
        initRecognition();

        const unlockAudio = () => {
            if (!isListening && !isSpeaking) {
                startListening();
                announceScreen();
            }
            window.removeEventListener("click", unlockAudio);
            window.removeEventListener("keydown", unlockAudio);
            window.removeEventListener("touchstart", unlockAudio);
        };

        window.addEventListener("click", unlockAudio);
        window.addEventListener("keydown", unlockAudio);
        window.addEventListener("touchstart", unlockAudio);

        if (isAssistantActive) {
            setTimeout(startListening, 500);
        }
    });
})();   