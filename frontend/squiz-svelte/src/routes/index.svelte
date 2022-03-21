<svelte:head>
    <title>7 second quiz</title>
</svelte:head>

<script lang="ts">
    import { username, isGuest } from "../stores.ts"

    function notGuest(){
        isGuest.set(false)
    }

    function yesGuest(){
        isGuest.set(true)
    }

    function canPlay(){
        return $username != ''
    }
</script>

<div>
<div class="wrapper">
<h1>Welcome to 7 second quiz</h1>
<div class="content">
<label for=username>Username</label>
<input name="username" bind:value={$username}>

<div class="play-buttons-container">
<a on:click="{notGuest}" href="/game" class:disabled="{$username == ''}">Play</a>
<a on:click="{yesGuest}" href="/game">Play as guest</a>
</div>
</div>
</div>
</div>

<style lang="css">
    * {
        color: #BBB;
        font-size: 1.1rem;
    }

    .disabled{
        pointer-events:none
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

    .play-buttons-container{
        display: grid;
        grid-template-columns: 1fr 1fr;
        width: 100%;
        justify-items: center;
    }

    a, a:visited, input{
        border: .2rem solid #20A020;
        margin: .3rem;
        padding: .4rem;
        border-radius: 1.1rem;
        background-color: #202020;
        text-decoration: none;
        transition: border-radius 0.3s cubic-bezier(0.65, 0, 0.35, 1)
    }

    a.disabled{
        border-color: #502020;
        color: #888;
        background-color: #151515;
    }

    label{
        font-size: 1.2rem;
    }

    .wrapper{
        width: 120%;
        justify-self: center;
        justify-items: center;
        display: grid;
        grid-template-columns: 100%;
    }

    .content{
        /* width: calc(max-content + 5%); */
        width: 60%;
        display: grid;
        grid-template-columns: 100%;
        justify-self: center;
    }

    a:hover{
        border-radius: .8rem;
    }
</style>
