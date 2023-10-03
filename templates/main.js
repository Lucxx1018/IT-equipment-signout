document.addEventListener("DOMContentLoaded", () => {
    let signatureButton = document.getElementById("signatureButton")
    let signatureCanvas = document.getElementById("signatureCanvas");
    const signaturePad = new SignaturePad(signatureCanvas);

    signatureButton.addEventListener('click', async () => {
        let dataUri = signaturePad.toDataURL("image/svg+xml");

        try {
            response = await fetch('/process', {
                method: 'POST',
                body: JSON.stringify({ dataUri }),
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            console.log(await response.json())
        } catch (err) {
            console.log("Error: ", err)
        }
    });
})
