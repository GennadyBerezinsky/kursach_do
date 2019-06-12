<?php

if ($_POST['algorithm'] == 'antAlgorithm.py') $type = 0;
else $type = 1;

include_once('../functions.php');
$link = dbConnect();

$uploadfile = basename('input.txt');

if (move_uploaded_file($_FILES['matrixFile']['tmp_name'], $uploadfile)) {
    $lines = file('input.txt');
    $matrixSize = count($lines);
    $line = '';
    for ($i = 0; $i < $matrixSize; $i++) {
        $lines[$i] = str_replace(", ", "", $lines[$i]);
        for ($j = $i; $j < $matrixSize; $j++) {
            if ($i != $j) $line .= $lines[$i][$j];
        }
    }
    $output = shell_exec('python3 python/' . $_POST['algorithm'] . ' ' . $line . ' ' . $matrixSize);

    $jsonResult = json_decode($output);

    $sql = "INSERT INTO `algorithmInfo` (`id`, `time`, `animals`, `matrixSize`, `type`) VALUES (NULL, '" . $jsonResult['0'] . "', '" . $jsonResult[1] . "', '$matrixSize', '$type');";
    mysqli_query($link, $sql);

    $fd = fopen("output.txt", 'w') or die("не удалось создать файл");
    fwrite($fd, $output);
    fclose($fd);
    if ($_POST['algorithm'] == 'antAlgorithm.py') header("Location: ../example.php?algorithm=ant&matrixSize=$matrixSize&result=$output");
    else header("Location: ../example.php?algorithm=genetic&matrixSize=$matrixSize&result=$output");
} else {
    echo "Возможная атака с помощью файловой загрузки!\n";
}
