let signatureButton = document.getElementById("signatureButton")
document.getElementById("signatureCanvas");
const signaturePad = new SignaturePad(canvas);
signatureButton.addEventListner('click', () => {
    let dataUri = signaturePad.toDataURL(...);
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'

        },
        body: JSON.stringify({ dataUri })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});