<!DOCTYPE html>
<html lang="en">

<head>
    <?php include_once('functions.php'); ?>
    <?php if (isset($_GET['result'])) $jsonResult = json_decode($_GET['result']); ?>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Operations research</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <style>
        .fileContainer {
            overflow: hidden;
            position: relative;
        }

        .fileContainer [type=file] {
            cursor: inherit;
            display: block;
            font-size: 999px;
            filter: alpha(opacity=0);
            min-height: 100%;
            min-width: 100%;
            opacity: 0;
            position: absolute;
            right: 0;
            text-align: right;
            top: 0;
        }
    </style>

</head>

<body>
    <?php include_once('header.php'); ?>
    <div class="container-fluid shadow p-3 mb-5 bg-white rounded" style="margin-top: 70px; min-height: 110vh;">
        <div class="row">
            <div class="col-md-12" style="text-align:center">
                <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'ant') : ?>
                    <h3>Розв'язання мурашиним алгоритмом</h3>
                <?php endif ?>
                <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'genetic') : ?>
                    <h3>Розв'язання генетичним алгоритмом</h3>
                <?php endif ?>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12" style="text-align:center">
                <form method="POST" action="system/countAlgorithm.php">
                    <?php
                    $matrixSize = $_GET['matrixSize'];
                    $startMatrix = $jsonResult[3];
                    echo "<br>";
                    for ($i = 0; $i < $matrixSize; $i++) {
                        for ($j = 0; $j < $matrixSize; $j++) {
                            if ($i == $j || $i > $j) $disabled = 'disabled';
                            else $disabled = 'value="' . $startMatrix[$i][$j] . '"';
                            echo '<input type="text" class="randomFill" id="field' . $i . $j . '" name="field' . $i . $j . '" size="1" required ' . $disabled . '>';
                        }
                        echo '<br>';
                    }
                    ?>
                    <br>

                    <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'ant') : ?>
                        <input type="hidden" value="antAlgorithm.py" name="algorithm">
                    <?php endif ?>
                    <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'genetic') : ?>
                        <input type="hidden" value="geneticAlgorithm.py" name="algorithm">
                    <?php endif ?>

                    <input type="hidden" value="<?= $_GET['matrixSize'] ?>" name="matrixSize">
                    <input type="submit" class="btn btn-success" value="Розв'язати">
                </form>
                <br>
                <button class="btn btn-success" onclick="genRandom()">Випадкова генерація</button>
                <br><br>
                <form action="system/uploadAlgorithm.php" method="post" enctype="multipart/form-data">
                    <label class="btn btn-warning fileContainer">
                        Обрати файл
                        <input type="file" required name="matrixFile">
                    </label><br>

                    <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'ant') : ?>
                        <input type="hidden" value="antAlgorithm.py" name="algorithm">
                    <?php endif ?>
                    <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'genetic') : ?>
                        <input type="hidden" value="geneticAlgorithm.py" name="algorithm">
                    <?php endif ?>

                    <input type="hidden" value="<?= $_GET['matrixSize'] ?>" name="matrixSize">
                    <input type="submit" value="Розв'язати з файлу" class="btn btn-warning">
                </form>
            </div>
        </div>

        <?php if (isset($_GET['result'])) : ?>
            <div class="row">
                <div class="col-md-12" style="text-align:center">
                    <br>
                    <h3>Розв'язання:</h3>
                    <p>Витрачено часу: <?= $jsonResult[0] ?></p>
                    <p>Кількість тварин: <?= $jsonResult[1] ?></p>
                    <p>Шлях: <?php foreach ($jsonResult[2] as $way) { echo ($way + 1)." ";} ?></p>
                    <div id="canvas" style="height: 400px; width: 100%;"></div>
                    <a class="btn btn-warning" href="system/output.txt" download>Завантажити відповідь</a>
                </div>
            </div>
        <?php endif; ?>

    </div>
    <script src="js/jquery-3.3.1.slim.min.js"></script>
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script type="text/javascript" src="js/raphael.js"></script>
    <script type="text/javascript" src="js/dracula.min.js"></script>
    <script type="text/javascript">
        function genRandom() {
            $(function() {
                for (let i = 0; i < <?= $matrixSize ?>; i++) {
                    for (let j = i; j < <?= $matrixSize ?>; j++) {
                        if (i != j && j > i) {
                            let fieldName = '#field' + i.toString(10) + j.toString(10);
                            $(fieldName).val(Math.round(Math.random()));
                        }
                    }
                }
            });
        }
    </script>
    <script type="text/javascript">
        const g = new Dracula.Graph

        <?php for ($i = 0; $i < $_GET['matrixSize']; $i++) : ?>
            <?php for ($j = $i; $j < $_GET['matrixSize']; $j++) : ?>
                <?php if ($jsonResult[3][$i][$j] == 1 && $i != $j) : ?>
                    g.addEdge('<?= $i + 1 ?>', '<?= $j + 1 ?>',
                        <?php if (in_array($i, $jsonResult[2]) && in_array($j, $jsonResult[2])) : ?> {
                                style: {
                                    stroke: '#bfa',
                                    fill: '#56f',
                                    label: 'Label'
                                }
                            }
                        <?php endif; ?>
                    )
                <?php endif; ?>
            <?php endfor; ?>
        <?php endfor; ?>

        const layouter = new Dracula.Layout.Spring(g)

        const renderer = new Dracula.Renderer.Raphael('#canvas', g)

        renderer.draw()
    </script>
</body>

</html>