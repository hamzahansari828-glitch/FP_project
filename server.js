const express = require("express");
const session = require("express-session");


const { spawn } = require("child_process");
const path = require("path");


const app = express();
const PORT = 3000;


// =====================================================
// MIDDLEWARE
// =====================================================

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(
    session({
        secret:
            process.env.SESSION_SECRET ||
            "greenedge-secret",

        resave: false,

        saveUninitialized: false,

        cookie: {
            httpOnly: true,
            maxAge: 1000 * 60 * 60
        }
    })
);

app.set("view engine", "ejs");

app.use(express.static("public"));


// =====================================================
// WHATSAPP CLOUD API
// =====================================================

async function sendWhatsAppMessage(
    to,
    templateName,
    languageCode = "en_US",
    parameters = []
) {

    const url =
        `https://graph.facebook.com/v25.0/${process.env.WHATSAPP_PHONE_NUMBER_ID}/messages`;

    const cleanNumber =
        String(to).replace(/\D/g, "");

    const requestBody = {

        messaging_product: "whatsapp",

        to: cleanNumber,

        type: "template",

        template: {

            name: templateName,

            language: {
                code: languageCode
            }
        }
    };


    // -----------------------------------------
    // TEMPLATE PARAMETERS
    // -----------------------------------------

    if (parameters.length > 0) {

        requestBody.template.components = [

            {
                type: "body",

                parameters:
                    parameters.map(value => ({

                        type: "text",

                        text: String(value)

                    }))
            }

        ];
    }


    console.log(
        "📤 WhatsApp Message Request:",
        JSON.stringify(requestBody, null, 2)
    );


    const response = await fetch(
        url,
        {
            method: "POST",

            headers: {

                "Authorization":
                    `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`,

                "Content-Type":
                    "application/json"
            },

            body:
                JSON.stringify(requestBody)
        }
    );


    const data =
        await response.json();


    console.log(
        "📩 WhatsApp Message Response:",
        JSON.stringify(data, null, 2)
    );


    if (!response.ok) {

        throw new Error(
            data?.error?.message ||
            "WhatsApp message failed."
        );
    }


    return data;
}


// =====================================================
// WHATSAPP LOCATION API
// =====================================================

// async function sendWhatsAppLocation(to, latitude, longitude) {

//     const url =
//         `https://graph.facebook.com/v25.0/${process.env.WHATSAPP_PHONE_NUMBER_ID}/messages`;

//     const cleanNumber =
//         String(to).replace(/\D/g, "");

//     const lat = Number(latitude);
//     const lng = Number(longitude);

//     if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
//         throw new Error("Invalid latitude or longitude.");
//     }

//     const requestBody = {
//         messaging_product: "whatsapp",
//         to: cleanNumber,
//         type: "location",
//         location: {
//             latitude: lat,
//             longitude: lng,
//             name: "Emergency Location",
//             address: "Current SOS Location"
//         }
//     };

//     console.log(
//         "📍 WhatsApp Location Request:",
//         JSON.stringify(requestBody, null, 2)
//     );

//     const response = await fetch(url, {
//         method: "POST",

//         headers: {
//             Authorization:
//                 `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`,

//             "Content-Type":
//                 "application/json"
//         },

//         body:
//             JSON.stringify(requestBody)
//     });

//     const data =
//         await response.json();

//     console.log(
//         "📍 WhatsApp Location Response:",
//         JSON.stringify(data, null, 2)
//     );

//     if (!response.ok) {

//         throw new Error(
//             data?.error?.message ||
//             "WhatsApp location message failed."
//         );
//     }

//     return data;
// }



async function sendWhatsAppLocation(to, latitude, longitude) {

    const url =
        `https://graph.facebook.com/v25.0/${process.env.WHATSAPP_PHONE_NUMBER_ID}/messages`;

    const cleanNumber =
        String(to).replace(/\D/g, "");

    const lat = Number(latitude);
    const lng = Number(longitude);

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
        throw new Error("Invalid latitude or longitude.");
    }

    const requestBody = {
        messaging_product: "whatsapp",
        to: cleanNumber,
        type: "location",
        location: {
            latitude: lat,
            longitude: lng,
            name: "Emergency Location",
            address: "Current SOS Location"
        }
    };

    console.log(
        "📍 LOCATION REQUEST:",
        JSON.stringify(requestBody, null, 2)
    );

    const response = await fetch(url, {
        method: "POST",

        headers: {
            Authorization:
                `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`,

            "Content-Type":
                "application/json"
        },

        body: JSON.stringify(requestBody)
    });

    const data = await response.json();

    console.log(
        "📍 LOCATION API RESPONSE:",
        JSON.stringify(data, null, 2)
    );

    if (!response.ok) {
        throw new Error(
            data?.error?.message ||
            "WhatsApp location failed."
        );
    }

    return data;
}



// =====================================================
// NORMALIZE INDIAN PHONE NUMBER
// =====================================================

function normalizeIndianNumber(phone) {

    let cleanPhone =
        String(phone || "")
            .replace(/\D/g, "");


    // -----------------------------------------
    // 10 digit Indian number
    // 9503791496
    //        ↓
    // 919503791496
    // -----------------------------------------

    if (cleanPhone.length === 10) {

        return "91" + cleanPhone;
    }


    // -----------------------------------------
    // 11 digit number starting with 0
    // 09503791496
    //        ↓
    // 919503791496
    // -----------------------------------------

    if (
        cleanPhone.length === 11 &&
        cleanPhone.startsWith("0")
    ) {

        return "91" + cleanPhone.substring(1);
    }


    // -----------------------------------------
    // Already has 91
    // -----------------------------------------

    if (
        cleanPhone.length === 12 &&
        cleanPhone.startsWith("91")
    ) {

        return cleanPhone;
    }


    // -----------------------------------------
    // Other international number
    // -----------------------------------------

    return cleanPhone;
}


