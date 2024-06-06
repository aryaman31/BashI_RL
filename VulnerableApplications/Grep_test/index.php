<!-- This file doesn't sanitise the user input and runs a shell command,
     hence has a command injection vulnerability 
    Vuln is 
        ; ls     

    -->

<!DOCTYPE html>
<html>
<head>
    <title>Grep test</title>
</head>
<body>

    <h2>Check if a word exists in the file!</h2>

    <form method="get" action="">
        <label for="search_text">Enter search term:</label>
        <input type="text" name="search_text" id="search_text" required>
        <input type="submit" value="Ping">
    </form>

    <?php
    if (isset($_GET["search_text"])) {
        $search_text = $_GET["search_text"];
        $search_result = shell_exec("grep " . $search_text . " lorem.txt");
        echo "<h3>Search Results for $search_text:</h3>";
        echo "<pre>$search_result</pre>";
    }
    ?>

</body>
</html>
