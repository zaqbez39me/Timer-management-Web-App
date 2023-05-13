<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <header class="header">
            <div class="wrapper">
                <div class="header__wrapper" style="padding-top: 116px">
                    <div class="header__logo">
                        <a href="3.html" class="header__logo-link">
                            <img src="./img/svg/countdown-timers.svg" alt="countdown timers">
                        </a>
                    </div>
                </div>
            </div>
        </header>
        <main class="main">
            <div class="container">
                <div class="logreg-box">
                    <h1 class="logreg" id="title">Register</h1>
                    <form action="auth/register" method="post">
                        <div class="input-group">
                            <div class="input-field" id="nameField">
                                <input class="ilogreg" type="text" id="name" placeholder="Username" name="username">
                            </div>
                            <div class="input-field">
                                <input class="ilogreg" type="password" id="pass" placeholder="Password" name="password">
                            </div>
                            <div class="input-field" id="cPass">
                                <input class="ilogreg" type="password" id="secPass" placeholder="Confirm Password">
                            </div>
                            <div class="error-field1" id="error1">
                                <p class="errreg" id="diffPass-problem">Different passwords or Username is incorrect</p>
                            </div>
                            <div class="error-field1" id="error2">
                                <p class="errlog" id="incorrect-data">Incorrect name or password</p>
                            </div>
                        </div>
                        <div class="btn-field">
                            <button type="button" id="rBtn">Register</button>
                            <button type="button" class="disable" id="lBtn">Login</button>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    <script src="script_1.js">

    </script>
    </body>
</html>
