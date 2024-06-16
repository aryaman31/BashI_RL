<!DOCTYPE html>
<html>
<head>
    <title>DNS Lookup</title>
</head>
<body>

    <h2>DNS Lookup</h2>

    <form method="post" action="">
        <label for="domain">Enter Domain:</label>
        <input type="text" name="domain" id="domain" required>
        <input type="submit" value="Lookup">
    </form>

    <?php
    if (isset($_POST["domain"])) {
        $domain = $_POST["domain"];
        // Vulnerable to command injection
        $output = [];
        exec("nslookup " . $domain, $output);
        echo "<h3>DNS Lookup Results for $domain:</h3>";
        echo "<pre>" . implode("\n", $output) . "</pre>";
    }
    ?>

</body>
</html>
