document.addEventListener("DOMContentLoaded", () => {
    let formName = document.getElementById("name");
    let formEquipment = document.getElementById("equipment-select");
    let signatureCanvas = document.getElementById("signatureCanvas");

    let signaturePad;
    if (signatureCanvas !== null) {
        signaturePad = new SignaturePad(signatureCanvas);
        signaturePad.clear();
    } 

    let confirmButton = document.getElementById("confirmButton");
    confirmButton.addEventListener('click', async () => {
        let payload;
        if (signatureCanvas === null) {
            payload = JSON.stringify({ name: formName.value, equipment: formEquipment.value });
        } else {
            let dataUri = signaturePad.toDataURL("image/svg+xml");
            let signatureData = JSON.stringify(dataUri);
            payload = JSON.stringify({ name: formName.value, equipment: formEquipment.value, signature: signatureData });
        }

        try {
            response = await fetch(window.location, {
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
