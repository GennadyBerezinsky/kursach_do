<?php

if ($_POST['algorithm'] == 'antAlgorithm.py') $type = 0;
else $type = 1;

include_once('../functions.php');
$link = dbConnect();

$matrixSize = $_POST['matrixSize'];

$line = '';
for ($i = 0; $i < $matrixSize; $i++) {
    for ($j = 0; $j < $matrixSize; $j++) {
        $line .= $_POST['field' . $i . $j];
    }
}

$output = shell_exec('python3 python/' . $_POST['algorithm'] . ' ' . $line . ' ' . $matrixSize);
$fd = fopen("output.txt", 'w') or die("не удалось создать файл");
fwrite($fd, $output);
fclose($fd);

$jsonResult = json_decode($output);

$sql = "INSERT INTO `algorithmInfo` (`id`, `time`, `animals`, `matrixSize`, `type`) VALUES (NULL, '" . $jsonResult['0'] . "', '" . $jsonResult[1] . "', '$matrixSize', '$type');";
mysqli_query($link, $sql);

if ($_POST['algorithm'] == 'antAlgorithm.py') header("Location: ../example.php?algorithm=ant&matrixSize=$matrixSize&result=$output");
else header("Location: ../example.php?algorithm=genetic&matrixSize=$matrixSize&result=$output");
