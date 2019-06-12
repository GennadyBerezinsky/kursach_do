<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Operations research</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
    <?php include_once('header.php'); ?>
    <div class="container-fluid shadow p-3 mb-5 bg-white rounded" style="margin-top: 70px">
        <div class="row">
            <div class="col-md-12" style="text-align:center">

                <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'ant') : ?>
                    <h3>Мурашиний алгоритм</h3>
                <?php endif ?>
                <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'genetic') : ?>
                    <h3>Генетичний алгоритм</h3>
                <?php endif ?>

            </div>
            <div class="col-md-1"></div>
            <div class="col-md-10 shadow p-3 mb-5 bg-white rounded" style="margin-top:30px;">
                <div class="row">
                    <div class="col-md-12">

                        <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'ant') : ?>
                            <?php include_once('antDescription.php'); ?>
                        <?php endif ?>
                        <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'genetic') : ?>
                            <?php include_once('geneticDescription.php'); ?>
                        <?php endif ?>

                    </div>
                    <div class="col-md-12" style="margin-top:20px;">
                        <form action="example.php" mathod="GET">

                            <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'ant') : ?>
                                <input type="hidden" value="ant" name="algorithm">
                            <?php endif ?>
                            <?php if (isset($_GET['algorithm']) && $_GET['algorithm'] == 'genetic') : ?>
                                <input type="hidden" value="genetic" name="algorithm">
                            <?php endif ?>

                            <button type="submit" class="btn btn-primary">Розв'язати приклад</button>
                            <select name="matrixSize">
                                <?php for ($i = 3; $i <= 20; $i++) : ?>
                                    <option value="<?= $i ?>"><?= $i ?></option>
                                <?php endfor; ?>
                            </select>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-md-1"></div>
        </div>
    </div>
    <script src="js/jquery-3.3.1.slim.min.js"></script>
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
</body>

</html>