document.addEventListener("DOMContentLoaded", () => {
    let formName = document.getElementById("name");
    let formEquipment = document.getElementById("equipment-select");
    let signinFlag = false;
    try {
        let signatureCanvas = document.getElementById("signatureCanvas");
        const signaturePad = new SignaturePad(signatureCanvas);
        console.log("The pad got defined");
        signaturePad.clear();
    }
    catch (err) {
        console.log("Error: ", err, " , which probably means this is the signin page so we'll continue anyways.");
        let signinFlag = 1;
    }
    let signatureButton = document.getElementById("signatureButton");

    signatureButton.addEventListener('click', async (event) => {
        if (signinFlag == 1) {
            let payload = JSON.stringify({ name: formName.value, equipment: formEquipment.value});
        }
        else {
            console.log("DEBUG PRINT YIPPEEEE")
            let dataUri = signaturePad.toDataURL("image/svg+xml");
            let signatureData = JSON.stringify(dataUri);
            let payload = JSON.stringify({ name: formName.value, equipment: formEquipment.value, signature: signatureData });
        }
        try {
            response = await fetch('/', {
                method: 'POST',
                body: payload,
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            window.location = (await response.json()).redirect_to
        } catch (err) {
            console.log("Error: ", err)
        }
    });
})
