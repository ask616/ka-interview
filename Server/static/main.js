function userGraph(userData) {
    var nodes = [];
    var links = [];
    var keys = Object.keys(userData)

    var i = 0
    for (var key in userData) {
        if (userData.hasOwnProperty(key)) {

            node = {
                "name" : userData[key].username,
                "id" : key,
                "isTeacher" : eval(userData[key].students).length > 0
            }

            nodes.push(node)

            if(userData[key].adjacencies.length > 0){
                for (ind = 0; ind < userData[key].adjacencies.length; ind++){
                    link = {
                        "source" : i,
                        "target" : keys.indexOf(userData[key].adjacencies[ind])
                    }

                    links.push(link)

                }
            }

            i++;
        }
    }
    
    var width = 650, height = 400

    var force = d3.layout.force()
    .charge(-150)
    .linkDistance(75)
    .size([width, height]);

    var zoom = d3.behavior.zoom()
    .scaleExtent([.4, 10])
    .on("zoom", zoomed)


    var drag = d3.behavior.drag()
    .origin(function(d) { return d; })
    .on("dragstart", dragstarted)
    .on("drag", dragged)
    .on("dragend", dragended);


    var svg = d3.select("#graph").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .call(zoom)
    .on("dblclick.zoom", null);

    var rect = svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");

    var container = svg.append("g");

    force.nodes(nodes)
    .links(links)
    .start();

    var link = container.append("g")
    .attr("class", "links")
    .selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = container.append("g")
    .attr("class", "nodes")
    .selectAll(".node")
    .data(nodes)
    .enter().append("g")
    .attr("class", "node")
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .call(drag);

    node.append("circle")
    .attr("r", function(d) { return d.weight * 2+ 12; })
    .style("fill", function(d) { return (d.isTeacher) ? "#BF55EC" : "lightcoral"; });

    node.append("text")
    .attr("dx", 12)
    .attr("dy", ".35em")
    .text(function(d) { return d.name });

    node.on("dblclick", function(d){
        d3.select(this)
        .select("circle").transition()
        .duration(750)
        .style("stroke","black");

        totalInfection(d.id)



    });

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });

    var linkedByIndex = {};
    links.forEach(function(d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });

    function isConnected(a, b) {
        return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index];
    }

    function dottype(d) {
        d.x = +d.x;
        d.y = +d.y;
        return d;
    }

    function zoomed() {
        container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }

    function dragstarted(d) {
        d3.event.sourceEvent.stopPropagation();

        d3.select(this).classed("dragging", true);
        force.start();
    }

    function dragged(d) {
        d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
    }

    function dragended(d) {
        d3.select(this).classed("dragging", false);
    }

}

function totalInfection(id){
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/totalInfection/",
        data: JSON.stringify({
            "infectedUser" : id,
            "newVersion" : $("#newVersion").val().trim()
        }),
        dataType: "json",
        contentType: "application/json"
    }).done(function(data) {
        userGraph(data)



    });
}
