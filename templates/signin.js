document.addEventListener("DOMContentLoaded", () => {
    let formName = document.getElementById("name");
    let formEquipment = document.getElementById("equipment-select");
    let signatureButton = document.getElementById("signatureButton");

    signatureButton.addEventListener('click', async (event) => {
            let payload = JSON.stringify({ name: formName.value, equipment: formEquipment.value });
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
