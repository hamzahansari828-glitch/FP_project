'''
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

assistant_active = False


def contains_exact_word(command, word_list):
    clean_command = re.sub(r'[^\w\s]', '', command)
    words = clean_command.split()

    for item in word_list:
        item_words = item.split()

        if len(item_words) == 1:
            if item in words:
                return True
        else:
            if item in clean_command:
                return True

    return False


@app.route("/voice", methods=["POST"])
def voice_command():

    global assistant_active

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "action": "error",
            "message": "No voice command received."
        })

    command = data.get("command", "").lower().strip()

    print("================================")
    print("🎤 User:", command)
    print("Assistant active:", assistant_active)
    print("================================")


    # ==========================================
    # ASSISTANT NOT ACTIVE
    # ==========================================

    if not assistant_active:

        yes_words = [
            "yes",
            "yeah",
            "yep",
            "yup",
            "sure",
            "okay",
            "ok",
            "of course",
            "yes please"
        ]

        wake_words = [
            "hey greendge",
            "hey green edge",
            "hey greenege",
            "hey",
            "hello",
            "hi",
            "wakeup",
            "wake up"
        ]

        no_words = [
            "no",
            "nope",
            "not now",
            "no thanks"
        ]


        # YES
        if contains_exact_word(command, yes_words):

            assistant_active = True

            print("✅ ASSISTANT ACTIVATED")

            return jsonify({
                "success": True,
                "action": "activate",
                "message": "Great. How can I help you?"
            })


        # WAKE WORD
        if contains_exact_word(command, wake_words):

            assistant_active = True

            print("✅ ASSISTANT ACTIVATED BY WAKE WORD")

            return jsonify({
                "success": True,
                "action": "activate",
                "message": "Yes, how can I help you?"
            })


        # NO
        if contains_exact_word(command, no_words):

            return jsonify({
                "success": True,
                "action": "waiting",
                "message": "Okay. Say wakeup whenever you need me."
            })


        return jsonify({
            "success": True,
            "action": "waiting",
            "message": "Please say yes or no."
        })


    # ==========================================
    # ASSISTANT ACTIVE
    # ==========================================

    # NAVIGATION
    if "navigation" in command or "navigate" in command:

        print("🧭 NAVIGATION COMMAND DETECTED")

        return jsonify({
            "success": True,
            "action": "navigation",
            "message": "Opening navigation."
        })


    # SETTINGS
    if "setting" in command or "settings" in command:

        return jsonify({
            "success": True,
            "action": "setting",
            "message": "Opening settings."
        })


    # PROFILE
    if "profile" in command:

        return jsonify({
            "success": True,
            "action": "profile",
            "message": "Opening profile."
        })


    # DOCUMENT READER
    if "read document" in command or "document reader" in command:

        return jsonify({
            "success": True,
            "action": "documentR",
            "message": "Opening document reader."
        })


    # DOCUMENT SUMMARY
    if "document summary" in command or "summary" in command:

        return jsonify({
            "success": True,
            "action": "documentS",
            "message": "Opening document summary."
        })


    # LOCATION
    if "location" in command or "where am i" in command:

        return jsonify({
            "success": True,
            "action": "location",
            "message": "Opening your location."
        })


    # SOS
    if (
        "emergency" in command
        or "sos" in command
        or "help me" in command
    ):

        return jsonify({
            "success": True,
            "action": "emergency",
            "message": "Opening emergency SOS."
        })


    # STOP ASSISTANT
    if any(stop_phrase in command for stop_phrase in [
        "stop voice assistant",
        "turn off voice assistant",
        "stop assistant",
        "stop listening"
    ]):

        assistant_active = False

        return jsonify({
            "success": True,
            "action": "waiting",
            "message": "Okay. I am going quiet. Say wakeup when you need me."
        })


    # UNKNOWN
    return jsonify({
        "success": True,
        "action": "unknown",
        "message": "Sorry, I didn't understand that command."
    })


if __name__ == "__main__":

    print("================================")
    print("Voice Assistant running")
    print("http://127.0.0.1:5000")
    print("================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )




import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

assistant_active = False


def contains_exact_word(command, word_list):
    # Replace non-alphanumeric chars with spaces to prevent words from sticking together
    clean_command = re.sub(r'[^\w\s]', ' ', command.lower())
    clean_command = " ".join(clean_command.split())  # Normalize extra spaces

    for item in word_list:
        pattern = r'\b' + re.escape(item.lower()) + r'\b'
        if re.search(pattern, clean_command):
            return True

    return False


@app.route("/voice", methods=["POST"])
def voice_command():
    global assistant_active

    data = request.get_json() or {}
    command = data.get("command", "").lower().strip()

    if not command:
        return jsonify({
            "success": False,
            "action": "error",
            "message": "No voice command received."
        })

    print("================================")
    print("🎤 User:", command)
    print("Assistant active:", assistant_active)
    print("================================")

    yes_words = ["yes", "yeah", "yep", "yup", "sure", "okay", "ok", "of course", "yes please"]
    wake_words = ["hey greendge", "hey green edge", "hey greenege", "hey", "hello", "hi", "wakeup", "wake up"]
    no_words = ["no", "nope", "not now", "no thanks"]

    # ==========================================
    # ASSISTANT NOT ACTIVE
    # ==========================================
    if not assistant_active:

        if contains_exact_word(command, yes_words) or contains_exact_word(command, wake_words):
            assistant_active = True
            print("✅ ASSISTANT ACTIVATED")
            return jsonify({
                "success": True,
                "action": "activate",
                "message": "Great. How can I help you?"
            })

        if contains_exact_word(command, no_words):
            return jsonify({
                "success": True,
                "action": "waiting",
                "message": "Okay. Say wakeup whenever you need me."
            })

        return jsonify({
            "success": True,
            "action": "waiting",
            "message": "Please say yes or wake up to start."
        })

    # ==========================================
    # ASSISTANT ACTIVE
    # ==========================================

    # Handle redundant "yes" / acknowledgment while already active
    if contains_exact_word(command, yes_words):
        return jsonify({
            "success": True,
            "action": "listening",
            "message": "I am listening. What would you like to do?"
        })

    # NAVIGATION
    if "navigation" in command or "navigate" in command:
        return jsonify({
            "success": True,
            "action": "navigation",
            "message": "Opening navigation."
        })

    # SETTINGS
    if "setting" in command or "settings" in command:
        return jsonify({
            "success": True,
            "action": "setting",
            "message": "Opening settings."
        })

    # PROFILE
    if "profile" in command:
        return jsonify({
            "success": True,
            "action": "profile",
            "message": "Opening profile."
        })

    # DOCUMENT READER
    if "read document" in command or "document reader" in command:
        return jsonify({
            "success": True,
            "action": "documentR",
            "message": "Opening document reader."
        })

    # DOCUMENT SUMMARY
    if "document summary" in command or "summary" in command:
        return jsonify({
            "success": True,
            "action": "documentS",
            "message": "Opening document summary."
        })

    # LOCATION
    if "location" in command or "where am i" in command:
        return jsonify({
            "success": True,
            "action": "location",
            "message": "Opening your location."
        })

    # SOS / EMERGENCY
    if any(kw in command for kw in ["emergency", "sos", "help me"]):
        return jsonify({
            "success": True,
            "action": "emergency",
            "message": "Opening emergency SOS."
        })

    # STOP ASSISTANT
    if any(stop_phrase in command for stop_phrase in [
        "stop voice assistant",
        "turn off voice assistant",
        "stop assistant",
        "stop listening"
    ]):
        assistant_active = False
        return jsonify({
            "success": True,
            "action": "waiting",
            "message": "Okay. I am going quiet. Say wakeup when you need me."
        })

    # UNKNOWN
    return jsonify({
        "success": True,
        "action": "unknown",
        "message": "Sorry, I didn't understand that command."
    })


if __name__ == "__main__":

    print("================================")
    print("Voice Assistant running")
    print("http://127.0.0.1:5000")
    print("================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )





import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

assistant_active = False

# Simplified and more accurate exact word matching
def contains_exact_word(command, word_list):
    # Remove punctuation and pad with spaces (e.g., " yes open ")
    clean_command = f" {re.sub(r'[^\w\s]', '', command)} "
    
    for item in word_list:
        # Pad the item with spaces to ensure exact whole-word match
        if f" {item} " in clean_command:
            return True
            
    return False


@app.route("/voice", methods=["POST"])
def voice_command():
    global assistant_active

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "action": "error",
            "message": "No voice command received."
        })

    command = data.get("command", "").lower().strip()

    print("================================")
    print("🎤 User:", command)
    print("Assistant active:", assistant_active)
    print("================================")

    yes_words = ["yes", "yeah", "yep", "yup", "sure", "okay", "ok", "of course", "yes please"]
    wake_words = ["hey greendge", "hey green edge", "hey greenege", "hey", "hello", "hi", "wakeup", "wake up"]
    no_words = ["no", "nope", "not now", "no thanks"]
    stop_words = ["stop voice assistant", "turn off voice assistant", "stop assistant", "stop listening"]

    # ==========================================
    # 1. STOP COMMAND (Check this first)
    # ==========================================
    if any(stop_phrase in command for stop_phrase in stop_words):
        assistant_active = False
        return jsonify({
            "success": True,
            "action": "waiting",
            "message": "Okay. I am going quiet. Say wakeup when you need me."
        })

    # ==========================================
    # 2. EXTRACT INTENTS
    # ==========================================
    is_yes = contains_exact_word(command, yes_words)
    is_wake = contains_exact_word(command, wake_words)
    is_no = contains_exact_word(command, no_words)

    # ==========================================
    # 3. HANDLE INACTIVE STATE
    # ==========================================
    if not assistant_active:
        if is_yes or is_wake:
            # Wake the assistant up, but DON'T return yet. 
            # Let it pass through in case they said "yes open settings"
            assistant_active = True
            print("✅ ASSISTANT ACTIVATED")
        elif is_no:
            return jsonify({
                "success": True,
                "action": "waiting",
                "message": "Okay. Say wakeup whenever you need me."
            })
        else:
            return jsonify({
                "success": True,
                "action": "waiting",
                "message": "Please say yes or no."
            })

    # ==========================================
    # 4. COMMAND MATCHING (Assistant is Active)
    # ==========================================
    
    if "navigation" in command or "navigate" in command:
        print("🧭 NAVIGATION COMMAND DETECTED")
        return jsonify({"success": True, "action": "navigation", "message": "Opening navigation."})

    if "setting" in command or "settings" in command:
        return jsonify({"success": True, "action": "setting", "message": "Opening settings."})

    if "profile" in command:
        return jsonify({"success": True, "action": "profile", "message": "Opening profile."})

    if "read document" in command or "document reader" in command:
        return jsonify({"success": True, "action": "documentR", "message": "Opening document reader."})

    if "document summary" in command or "summary" in command:
        return jsonify({"success": True, "action": "documentS", "message": "Opening document summary."})

    if "location" in command or "where am i" in command:
        return jsonify({"success": True, "action": "location", "message": "Opening your location."})

    if "emergency" in command or "sos" in command or "help me" in command:
        return jsonify({"success": True, "action": "emergency", "message": "Opening emergency SOS."})

    # ==========================================
    # 5. NO SPECIFIC COMMAND MATCHED
    # ==========================================
    
    # If the user just said "yes" or "wake up" (without a following command), gracefully reply
    if is_yes or is_wake:
        return jsonify({
            "success": True,
            "action": "activate",
            "message": "Yes, how can I help you?"
        })

    # If it reached here, it's active, but no commands or wake words matched.
    return jsonify({
        "success": True,
        "action": "unknown",
        "message": "Sorry, I didn't understand that command."
    })


if __name__ == "__main__":
    print("================================")
    print("Voice Assistant running")
    print("http://127.0.0.1:5000")
    print("================================")
    
    app.run(host="0.0.0.0", port=5000, debug=True) 


import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def contains_exact_word(command, word_list):
    clean_command = f" {re.sub(r'[^\w\s]', '', command)} "
    for item in word_list:
        if f" {item} " in clean_command:
            return True
    return False

@app.route("/voice", methods=["POST"])
def voice_command():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "action": "error",
            "message": "No voice command received."
        })

    command = data.get("command", "").lower().strip()
    
    # NEW: Get the active state from the frontend (defaults to False)
    # We no longer use 'global assistant_active'
    assistant_active = data.get("is_active", False)

    print("================================")
    print("🎤 User:", command)
    print("Assistant active (from frontend):", assistant_active)
    print("================================")

    yes_words = ["yes", "yeah", "yep", "yup", "sure", "okay", "ok", "of course", "yes please"]
    wake_words = ["hey greendge", "hey green edge", "hey greenege", "hey", "hello", "hi", "wakeup", "wake up"]
    no_words = ["no", "nope", "not now", "no thanks"]
    stop_words = ["stop voice assistant", "turn off voice assistant", "stop assistant", "stop listening"]

    # 1. STOP COMMAND
    if any(stop_phrase in command for stop_phrase in stop_words):
        return jsonify({
            "success": True,
            "action": "waiting",
            "message": "Okay. I am going quiet. Say wakeup when you need me.",
            "new_state": False # Tell the frontend to turn off
        })

    # 2. EXTRACT INTENTS
    is_yes = contains_exact_word(command, yes_words)
    is_wake = contains_exact_word(command, wake_words)
    is_no = contains_exact_word(command, no_words)

    # 3. HANDLE INACTIVE STATE
    if not assistant_active:
        if is_yes or is_wake:
            return jsonify({
                "success": True,
                "action": "activate",
                "message": "Yes, how can I help you?",
                "new_state": True # Tell the frontend it is now ACTIVE
            })
        elif is_no:
            return jsonify({
                "success": True,
                "action": "waiting",
                "message": "Okay. Say wakeup whenever you need me.",
                "new_state": False
            })
        else:
            return jsonify({
                "success": True,
                "action": "waiting",
                "message": "Please say yes or no.",
                "new_state": False
            })

    # 4. COMMAND MATCHING (Assistant is Active)
    if "navigation" in command or "navigate" in command:
        return jsonify({"success": True, "action": "navigation", "message": "Opening navigation.", "new_state": True})

    if "setting" in command or "settings" in command:
        return jsonify({"success": True, "action": "setting", "message": "Opening settings.", "new_state": True})

    if "profile" in command:
        return jsonify({"success": True, "action": "profile", "message": "Opening profile.", "new_state": True})

    if "read document" in command or "document reader" in command:
        return jsonify({"success": True, "action": "documentR", "message": "Opening document reader.", "new_state": True})

    if "document summary" in command or "summary" in command:
        return jsonify({"success": True, "action": "documentS", "message": "Opening document summary.", "new_state": True})

    if "location" in command or "where am i" in command:
        return jsonify({"success": True, "action": "location", "message": "Opening your location.", "new_state": True})

    if "emergency" in command or "sos" in command or "help me" in command:
        return jsonify({"success": True, "action": "emergency", "message": "Opening emergency SOS.", "new_state": True})

    # 5. NO SPECIFIC COMMAND MATCHED
    if is_yes or is_wake:
        return jsonify({
            "success": True,
            "action": "activate",
            "message": "Yes, how can I help you?",
            "new_state": True
        })

    return jsonify({
        "success": True,
        "action": "unknown",
        "message": "Sorry, I didn't understand that command.",
        "new_state": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def contains_any(command, phrases):
    clean = f" {re.sub(r'[^\w\s]', ' ', command.lower())} "
    clean = " ".join(clean.split())
    for phrase in phrases:
        pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
        if re.search(pattern, clean):
            return True
    return False

@app.route("/voice", methods=["POST"])
def process_voice():
    data = request.get_json() or {}
    raw_command = data.get("command", "").lower().strip()
    is_active = data.get("is_active", False)
    current_page = data.get("current_page", "")

    if not raw_command:
        return jsonify({
            "success": False,
            "action": "none",
            "message": "I did not hear anything."
        })

    print(f"🎤 Heard: '{raw_command}' | Active: {is_active} | Page: {current_page}")

    wake_words = ["hey greenedge", "greenedge", "green edge", "hey assistant", "wakeup", "wake up", "hello"]
    stop_words = ["stop listening", "go quiet", "sleep", "shut up", "turn off assistant", "mute"]
    help_words = ["help", "what can i say", "commands", "how to use"]

    # 1. Check for Stop / Sleep
    if contains_any(raw_command, stop_words):
        return jsonify({
            "success": True,
            "action": "sleep",
            "message": "Going to sleep. Say 'Hey GreenEdge' or tap the screen when you need me.",
            "is_active": False
        })

    # 2. Wake-up Detection
    woke_up = contains_any(raw_command, wake_words)
    if woke_up:
        is_active = True

    # Strip wake word to extract the actual command if spoken together
    cmd = raw_command
    for w in wake_words:
        cmd = cmd.replace(w, "").strip()

    # If user ONLY said wake word
    if woke_up and not cmd:
        return jsonify({
            "success": True,
            "action": "activated",
            "message": "I am listening. How can I help you?",
            "is_active": True
        })

    # If assistant is not active and no wake word was triggered, ignore background noise
    if not is_active:
        return jsonify({
            "success": True,
            "action": "ignored",
            "message": "",
            "is_active": False
        })

    # 3. Help Intent
    if contains_any(cmd, help_words):
        return jsonify({
            "success": True,
            "action": "speak_only",
            "message": "You can say: open navigation, read document, summarize document, where am I, emergency SOS, go home, or go back.",
            "is_active": True
        })

    # 4. Global Navigation Intents
    if contains_any(cmd, ["go back", "back", "previous screen"]):
        return jsonify({"success": True, "action": "history_back", "message": "Going back.", "is_active": True})

    if contains_any(cmd, ["home", "dashboard", "main menu"]):
        return jsonify({"success": True, "action": "navigate", "url": "/home", "message": "Opening Home dashboard.", "is_active": True})

    if contains_any(cmd, ["navigation", "smart navigation", "start walking", "navigate"]):
        return jsonify({"success": True, "action": "navigate", "url": "/Snavigation", "message": "Opening smart navigation.", "is_active": True})

    if contains_any(cmd, ["read document", "document reader", "scanner", "scan text"]):
        return jsonify({"success": True, "action": "navigate", "url": "/documentR", "message": "Opening document reader.", "is_active": True})

    if contains_any(cmd, ["summary", "document summary", "summarize"]):
        return jsonify({"success": True, "action": "navigate", "url": "/documentS", "message": "Opening document summary.", "is_active": True})

    if contains_any(cmd, ["location", "where am i", "my location", "gps"]):
        return jsonify({"success": True, "action": "navigate", "url": "/location", "message": "Fetching your walking location.", "is_active": True})

    if contains_any(cmd, ["settings", "setting", "preferences", "app settings"]):
        return jsonify({"success": True, "action": "navigate", "url": "/setting", "message": "Opening settings.", "is_active": True})

    if contains_any(cmd, ["profile", "my account", "user profile"]):
        return jsonify({"success": True, "action": "navigate", "url": "/profile", "message": "Opening profile.", "is_active": True})

    if contains_any(cmd, ["sos", "emergency", "help me", "call guardian", "danger"]):
        return jsonify({"success": True, "action": "navigate", "url": "/sos", "message": "Opening emergency SOS.", "is_active": True})

    # 5. In-Page Specific Actions
    if contains_any(cmd, ["scan", "take photo", "capture"]):
        return jsonify({"success": True, "action": "page_action", "target": "scanBtn", "message": "Opening camera to scan.", "is_active": True})

    if contains_any(cmd, ["read aloud", "read text", "play audio", "listen"]):
        return jsonify({"success": True, "action": "page_action", "target": "readAloudBtn", "message": "Reading extracted text.", "is_active": True})

    if contains_any(cmd, ["trigger sos", "send alert", "sound siren"]):
        return jsonify({"success": True, "action": "page_action", "target": "sosBtn", "message": "Triggering SOS.", "is_active": True})

    # 6. Fallback
    return jsonify({
        "success": True,
        "action": "unknown",
        "message": "Sorry, I didn't recognize that command. Say help to hear available commands.",
        "is_active": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 






import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def contains_any(command, phrases):
    clean = f" {re.sub(r'[^\w\s]', ' ', command.lower())} "
    clean = " ".join(clean.split())
    for phrase in phrases:
        pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
        if re.search(pattern, clean):
            return True
    return False

@app.route("/voice", methods=["POST"])
def process_voice():
    data = request.get_json() or {}
    raw_command = data.get("command", "").lower().strip()
    is_active = data.get("is_active", False)
    current_page = data.get("current_page", "")

    if not raw_command:
        return jsonify({"success": False, "action": "none", "message": ""})

    print(f"🎤 Heard: '{raw_command}' | Active: {is_active} | Page: {current_page}")

    # Sorted longest-to-shortest to strip phrases cleanly
    wake_words = ["hey greenedge", "hey green edge", "greenedge", "green edge", "hey assistant", "wakeup", "wake up", "hello", "hey"]
    stop_words = ["stop listening", "go quiet", "sleep", "shut up", "turn off assistant", "mute", "stop"]
    help_words = ["help", "what can i say", "commands", "how to use"]

    # 1. Check for Stop / Sleep
    if contains_any(raw_command, stop_words):
        return jsonify({
            "success": True,
            "action": "sleep",
            "message": "Going to sleep. Say 'Hey GreenEdge' when you need me.",
            "is_active": False
        })

    # 2. Wake-up Detection & Command Extraction
    woke_up = contains_any(raw_command, wake_words)
    
    cmd = raw_command
    if woke_up:
        # Strip the wake words out of the sentence to see if a command is attached
        for w in sorted(wake_words, key=len, reverse=True):
            cmd = re.sub(r'\b' + re.escape(w) + r'\b', '', cmd).strip()

    # 3. State Management & Welcoming
    if not is_active:
        if woke_up:
            # Waking up from sleep! 
            # If they just said the wake word OR there's background noise without a valid command, welcome them.
            valid_intents = ["navigate", "navigation", "read", "scan", "summary", "summarize", "location", "where", "setting", "settings", "profile", "sos", "emergency", "home", "back"]
            if not cmd or not contains_any(cmd, valid_intents):
                return jsonify({
                    "success": True,
                    "action": "activated",
                    "message": "Hey User, welcome back. How may I help you?",
                    "is_active": True
                })
            else:
                is_active = True # Continue down to process the valid command
        else:
            # Asleep and no wake word detected -> ignore background noise
            return jsonify({"success": True, "action": "ignored", "message": "", "is_active": False})
    else:
        # Already active. If they just say a wake word as an acknowledgment
        if woke_up and not cmd:
            return jsonify({
                "success": True,
                "action": "activated",
                "message": "I am listening. What would you like to do?",
                "is_active": True
            })

    # 4. Help Intent
    if contains_any(cmd, help_words):
        return jsonify({"success": True, "action": "speak_only", "message": "You can say: open navigation, read document, summarize document, where am I, emergency SOS, go home, or go back.", "is_active": True})

   # 5. Global Navigation & Context-Aware Intents
    if contains_any(cmd, ["go back", "back", "previous screen", "return"]):
        return jsonify({"success": True, "action": "history_back", "message": "Going back.", "is_active": True})

    if contains_any(cmd, ["home", "dashboard", "main menu"]):
        return jsonify({"success": True, "action": "navigate", "url": "/home", "message": "Opening Home dashboard.", "is_active": True})

    if contains_any(cmd, ["navigation", "smart navigation", "start walking", "navigate"]):
        return jsonify({"success": True, "action": "navigate", "url": "/Snavigation", "message": "Opening smart navigation.", "is_active": True})

    if contains_any(cmd, ["read document", "document reader", "scanner", "scan text"]):
        return jsonify({"success": True, "action": "navigate", "url": "/documentR", "message": "Opening document reader.", "is_active": True})

    if contains_any(cmd, ["summary", "document summary", "summarize"]):
        return jsonify({"success": True, "action": "navigate", "url": "/documentS", "message": "Opening document summary.", "is_active": True})

    if contains_any(cmd, ["location", "where am i", "my location", "gps"]):
        return jsonify({"success": True, "action": "navigate", "url": "/location", "message": "Fetching your walking location.", "is_active": True})

    if contains_any(cmd, ["settings", "setting", "preferences", "app settings"]):
        return jsonify({"success": True, "action": "navigate", "url": "/setting", "message": "Opening settings.", "is_active": True})

    if contains_any(cmd, ["profile", "my account", "user profile"]):
        return jsonify({"success": True, "action": "navigate", "url": "/profile", "message": "Opening profile.", "is_active": True})

    # --- NEW CONTEXT-AWARE SOS LOGIC ---
    if contains_any(cmd, ["sos", "emergency", "help me", "danger", "trigger sos", "sound siren"]):
        if current_page == "/sos":
            return jsonify({"success": True, "action": "page_action", "target": "sosBtn", "message": "Triggering SOS.", "is_active": True})
        else:
            return jsonify({"success": True, "action": "navigate", "url": "/sos", "message": "Opening emergency SOS.", "is_active": True})

    if contains_any(cmd, ["call guardian", "call mother", "make a call", "call contact", "dial"]):
        if current_page == "/sos":
            return jsonify({"success": True, "action": "page_action", "target": "callBtn", "message": "Calling your emergency contact.", "is_active": True})
        else:
            return jsonify({"success": True, "action": "navigate", "url": "/sos", "message": "Opening emergency SOS to make a call.", "is_active": True})


    # 6. In-Page Specific Actions (Buttons & Controls)
    if contains_any(cmd, ["scan", "take photo", "capture", "scan document"]):
        return jsonify({"success": True, "action": "page_action", "target": "scanBtn", "message": "Opening camera.", "is_active": True})

    if contains_any(cmd, ["upload", "gallery", "choose file", "upload document", "upload from gallery"]):
        return jsonify({"success": True, "action": "page_action", "target": "uploadBtn", "message": "Opening file browser.", "is_active": True})

    if contains_any(cmd, ["read aloud", "read text", "play audio", "listen", "read it"]):
        return jsonify({"success": True, "action": "page_action", "target": "readAloudBtn", "message": "Reading extracted text.", "is_active": True}) 
    # 7. Fallback
    return jsonify({
        "success": True,
        "action": "unknown",
        "message": "Sorry, I didn't recognize that command. Say help to hear available commands.",
        "is_active": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 
''' 



