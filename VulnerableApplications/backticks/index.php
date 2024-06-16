<!DOCTYPE html>
<html>
<head>
    <title>List Files</title>
</head>
<body>

    <h2>List Files</h2>

    <form method="post" action="">
        <label for="directory">Enter Directory:</label>
        <input type="text" name="directory" id="directory" required>
        <input type="submit" value="List Files">
    </form>

    <?php
    if (isset($_POST["directory"])) {
        $directory = $_POST["directory"];
        // Vulnerable to command injection
        $files = `ls -la $directory`;
        echo "<h3>Files in $directory:</h3>";
        echo "<pre>$files</pre>";
    }
    ?>

</body>
</html>
