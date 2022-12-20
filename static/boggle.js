$game = $('#game')
$userGuess = $('#guess');
$endGame = $('#end-game');

$game.hide()
$endGame.hide()
score = 0;

class BoggleGame{
    static startGame(){
        //show game board
        $game.show()
        $('#rules').hide()

        //start game timer
        setTimeout(BoggleGame.gameTimerEnd, 60000)
    }

    static async handleGuess(evt){
        //prevent page from refreshing
        evt.preventDefault();
    
        // store users guess in a variable
        const guess = $userGuess.val();
    
        //clear the value for guess input
        $userGuess.val('');
    
        //make axios request to the server
        const resp = await axios.get('/check', {
            params: { 'guess': guess }
        })
    
        //use server response to flash message to user
        $('.guess-message').text(`${guess} is ${resp.data.result}`)
    
        if(resp.data.result == 'ok'){
            score += guess.length
            $('#current-score').text(score)
            $('#found-words-list').append(`<li>${guess}</li>`)
        }
    }

    static async gameTimerEnd(){
        //hide the submit guess form so user can't submit guesses
        $('#guess-form').hide()
        $endGame.show()

        //send request to server with high score
        axios.get('/end-game', {params: {'score': score }})
    }
}

$('#start-button').click(BoggleGame.startGame);

$('#submit-guess').click(BoggleGame.handleGuess);