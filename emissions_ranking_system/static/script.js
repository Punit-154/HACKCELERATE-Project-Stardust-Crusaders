const debugLog = document.getElementById('debugLog');
function log(msg) {
    console.log(msg);
    debugLog.innerText += msg + "\n";
}

async function fetchRankings() {
    log("Fetching rankings...");
    try {
        const response = await fetch('/api/rankings/all');
        log("Response status: " + response.status);

        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }

        const data = await response.json();
        log("Data received. Status: " + data.status);

        if (data.status !== 'success') {
            throw new Error("API status not success: " + data.message);
        }

        document.getElementById('lastUpdate').innerText =
            data.last_update || "No data";

        // MATERIALS TABLE
        log("Rendering Materials: " + (data.materials ? data.materials.length : "undefined"));
        const materialsBody = document.querySelector('#materialsTable tbody');
        if (!materialsBody) throw new Error("Materials tbody not found");

        let matHtml = '';
        data.materials.forEach(item => {
            matHtml += `<tr>
                <td>${item.rank}</td>
                <td>${item.material}</td>
                <td>${Number(item.emissions).toFixed(2)}</td>
            </tr>`;
        });
        materialsBody.innerHTML = matHtml;

        // TRANSPORT TABLE
        log("Rendering Transport: " + (data.transport ? data.transport.length : "undefined"));
        const transportBody = document.querySelector('#transportTable tbody');
        if (!transportBody) throw new Error("Transport tbody not found");

        let transHtml = '';
        data.transport.forEach(item => {
            transHtml += `<tr>
                <td>${item.rank}</td>
                <td>${item.mode}</td>
                <td>${Number(item.emissions).toFixed(2)}</td>
            </tr>`;
        });
        transportBody.innerHTML = transHtml;

        log("Rendering complete.");

    } catch (error) {
        log("ERROR: " + error.message);
        document.getElementById('lastUpdate').innerText = "Error";
    }
}

// Load immediately
log("Script started.");
fetchRankings();

// Manual refresh button handler (if we had one)
// setInterval(fetchRankings, 5000); // Disabled auto-refresh to reduce noise
