async function encodeText() {
    const text = document.getElementById("text-input").value;
    const type = document.getElementById("method").value;

    const response = await fetch("/encode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, type })
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result || data.error;
}

async function decodeText() {
    const text = document.getElementById("text-input").value;
    const type = document.getElementById("method").value;

    const response = await fetch("/decode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, type })
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result || data.error;
}
