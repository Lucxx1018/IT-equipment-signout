document.addEventListener("DOMContentLoaded", () => {
    let formName = document.getElementById("name");
    let formEquipment = document.getElementById("equipment-select");
    let signatureCanvas = document.getElementById("signatureCanvas");
    let signatureButton = document.getElementById("signatureButton");
    const signaturePad = new SignaturePad(signatureCanvas);
    signaturePad.clear();

    signatureButton.addEventListener('click', async (event) => {
        let dataUri = signaturePad.toDataURL("image/svg+xml");
        let signatureData = JSON.stringify(dataUri);
        let name = formName.value;
        let equipment = formEquipment.value;
        let formData = JSON.stringify([name, equipment]);
        let payload = JSON.stringify([formData, signatureData]);
        console.log(payload);
        try {
            response = await fetch('/', {
                method: 'POST',
                body: payload,
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            console.log(await response)
        } catch (err) {
            console.log("Error: ", err)
        }
    });
})
