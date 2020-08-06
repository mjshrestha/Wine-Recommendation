// created with the help of https://bl.ocks.org/adamjanes/6cf85a4fd79e122695ebde7d41fe327f

console.log("HELLO!", svg)

//creating svg
var svg = d3.select("svg"),
    margin = {top: 20, right: 90, bottom: 10, left: 100},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

//adding tooltip
var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-5, 0])
    .direction('n')
    .html(function(d) {
		 if (typeof d.no_of_wineries !== 'undefined') {
        return "Country: " + Wine.get(d.id).country +
            "<br/>No. of wineries: " + d.no_of_wineries +
            "<br/>Popular winery: " + Wine.get(d.id).winery +
            "<br/>Popular wine: " + Wine.get(d.id).best_wine_with_low_price +
            "<br/>Wine variety of Popular wine: " + Wine.get(d.id).best_wine_variety +
            "</br>Price of Popular wine: " +"$"+ Wine.get(d.id).best_wine_price ;
		 }
    });

var Country_id = d3.map(),
    Wine = d3.map();
    //path = d3.geoPath();

//linear scale for placemect positions
var x = d3.scaleLinear()
    .domain([1, 10])
    .rangeRound([20, 100]);

//color scale
var color = d3.scaleThreshold()
    .domain([1,3,15,30,200,350,500,3000,6000])
    .range(['#fcfbfd','#dadaeb','#bcbddc','#9e9ac8','#807dba','#6a51a3','#54278f','#3f007d', '#0a005b']);

//console.log(color.domain());

// Legend
var g = svg.append("g")
    .attr("class", "legendThreshold")
    .attr("transform", "translate(20,20)");
g.append("text")
    .attr("class", "caption")
    .attr("x", 35)
    .attr("y", -6)
    .style("text-anchor", "middle")
    .style("font-weight", "bold")
    .text("Wineries count");

var labels = ['0', '1-2', '3-14', '15-29', '30-349', '350-499', '500-2999', '3000-5999', '> 6000'];

var legend = d3.legendColor()
    .labels(function (d) { return labels[d.i]; })
    .shapePadding(20)
    .labelOffset(22)
    .labelAlign("middle")
    .scale(color);
svg.select(".legendThreshold")
    .call(legend);

//var dsv = d3.dsv(",", "text/-separated-values; charset=ISO-8859-15");

//loading data
var promises = [
    d3.json("world_countries.json"),
    d3.csv("wineries_count.csv", function(d) {Country_id.set(d.country_id, +d.no_of_wineries);}
    )]
d3.csv("worldmap-wineries.csv", function(d) {Wine.set(d.country_id, d);})

Promise.all(promises).then(ready)

var projection = d3.geoMercator()
    .scale(130)
    .translate( [width / 2, height / 1.5]);

var path = d3.geoPath().projection(projection);

svg.call(tip, this);

function ready([world_countries]) {
//drawing map

var map = svg.append("g")
            .attr("transform", "translate(" + 120 + "," + margin.top + ")");
			
    map.append("g")
        .attr("class", "countries1")
        .selectAll("path")
        .data(topojson.feature(world_countries, world_countries.objects.countries1).features)
        .enter().append("path")
        .attr("fill", function(d) {
            return color(d.no_of_wineries = Country_id.get(d.id))})
        .attr("d", path)
        .style('stroke', 'white')
        .style('stroke-width', 1.5)
        .style("opacity",0.8)
        // tooltips
        .style("stroke","white")
        .style('stroke-width', 0.3)
        .on('mouseover',function(d){
            tip.show(d, this);

            d3.select(this)
                .style("opacity", 1)
                .style("stroke","white")
                .style("stroke-width",3);
        })
        .on('mouseout', function(d){
            tip.hide(d, this);

            d3.select(this)
                .style("opacity", 0.8)
                .style("stroke","white")
                .style("stroke-width",0.3);
        });


    map.append("path")
        .datum(topojson.mesh(world_countries, world_countries.objects.countries2, function(a, b) { return a !== b; }))
        .attr("class", "states")
        .attr("d", path);
}