import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def contains_any(command, phrases):
    clean = f" {re.sub(r'[^\w\s]', ' ', command.lower())} "
    clean = " ".join(clean.split())
    for phrase in phrases:
        pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
        if re.search(pattern, clean):
            return True
    return False

@app.route("/voice", methods=["POST"])
def process_voice():
    data = request.get_json() or {}
    raw_command = data.get("command", "").lower().strip()
    is_active = data.get("is_active", False)
    current_page = data.get("current_page", "")
    
    # Extract Conversational Memory
    session_state = data.get("session_state", {})
    step = session_state.get("step", "idle")

    if not raw_command:
        return jsonify({"success": False, "action": "none", "message": ""})

    print(f"🎤 Heard: '{raw_command}' | Active: {is_active} | Page: {current_page} | Step: {step}")

    wake_words = ["hey greenedge", "hey green edge", "greenedge", "green edge", "hey assistant", "wakeup", "wake up", "hello", "hey"]
    stop_words = ["stop listening", "go quiet", "sleep", "shut up", "turn off assistant", "mute", "stop"]
    help_words = ["help", "what can i say", "commands", "how to use"]

    # 1. Check for Stop / Sleep
    if contains_any(raw_command, stop_words):
        return jsonify({
            "success": True,
            "action": "sleep",
            "message": "Going to sleep. Say 'Hey GreenEdge' when you need me.",
            "is_active": False
        })

    # 2. Wake-up Detection & Command Extraction
    woke_up = contains_any(raw_command, wake_words)
    cmd = raw_command
    if woke_up:
        for w in sorted(wake_words, key=len, reverse=True):
            cmd = re.sub(r'\b' + re.escape(w) + r'\b', '', cmd).strip()

    # 3. Handle Sleeping State
    if not is_active:
        if woke_up:
            valid_intents = ["navigate", "navigation", "read", "scan", "summary", "summarize", "location", "where", "setting", "settings", "profile", "sos", "emergency", "home", "back", "login", "log in"]
            if not cmd or not contains_any(cmd, valid_intents):
                return jsonify({"success": True, "action": "activated", "message": "Hey User, welcome back. How may I help you?", "is_active": True})
            else:
                is_active = True 
        else:
            return jsonify({"success": True, "action": "ignored", "message": "", "is_active": False})
    else:
        if woke_up and not cmd:
            return jsonify({"success": True, "action": "activated", "message": "I am listening. What would you like to do?", "is_active": True})


    # ==========================================
    # 4. MULTI-TURN LOGIN FLOW (CONTEXT: /login)
    # ==========================================
    if current_page == "/login" and is_active:

        # --- NEW: TOUCH ID TRIGGER ---
        if contains_any(cmd, ["touch id", "fingerprint", "face id", "biometrics", "scan finger"]):
            session_state["step"] = "idle"
            return jsonify({
                "success": True, "action": "page_action", "target": "biometricBtn", 
                "message": "Activating device biometrics. Please place your finger on the sensor.", 
                "session_state": session_state, "is_active": False # Turn off mic so OS can take over
            }) 
        
        # A. Waiting for Username
        if step == "awaiting_username":
            # Format voice formatting quirks ("at" -> "@", "dot" -> ".")
            formatted_username = cmd.replace(" at ", "@").replace(" dot ", ".").replace(" ", "")
            session_state["temp_username"] = formatted_username
            session_state["step"] = "confirming_username"
            return jsonify({
                "success": True, "action": "speak_and_listen", 
                "message": f"You said {formatted_username}. Is that correct?", 
                "session_state": session_state, "is_active": True
            })
            
        # B. Confirming Username
        elif step == "confirming_username":
            if contains_any(cmd, ["yes", "yeah", "yep", "correct", "right", "it is"]):
                session_state["step"] = "awaiting_password"
                return jsonify({
                    "success": True, "action": "fill_and_listen", "target": "email", "val": session_state["temp_username"], 
                    "message": "Username confirmed. Now, please say or spell your password. CAUTION: Ensure no one else is around listening to you.", 
                    "session_state": session_state, "is_active": True
                })
            elif contains_any(cmd, ["no", "incorrect", "wrong", "change"]):
                session_state["step"] = "awaiting_username"
                return jsonify({
                    "success": True, "action": "speak_and_listen", 
                    "message": "Let's try again. What is your email or phone number?", 
                    "session_state": session_state, "is_active": True
                })
                
        # C. Waiting for Password
        elif step == "awaiting_password":
            formatted_password = cmd.replace(" ", "") # Remove spaces for passwords
            session_state["temp_password"] = formatted_password
            session_state["step"] = "confirming_password"
            return jsonify({
                "success": True, "action": "speak_and_listen", 
                "message": "Password recorded securely. Should I submit and log you in?", 
                "session_state": session_state, "is_active": True
            })
            
        # D. Confirming Password & Submit
        elif step == "confirming_password":
            if contains_any(cmd, ["yes", "yeah", "yep", "correct", "right", "log in", "login", "submit"]):
                session_state["step"] = "idle"
                return jsonify({
                    "success": True, "action": "fill_and_submit", "target": "password", "val": session_state["temp_password"], 
                    "message": "Logging you in now.", 
                    "session_state": session_state, "is_active": True
                })
            elif contains_any(cmd, ["no", "incorrect", "wrong", "change"]):
                session_state["step"] = "awaiting_password"
                return jsonify({
                    "success": True, "action": "speak_and_listen", 
                    "message": "Let's try again. Please say your password securely.", 
                    "session_state": session_state, "is_active": True
                })

        # E. Start the flow
        if contains_any(cmd, ["login", "log in", "sign in", "enter details", "start login", "fill form"]):
            session_state["step"] = "awaiting_username"
            return jsonify({
                "success": True, "action": "speak_and_listen", 
                "message": "Please say your email or phone number.", 
                "session_state": session_state, "is_active": True
            })


    # ==========================================
    # 5. GLOBAL COMMANDS
    # ==========================================
    if contains_any(cmd, help_words):
        return jsonify({"success": True, "action": "speak_only", "message": "You can say: open navigation, read document, summarize document, where am I, emergency SOS, go home, or go back.", "is_active": True})

    if contains_any(cmd, ["go back", "back", "previous screen", "return"]):
        return jsonify({"success": True, "action": "history_back", "message": "Going back.", "is_active": True})

    if contains_any(cmd, ["home", "dashboard", "main menu"]):
        return jsonify({"success": True, "action": "navigate", "url": "/home", "message": "Opening Home dashboard.", "is_active": True})

    if contains_any(cmd, ["navigation", "smart navigation", "start walking", "navigate"]):
        return jsonify({"success": True, "action": "navigate", "url": "/Snavigation", "message": "Opening smart navigation.", "is_active": True})

    if contains_any(cmd, ["read document", "document reader", "scanner", "scan text"]):
        return jsonify({"success": True, "action": "navigate", "url": "/documentR", "message": "Opening document reader.", "is_active": True})

    if contains_any(cmd, ["summary", "document summary", "summarize"]):
        return jsonify({"success": True, "action": "navigate", "url": "/documentS", "message": "Opening document summary.", "is_active": True})

    if contains_any(cmd, ["location", "where am i", "my location", "gps"]):
        return jsonify({"success": True, "action": "navigate", "url": "/location", "message": "Fetching your walking location.", "is_active": True})

    if contains_any(cmd, ["settings", "setting", "preferences", "app settings"]):
        return jsonify({"success": True, "action": "navigate", "url": "/setting", "message": "Opening settings.", "is_active": True})

    if contains_any(cmd, ["profile", "my account", "user profile"]):
        return jsonify({"success": True, "action": "navigate", "url": "/profile", "message": "Opening profile.", "is_active": True})

    if contains_any(cmd, ["sos", "emergency", "help me", "danger", "trigger sos", "sound siren"]):
        if current_page == "/sos":
            return jsonify({"success": True, "action": "page_action", "target": "sosBtn", "message": "Triggering SOS.", "is_active": True})
        return jsonify({"success": True, "action": "navigate", "url": "/sos", "message": "Opening emergency SOS.", "is_active": True})

    if contains_any(cmd, ["call guardian", "call mother", "make a call", "call contact", "dial"]):
        if current_page == "/sos":
            return jsonify({"success": True, "action": "page_action", "target": "callBtn", "message": "Calling your emergency contact.", "is_active": True})
        return jsonify({"success": True, "action": "navigate", "url": "/sos", "message": "Opening emergency SOS to make a call.", "is_active": True})

    if contains_any(cmd, ["scan", "take photo", "capture", "scan document"]):
        return jsonify({"success": True, "action": "page_action", "target": "scanBtn", "message": "Opening camera.", "is_active": True})

    if contains_any(cmd, ["upload", "gallery", "choose file", "upload document", "upload from gallery"]):
        return jsonify({"success": True, "action": "page_action", "target": "uploadBtn", "message": "Opening file browser.", "is_active": True})

    if contains_any(cmd, ["read aloud", "read text", "play audio", "listen", "read it"]):
        return jsonify({"success": True, "action": "page_action", "target": "readAloudBtn", "message": "Reading extracted text.", "is_active": True})

    return jsonify({
        "success": True,
        "action": "unknown",
        "message": "Sorry, I didn't recognize that command.",
        "is_active": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 
