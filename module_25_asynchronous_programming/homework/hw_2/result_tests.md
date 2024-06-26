<table>
    <tr>
        <th>Type requests</th>
        <th>10 cats</th>
        <th>50 cats</th>
        <th>100 cats</th>
    </tr>
    <tr>
        <th>Multiprocess'</th>
        <th>1.77</th>
        <th>5.09</th>
        <th>11.57</th>
    </tr>
    <tr>
        <th>Threads</th>
        <th>1.58</th>
        <th>1.18</th>
        <th>1.39</th>
    </tr>
    <tr>
        <th>aiohttp & blocking writer</th>
        <th>1.65</th>
        <th>1.65</th>
        <th>0.94</th>
</tr>
    <tr>
    <th>aiohttp & async writer</th>
    <th>1.07</th>
    <th>0.81</th>
    <th>2.00</th>
    </tr>
</table>

