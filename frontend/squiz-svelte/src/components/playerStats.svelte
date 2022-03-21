<script lang="ts">
    export let user;

    let avgTime = 0;
    let successRate = 0;
    let rawData = []

    async function getData() {
        const response = await fetch(`http://localhost:5000/getUser/${user}`)
        const data = await response.json()
        // console.log(response)
        // console.log(data)

        avgTime = data.average_time
        successRate = data.success_rate
        rawData = data.raw_data
    }

    getData()
</script>

<div>
<h2>{user}</h2>
<table>
    <tr>
    <td>Average time</td>
    <td>{avgTime}</td>
    </tr>
    <tr>
    <td>Success rate</td>
    <td>{successRate.toPrecision(3)}</td>
    </tr>
    <tr>
    <td>Games</td>
    <td>{rawData.length}</td>
</tr>
</table>
</div>

<style lang="css">
    div{
        margin-top: 2rem;
        display: grid;
        justify-items: center;
    }

    table{
        width: 50%;
    }

    td{
        text-align: center;
    }
</style>