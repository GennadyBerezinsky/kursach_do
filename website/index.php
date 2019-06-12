<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Operations research</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <script src="js/Chart.min.js"></script>
    <?php

    include_once('functions.php');

    $link = dbConnect();

    $antsStatistic = mysqli_query($link, "SELECT AVG(time), matrixSize FROM `algorithmInfo` WHERE `type` = 0 GROUP BY `matrixSize`");
    $antCount = mysqli_num_rows(mysqli_query($link, "SELECT * FROM `algorithmInfo` WHERE `type` = 0 "));
    $geneticStatistic = mysqli_query($link, "SELECT AVG(time), matrixSize FROM `algorithmInfo` WHERE `type` = 1 GROUP BY `matrixSize`");
    $geneticCount = mysqli_num_rows(mysqli_query($link, "SELECT * FROM `algorithmInfo` WHERE `type` = 1 "));
    ?>
</head>

<body>
    <?php include_once('header.php'); ?>
    <div class="container-fluid shadow p-3 mb-5 bg-white rounded" style="margin-top: 70px">
        <div class="row">
            <div class="col-md-12" style="text-align:center">
                <h3>Загальна статистика</h3>
            </div>
            <div class="col-md-6" style="heigh: 100px">
                <h6 style="text-align:center">Мурашиний алгоритм запускався <?= $antCount ?> разів</h6>
                <canvas id="myChartAnt" width="100" height="100"></canvas>
            </div>
            <div class="col-md-6" style="heigh: 100px">
                <h6 style="text-align:center">Генетичний алгоритм запускався <?= $geneticCount ?> разів</h6>
                <canvas id="myChartGenetic" width="100" height="100"></canvas>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6" style="text-align:center">
                <canvas id="myChartTotal" width="100" height="100"></canvas>
            </div>
            <div class="col-md-6" style="text-align:center">
                <canvas id="myChartTotal1" width="100" height="100"></canvas>
            </div>
        </div>
    </div>
    <script src="js/jquery-3.3.1.slim.min.js"></script>
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script>
        var ctx = document.getElementById('myChartAnt').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [
                    <?php
                    foreach ($antsStatistic as $ant) {
                        echo "'n = " . $ant['matrixSize'] . "',";
                    }
                    ?>
                ],
                datasets: [{
                    label: 'Час',
                    data: [
                        <?php
                        foreach ($antsStatistic as $ant) {
                            echo $ant['AVG(time)'] . ",";
                        }
                        ?>
                    ],
                    backgroundColor: [
                        'rgba(83, 139, 213, 1)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    </script>
    <script>
        var ctx = document.getElementById('myChartGenetic').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [
                    <?php
                    foreach ($geneticStatistic as $genetic) {
                        echo "'n = " . $genetic['matrixSize'] . "',";
                    }
                    ?>
                ],
                datasets: [{
                    label: 'Час',
                    data: [
                        <?php
                        foreach ($geneticStatistic as $genetic) {
                            echo $genetic['AVG(time)'] . ",";
                        }
                        ?>
                    ],
                    backgroundColor: [
                        'rgba(213, 181, 83, 1)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }, ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    </script>
    <script>
        var ctx = document.getElementById('myChartTotal').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [
                    <?php
                    foreach ($antsStatistic as $ant) {
                        echo "'n = " . $ant['matrixSize'] . "',";
                    }
                    ?>
                ],
                datasets: [{
                        label: 'Час в мурашиному алгоритмі',
                        data: [
                            <?php
                            foreach ($antsStatistic as $ant) {
                                echo $ant['AVG(time)'] . ",";
                            }
                            ?>
                        ],
                        backgroundColor: [
                            'rgba(83, 139, 213, 1)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderWidth: 1
                    }, {
                        label: 'Час в генетичному алгоритмі',
                        data: [
                            <?php
                            foreach ($geneticStatistic as $genetic) {
                                echo $genetic['AVG(time)'] . ",";
                            }
                            ?>
                        ],
                        backgroundColor: [
                            'rgba(213, 181, 83, 1)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderWidth: 1
                    },

                ]
            },
            options: {

            }
        });
    </script>
    <script>
        var ctx = document.getElementById('myChartTotal1').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [
                    <?php
                    foreach ($antsStatistic as $ant) {
                        echo "'n = " . $ant['matrixSize'] . "',";
                    }
                    ?>
                ],
                datasets: [{
                        label: 'Час в мурашиному алгоритмі',
                        data: [
                            <?php
                            foreach ($antsStatistic as $ant) {
                                echo $ant['AVG(time)'] . ",";
                            }
                            ?>
                        ],
                        backgroundColor: [
                            'rgba(83, 139, 213, 1)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderWidth: 1
                    }, {
                        label: 'Час в генетичному алгоритмі',
                        data: [
                            <?php
                            foreach ($geneticStatistic as $genetic) {
                                echo $genetic['AVG(time)'] . ",";
                            }
                            ?>
                        ],
                        backgroundColor: [
                            'rgba(213, 181, 83, 1)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderWidth: 1
                    },

                ]
            },
            options: {

            }
        });
    </script>
</body>

</html>