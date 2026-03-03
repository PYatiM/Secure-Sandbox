let editor;

require.config({ paths: { 'vs': 'https://unpkg.com/monaco-editor@0.44.0/min/vs' } });

require(['vs/editor/editor.main'], function () {
    editor = monaco.editor.create(document.getElementById('editor'), {
        value: "# Write Python code here\nprint('Hello Sandbox')",
        language: "python",
        theme: "vs-dark",
        automaticLayout: true
    });
});

async function runCode() {
    const status = document.getElementById("status");
    const code = editor.getValue(); 
    const userInput = document.getElementById("stdinInput").value; 
    
    status.textContent = "Running...";
    status.className = "status running";

    document.getElementById("stdout").textContent = "Running...";
    document.getElementById("stderr").textContent = "";
    document.getElementById("meta").textContent = "";

    try {
        const response = await fetch("/execute", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code, input: userInput })
        });

        const result = await response.json();

        // History
        const history = document.getElementById("history");
        const item = document.createElement("li");
        item.textContent =
            "Return: " + result.returncode +
            " | Time: " + result.execution_time + "s";
        history.prepend(item);

        // Output
        document.getElementById("stdout").textContent = result.stdout || "";
        document.getElementById("stderr").textContent = result.stderr || "";
        document.getElementById("meta").textContent =
            "Return Code: " + result.returncode +
            "\nExecution Time: " + result.execution_time + "s";

        if (result.returncode === 0) {
            status.textContent = "Execution Successful";
            status.className = "status success";
        } else {
            status.textContent = "Execution Failed";
            status.className = "status error";
        }

    } catch (error) {
        status.textContent = "Execution Error";
        status.className = "status error";
        document.getElementById("stderr").textContent = error.toString();
    }
}