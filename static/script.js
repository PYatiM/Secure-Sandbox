async function runCode() {
    const code = document.getElementById("codeInput").value;

    document.getElementById("stdout").textContent = "Running...";
    document.getElementById("stderr").textContent = "";
    document.getElementById("meta").textContent = "";

    const response = await fetch("/execute", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
    });

    const result = await response.json();

    document.getElementById("stdout").textContent = result.stdout || "";
    document.getElementById("stderr").textContent = result.stderr || "";

    document.getElementById("meta").textContent =
        "Return Code: " + result.returncode +
        "\nExecution Time: " + result.execution_time + "s";
}