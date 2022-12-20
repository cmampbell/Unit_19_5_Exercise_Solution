$startButton = $('#start-button')
$rules = $('#rules')
$game = $('#game')
$userGuess = $('#guess');
$guessForm = $('#guess-form')
$submitGuess = $('.submit-guess');
$currentScore = $('#current-score');
$guessMessage = $('.guess-message');
$endGame = $('#end-game');
$playAgain = $('#play-again');

$game.hide()
$endGame.hide()
score = 0;

function startGame(){
    //show game board
    $game.show()
    $rules.hide()
    //start timer
    setTimeout(async function(){
        //hide the submit guess button
        $guessForm.hide()
        $endGame.show()

        //send request to server with high score
        axios.get('/end-game', {params: {'score': score }})
    }, 30000)
}

$startButton.click(startGame);

async function handleGuess(evt){
    //prevent page from refreshing
    evt.preventDefault();

    // store users guess in a variable
    guess = $userGuess.val();

    //clear the value for guess input
    $userGuess.val('');

    //make axios request to the server
    resp = await axios.get('/check', {
        params: { 'guess': guess }
    })

    console.log(resp)

    //use server response to flash message to user
    $guessMessage.text(`${guess} is ${resp.data.result}`)

    if(resp.data.result == 'ok'){
        score += guess.length
        $currentScore.text(score)
    }
}

$submitGuess.click(handleGuess);