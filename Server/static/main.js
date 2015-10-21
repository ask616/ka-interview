/*
   Initializes the visualization using data retrieved from server and
   uses d3 to render
*/
function userGraph(userData) {
    var nodes = [];
    var links = [];
    var keys = Object.keys(userData)

    var i = 0; //Maintains index of current user
    //Iterate through every user in the DB
    for (var key in userData) {
        //Check to make sure we're not checking a prototype key
        if (userData.hasOwnProperty(key)) {

            node = {
                "name" : userData[key].username,
                "id" : key,
                "isTeacher" : eval(userData[key].students).length > 0,
                "version" : userData[key].version
            }

            nodes.push(node)

            //Link up the node to all of its adjacent nodes
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

    var freqs = {};
    for(var i = 0; i < nodes.length; i++){
        if(nodes[i].version in freqs){
            freqs[nodes[i].version]++;
        } else{
            freqs[nodes[i].version] = 1;
        }
    }

    for (var key in freqs) {
        //Check to make sure we're not checking a prototype key
        if (freqs.hasOwnProperty(key)) {
            var itemString = "<li>There are " + freqs[key] + " users with version " + key + "</li>";
            $(".version-list").append(itemString);
        }
    }


    var width = 650, height = 400

    var force = d3.layout.force()
    .charge(-100)
    .linkDistance(75)
    .size([width, height]);

    var zoom = d3.behavior.zoom()
    .scaleExtent([.4, 10])
    .on("zoom", zoomed)

    var drag = d3.behavior.drag()
    .origin(function(d) { return d })
    .on("dragstart", dragstarted)
    .on("drag", dragged)

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
    .style("stroke-width", function(d) { return 1 });

    var node = container.append("g")
    .attr("class", "nodes")
    .selectAll(".node")
    .data(nodes)
    .enter().append("g")
    .attr("class", "node")
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .call(drag);

    node.append("title")
    .text(function(d){ return d.version })

    node.append("circle")
    .attr("r", function(d) { return 5 })
    .style("fill", function(d) { return (d.isTeacher) ? "LightCoral" : hashStringToColor(d.version); });

    node.append("text")
    .attr("dx", 12)
    .attr("dy", "3px")
    .text(function(d) { return d.name });

    //Totally infect the graph of any node that is double-clicked
    node.on("dblclick", function(d){
        d3.select(this)
        .select("circle").transition()
        .duration(750)
        .style("stroke","black");

        totalInfection(d.id)
    });

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x })
        .attr("y1", function(d) { return d.source.y })
        .attr("x2", function(d) { return d.target.x })
        .attr("y2", function(d) { return d.target.y });
        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")" });
    });

    function zoomed() {
        container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }

    function dragstarted(d) {
        d3.event.sourceEvent.stopPropagation();
        force.start();
    }

    function dragged(d) {
        d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
    }

}

/*
   Total Infection changes the version of the entire graph component containing
   the user specified by id
*/
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
        // Reload the page to refresh results reflecting infection
        location.reload();
    });
}

/*
   Limited Infection changes the version of graphs whose sizes add up exactly
   to the specified size
*/
function limitedInfection(){
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/limitedInfection/",
        data: JSON.stringify({
            "target" : $("#targetInfected").val().trim(),
            "newVersion" : $("#newVersion").val().trim()
        }),
        dataType: "json",
        contentType: "application/json"
    }).done(function(data) {
        location.reload();
        // Reload the page to refresh results reflecting infection
    }).fail(function() {
        // Error returned indicating that the target cannot be reached
        alert("That target cannot be reached with this set!");
    })
}

// Hash functions from online that convert strings to hex values
function djb2(str){
    var hash = 5381;
    for (var i = 0; i < str.length; i++) {
        hash = ((hash << 5) + hash) + str.charCodeAt(i);
    }
    return hash;
}

function hashStringToColor(str) {
    var hash = djb2(str);
    var r = (hash & 0xFF0000) >> 16;
    var g = (hash & 0x00FF00) >> 8;
    var b = hash & 0x0000FF;
    return "#" + ("0" + r.toString(16)).substr(-2) + ("0" + g.toString(16)).substr(-2) + ("0" + b.toString(16)).substr(-2);
}
