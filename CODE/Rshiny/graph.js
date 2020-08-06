//install packages("r2d3")

//library(r2d3)

//expected data input 
//r2d3(data=c(list(price=list(30, 25, 40, 15, 40, 20, 35, 45, 50, 55), score=list(7,8,1,2,6,7,4,5,8,7), name=list('wine1', 'wine2', 'wine3', 'wine4', 'wine5', 'wine6', 'wine7', 'wine8', 'wine9', 'wine10'))), script = "graph.js")

svg.selectAll("*").remove();

hgt = height - 100;
wdth = width/2;

var y = d3.scaleBand()
		   .range([hgt, 0]);
		   
var x = d3.scaleLinear()
		   .range([0, wdth]);

var xTop = d3.scaleLinear()
		   .range([0, wdth]);

finalData = [];

for(i = 0; i<data.name.length; i++){
  finalData.push({name: data.name[i], price: data.price[i], score:data.score[i]});
}

//print(finalData);

x.domain([0, d3.max(finalData, function(d){ return d.price; })]);
y.domain(data.name.map(function(d) { return d; })).padding(0.8);

xTop.domain([d3.min(finalData, function(d){ return d.score; }), d3.max(finalData, function(d){ return d.score; })]);

var rectangles = svg.selectAll('rect')
.data(finalData)
.enter().append('rect')
.attr('width', function(d) { return x(d.price); })
.attr("x", 150)
.attr("y", function(d) { return (y(d.name)+10); })
.attr('height', "20")
.attr('fill', 'green');

var circle = svg.selectAll("circle")
        .data(finalData)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return (xTop(d.score)+150); })
        .attr("cy", function (d) { return (y(d.name)+20); })
        .attr("r", 5)
        .style("fill", "blue");

var yAxis = d3.axisLeft(y);

// Add the X Axis
svg.append("g")
.attr("transform", "translate(150, "+ (height-80) + ")")
.call(d3.axisBottom(x));

// Add the X Axis top
svg.append("g")
.attr("transform", "translate(150, "+ (30) + ")")
.call(d3.axisTop(xTop));

// Add the Y Axis
svg.append("g")
.attr("transform", "translate(150, 20)")
.call(yAxis);

// add label for the x axis
svg.append("text")
  .attr("transform", "translate(" + width/2 + "," + (height - 50) + ")")
  .style("text-anchor", "middle")
  .text("Price");

// add TOP label for the score
svg.append("text")
  .attr("transform", "translate(" + width/2 + ", 12)")
  .style("text-anchor", "middle")
  .text("Score");

// legends
var legendData = [
	["Score", "blue", "circle"],
	["Price", "green", "square"]
];

svg.selectAll('.symbol')
  .data(legendData)
  .enter()
  .append('path')
  .attr('transform', function(d, i) {
    return 'translate(' + (width - 120) + ',' + ((i * 20) + 10) + ')';
  })
  .attr('d', d3.symbol().type(function(d, i) {
      if (d[2] === "circle") 
	  {
        return d3.symbolCircle;
      } 
	  else if (d[2] === "square") 
	{
        return d3.symbolSquare;
      }
    })
    .size(100))
  .style("fill", function(d) {
    return d[1];})
  .style("stroke", function(d) {
    return d[1];
  });
 
svg.selectAll('.label')
  .data(legendData)
  .enter()
  .append('text')
  .attr("x", width - 100)
  .attr("y", function(d, i){ return ((i * 20)+15);})
  .text(function(d) {
    return d[0];
  }); 