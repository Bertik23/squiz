<svelte:head>
    <title>Playing - 7 second quiz</title>
</svelte:head>
<div>
<h1>Seven second quiz</h1>
<a class=home-link href="/" on:click="{send(-1)}">Home</a>

{#if game}
    <h2>Time remaining: {timeLeft}</h2>
    <table>
        {#each quiz as row, x}
        <tr>
            {#each row as letter, y}
            <td><button class="letter" on:click|preventDefault="{send(x*row.length + y)}">{letter}</button></td>
            {/each}
        </tr>
        {/each}
    </table>
{:else}
    <h3>{result}</h3>
    <button on:click|preventDefault="{playGame}">Next game</button>
{/if}
{#if !$isGuest}
<PlayerStats user={$username}/>
{/if}
</div>
<script lang="ts">
    import { username, isGuest } from "../stores"
    import PlayerStats from "../components/playerStats.svelte"

    let game = true;
    let result = "";
    let gameId;
    let timeLeft = 7
    let quiz = [[]];
    let quizStr = "";

    const sleep = (milliseconds) => {
        return new Promise(resolve => setTimeout(resolve, milliseconds))
    }

    async function getData() {
        const response = await fetch("http://localhost:5000/getQuiz")
        const data = await response.json()
        // console.log(response)
        // console.log(data)

        quiz = data.game
        quizStr = data.game_str
        gameId = data.id
    }

    async function waitAndSend() {
        while (timeLeft > 0){
            await sleep(1000);
            timeLeft -= 1;
        }
        if (timeLeft == 0){
            send(-1)
        }
    }

    async function _send(index){
        // console.log("_sending!!!")
        let params = ""
        if (gameId === undefined){
            // console.log("Not _sending")
            return
        }
        if (!$isGuest){
            params += `&username=${$username}`
        }
        const response = await fetch(`http://localhost:5000/submitQuiz?id=${gameId}&differentIndex=${index}`+params)
        const data = await response.json()
        // console.log(data);
        result = data.correct ? "Correct!" : "Wrong"
        game = false;
    }

    function send(index): any{
        if (gameId === undefined){
            // console.log("Not sending")
            return
        }
        timeLeft = -1;
        // console.log("sending!")
        _send(index)
    }

    function playGame(): any{
        timeLeft = 7;
        quiz = [[]];
        game = true;
        getData()
        waitAndSend()
    }

    // console.log(timeLeft)
    playGame()

</script>

<style>
    * {
        color: #BBB;
        font-size: 1.1rem;
    }

    h1 {
        font-size: 3rem;
    }
    div {
        display: grid;
        background-color: #000;
        height: 100%;
        justify-content: center;
        align-content: center;
    }

    a, a:visited, button{
        border: .2rem solid #20A020;
        margin: .3rem;
        padding: .4rem;
        border-radius: 1.1rem;
        background-color: #202020;
        text-decoration: none;
        transition: border-radius 0.3s cubic-bezier(0.65, 0, 0.35, 1)
    }

    label{
        font-size: 1.2rem;
    }

    .home-link{
        width: max-content;
        justify-self: center;
    }

    button:hover, a:hover{
        border-radius: .8rem;
    }

    .letter{
        width: 100%;
    }

    td{
        width: 2rem;
    }
</style>