function domyfunction(id) {
    console.log("results.js")
    console.log(id)
    var beers = id
    d3.json(`./beerinfo/${id}`).get(function (tableData) {

        console.log(tableData);
        var tbody = d3.select("#beers").select("tbody");
        columns = ["name", "ibu", "color", "abv", "attenuation_level", "tagline", "food_pairings"]
        // create a row for each object in the data
        var rows = tbody.selectAll("tr")
            .data(tableData)
            .enter()
            .append("tr");
        // create a cell in each row for each column
        var cells = rows.selectAll("td")
            .data(function (row) {
                return columns.map(function (column) {
                    return { column: column, value: row[column] };
                });
            })
            .enter()
            .append("td").text(function (d) { return d.value });
        
        console.log('done');



    });
}

