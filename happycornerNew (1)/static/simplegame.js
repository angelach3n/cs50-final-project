document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('ballGameCanvas');
    const ctx = canvas.getContext('2d');

    const paddleWidth = 10;
    const paddleHeight = 60;
    const ballSize = 12; // Increase the size of the ball

    let xPaddle = 0;
    let yPaddle = canvas.height / 2 - paddleHeight / 2;

    let xBall = canvas.width / 2;
    let yBall = canvas.height / 2;
    let xBallSpeed = 8;
    let yBallSpeed = 6;

    let score = 0;

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawPaddle(xPaddle, yPaddle);
        drawBall(xBall, yBall);
        drawScore();

        // Check for collisions more frequently by dividing the frame into steps
        const steps = 5;
        for (let i = 0; i < steps; i++) {
            xBall += xBallSpeed / steps;
            yBall += yBallSpeed / steps;

            // Ball and wall collision
            if (xBall + ballSize > canvas.width || xBall - ballSize < 0) {
                xBallSpeed = -xBallSpeed;
            }

            if (yBall + ballSize > canvas.height || yBall - ballSize < 0) {
                yBallSpeed = -yBallSpeed;
            }

            // Ball and paddle collision
            if (
                (xBall - ballSize < xPaddle + paddleWidth) &&
                (yBall + ballSize > yPaddle) &&
                (yBall - ballSize < yPaddle + paddleHeight)
            ) {
                xBallSpeed = -xBallSpeed;
                increaseScore();
            }
        }

        requestAnimationFrame(draw);
    }

    function drawPaddle(x, y) {
        ctx.fillRect(x, y, paddleWidth, paddleHeight);
    }

    function drawBall(x, y) {
        ctx.beginPath();
        ctx.arc(x, y, ballSize, 0, Math.PI * 2);
        ctx.fill();
        ctx.closePath();
    }

    function drawScore() {
        ctx.font = '20px "Arial", sans-serif';
        ctx.fillStyle = '#000'; // Black color
        ctx.fillText('Score: ' + score, 10, 30);
    }

    function increaseScore() {
        score++;
    }

    // Controls
    document.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowUp' && yPaddle > 0) {
            yPaddle -= 10;
        } else if (event.key === 'ArrowDown' && yPaddle + paddleHeight < canvas.height) {
            yPaddle += 10;
        }
    });

    draw();
});
