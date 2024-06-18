<!DOCTYPE html>
<html>
<head>
    <title>Ping IP Address with Filtering</title>
</head>
<body>

    <h2>Ping IP Address</h2>

    <form method="post" action="">
        <label for="ip">Enter IP Address:</label>
        <input type="text" name="ip" id="ip" required>
        <input type="submit" name="ping" value="Ping">
    </form>

    <?php
    if (isset($_POST["ping"])) {
        $ip = $_POST["ip"];

        // Attempt to filter out dangerous characters
        $ip = str_replace(array(';', '&', '|', '`', '$', '>', '<'), '', $ip);

        // Vulnerable to command injection
        $cmd = shell_exec("ping -c 4 " . $ip);
        echo "<h3>Ping Results for $ip:</h3>";
        echo "<h3>Ping Results for" . $_POST["ping"] . ":</h3>";
        echo "<pre>$cmd</pre>";
    }
    ?>

</body>
</html>