// =====================================================
// TEST WHATSAPP
// =====================================================

app.get(
    "/test-whatsapp",
    async (req, res) => {

        try {

            // -----------------------------------------
            // TEST NUMBER
            // -----------------------------------------

            const testNumber =
                "919503791496";


            const result =
                await sendWhatsAppMessage(
                    testNumber,
                    "hello_world",
                    "en_US"
                );


            console.log(
                "✅ Test WhatsApp message sent."
            );


            return res.json({

                success: true,

                message:
                    "WhatsApp message sent successfully.",

                result:
                    result
            });

        }
        catch (error) {

            console.error(
                "❌ Test WhatsApp failed:",
                error
            );


            return res.status(500).json({

                success: false,

                message:
                    error.message
            });
        }
    }
);


// =====================================================
// HOME / PUBLIC ROUTES
// =====================================================

app.get(
    "/",
    (req, res) => {

        res.render("splash");
    }
);


app.get(
    "/login",
    (req, res) => {

        res.render("login");
    }
);

app.get(
    "/home",
    (req, res) => {
        res.render("home");
    }
    
);



// =====================================================
// LOGIN
// =====================================================



// =====================================================
// VERIFY OTP
// =====================================================

app.get(
    "/verify-otp",
    (req, res) => {

        res.render(
            "verify-otp"
        );
    }
);




// =====================================================
// RESET PASSWORD
// =====================================================

app.get(
    "/reset-password",
    (req, res) => {

        if (
            !req.session.otpVerified ||
            !req.session.resetUserId
        ) {

            return res.redirect(
                "/forgot-password"
            );
        }


        res.render(
            "reset-password"
        );
    }
);




// =====================================================
// REGISTER
// =====================================================

app.get(
    "/register",
    (req, res) => {

        res.render(
            "register"
        );
    }
);





// =====================================================
// NAVIGATION & UI PAGES
// =====================================================

app.get(
    "/setting",
    (req, res) => {

        res.render("setting");
    }
);


app.get(
    "/navigate",
    (req, res) => {

        res.render("navigate");
    }
);


app.get(
    "/profile",
    (req, res) => {

        res.render("profile");
    }
);


app.get(
    "/Snavigation",
    (req, res) => {

        res.render("Snavigation");
    }
);


app.get(
    "/documentR",
    (req, res) => {

        res.render("documentR");
    }
);


app.get(
    "/documentS",
    (req, res) => {

        res.render("documentS");
    }
);


app.get(
    "/navigate6",
    (req, res) => {

        res.render("navigate6");
    }
);


// =====================================================
// SOS PAGE
// =====================================================

app.get("/sos",(req, res) => {
    res.render("sos");

});


// =====================================================
// GET EMERGENCY CONTACT
// =====================================================

app.get(
    "/api/emergency-contact",
    (req, res) => {  

        if (!req.session.userId) {

            return res.status(401).json({

                success: false,

                message:
                    "Please login first."
            });
        }


        const sql =
            "SELECT name, guardian_phone FROM users WHERE id = ?";


        mysql.query(
            sql,

            [
                req.session.userId
            ],

            (err, results) => {

                if (err) {

                    console.error(
                        "Emergency contact DB error:",
                        err
                    );

                    return res.status(500).json({

                        success: false,

                        message:
                            "Database error."
                    });
                }


                if (
                    results.length === 0
                ) {

                    return res.status(404).json({

                        success: false,

                        message:
                            "User not found."
                    });
                }


                const user =
                    results[0];


                const guardianPhone =
                    String(
                        user.guardian_phone ||
                        ""
                    ).trim();


                if (!guardianPhone) {

                    return res.status(404).json({

                        success: false,

                        message:
                            "Emergency contact not found."
                    });
                }


                return res.json({

                    success: true,

                    guardianName:
                        user.name,

                    guardianPhone:
                        guardianPhone
                });
            }
        );
    }
);


// =====================================================
// SOS API
// =====================================================



// =====================================================
// PYTHON NAVIGATION
// =====================================================

app.get(
    "/location",
    (req, res) => {

        const pythonScriptPath =
            path.join(
                __dirname,
                "python",
                "navigation.py"
            );


        const python =
            spawn(
                "python",
                [
                    pythonScriptPath
                ]
            );


        python.stdout.on(
            "data",
            (data) => {

                console.log(
                    `Python Output: ${data}`
                );
            }
        );


        python.stderr.on(
            "data",
            (data) => {

                console.error(
                    `Python Error: ${data}`
                );
            }
        );


        python.on(
            "close",
            (code) => {

                console.log(
                    `Python exited with code ${code}`
                );
            }
        );


        return res.send(
            "Voice navigation started. Please speak your destination."
        );
    }
);



// ... (Keep all your existing routes for WhatsApp, OTP, and EJS pages)

// =====================================================
// VOICE ASSISTANT PROXY (NEW)
// =====================================================
app.post("/api/voice-command", async (req, res) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/voice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(req.body)
        });
        const data = await response.json();
        return res.json(data);
    } catch (err) {
        console.error("Flask Voice Server Error:", err.message);
        return res.status(502).json({
            success: false,
            message: "Voice assistant service is currently unreachable.",
            is_active: req.body.is_active || false
        });
    }
});

// =====================================================
// START SERVER
// =====================================================
app.listen(PORT, "0.0.0.0", () => {
    console.log(`🚀 Server running at http://localhost:${PORT}`);
}); 





