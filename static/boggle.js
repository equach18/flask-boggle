class BoggleGame{
    constructor(seconds = 60){
        this.words = new Set();
        this.score = 0;
        this.seconds = seconds;

        this.startCountdown = this.startCountdown.bind(this)
        this.gameTimer = setInterval(this.startCountdown, 1000)

        this.submitHandler = this.submitHandler.bind(this)
        $("form").on("submit", this.submitHandler)
    }

    alertUser(message){
        //alerts user with the message 
        $("#message").html('');
        $("#message").append(message);
    }

    updateScore(word){
        this.score += word.length;
        $("#score").html('');
        $("#score").text(this.score);
    }

    updateTime(){
        $("#timer").html('');
        $("#timer").text(this.seconds);
    }

    async startCountdown(){
        this.updateTime();
        this.seconds --;
        if(this.seconds == 0){
            this.updateTime();
            clearInterval(this.gameTimer);
            await this.endGame()
        }
    }

    async endGame(){
        $("form").hide();
        $("#end-game").text("Score Recorded! Thank you for playing.");
        const res = await axios.post("/plays", {score: this.score})
        console.log(res.data)
        
        if (res.data.new_highscore){
            this.alertUser(`New highscore! ${this.score} points`)
        }
        else{
            this.alertUser(`You scored ${this.score} points. Thanks for playing!`)
        }
    }


    async submitHandler(e){
        // handles word submitted by the player
        e.preventDefault();
        const word = $("#word").val();
        
        const res = await axios.get("/check-word", {params: {word: word}});
        const validity = res.data.result;

        if (validity === "ok" && this.words.has(word) === false){
            this.alertUser(`${word} is valid!`);
            this.words.add(word);
            this.updateScore(word);
        }
        else if(this.words.has(word)){
            this.alertUser(`${word} has already been counted.`)
        }
        else if(validity === "not-on-board"){
            this.alertUser(`Invalid: ${word} is not on the board.`);
        }
        else if(validity === "not-word"){
            this.alertUser(`Invalid: ${word} is not a word.`);
        }
        $("form")[0].reset()
    }
}