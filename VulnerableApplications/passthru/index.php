<!DOCTYPE html>
<html>
<head>
    <title>System Uptime</title>
</head>
<body>

    <h2>System Uptime</h2>

    <form method="post" action="">
        <label for="command">Enter Command:</label>
        <input type="text" name="command" id="command" required>
        <input type="submit" value="Run">
    </form>

    <?php
    if (isset($_POST["command"])) {
        $command = $_POST["command"];
        // Vulnerable to command injection
        echo "<h3>Command Results:</h3>";
        echo "<pre>";
        passthru($command);
        echo "</pre>";
    }
    ?>

</body>
</html>
