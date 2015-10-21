function userGraph() {

    var graph = {
        "nodes":[
            {"name":"1","rating":90,"id":2951},
            {"name":"2","rating":80,"id":654654},
            {"name":"3","rating":80,"id":6546544},
            {"name":"4","rating":1,"id":68987978},
            {"name":"5","rating":1,"id":9878933},
            {"name":"6","rating":1,"id":6161},
            {"name":"7","rating":1,"id":64654},
            {"name":"8","rating":20,"id":354654},
            {"name":"9","rating":50,"id":8494},
            {"name":"10","rating":1,"id":6846874},
            {"name":"11","rating":1,"id":5487},
            {"name":"12","rating":80,"id":"parfum_kenzo"},
            {"name":"13","rating":1,"id":65465465},
            {"name":"14","rating":90,"id":"jungle_de_kenzo"},
            {"name":"15","rating":20,"id":313514},
            {"name":"16","rating":40,"id":36543614},
            {"name":"17","rating":100,"id":"Yann_YA645"},
            {"name":"18","rating":1,"id":97413},
            {"name":"19","rating":1,"id":97414},
            {"name":"20","rating":100,"id":976431231},
            {"name":"21","rating":1,"id":9416},
            {"name":"22","rating":1,"id":998949},
            {"name":"23","rating":100,"id":984941},
            {"name":"24","rating":100,"id":"99843"},
            {"name":"25","rating":1,"id":94915},
            {"name":"26","rating":1,"id":913134},
            {"name":"27","rating":1,"id":9134371}
        ],
        "links":[
            {"source":6,"target":5,"value":6, "label":"publishedOn"},
            {"source":8,"target":5,"value":6, "label":"publishedOn"},
            {"source":7,"target":1,"value":4, "label":"containsKeyword"},
            {"source":8,"target":10,"value":3, "label":"containsKeyword"},
            {"source":7,"target":14,"value":4, "label":"publishedBy"},
            {"source":8,"target":15,"value":6, "label":"publishedBy"},
            {"source":9,"target":1,"value":6, "label":"depicts"},
            {"source":19,"target":18,"value":2, "label":"postedOn"},
            {"source":18,"target":1,"value":6, "label":"childOf"},
            {"source":17,"target":19,"value":8, "label":"describes"},
            {"source":18,"target":11,"value":6, "label":"containsKeyword"},
            {"source":17,"target":13,"value":3, "label":"containsKeyword"},
            {"source":20,"target":13,"value":3, "label":"containsKeyword"},
            {"source":20,"target":21,"value":3, "label":"postedOn"},
            {"source":22,"target":20,"value":3, "label":"postedOn"},
            {"source":23,"target":21,"value":3, "label":"manageWebsite"},
            {"source":23,"target":24,"value":3, "label":"manageWebsite"},
            {"source":23,"target":25,"value":3, "label":"manageWebsite"},
            {"source":23,"target":26,"value":3, "label":"manageWebsite"}
        ]
    }


    var width = 650, height = 400

    var force = d3.layout.force()
    .charge(-200)
    .linkDistance(50)
    .size([width, height]);

    var zoom = d3.behavior.zoom()
    .scaleExtent([.4, 10])
    .on("zoom", zoomed);

    var drag = d3.behavior.drag()
    .origin(function(d) { return d; })
    .on("dragstart", dragstarted)
    .on("drag", dragged)
    .on("dragend", dragended);


    var svg = d3.select("#map").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .call(zoom);

    var rect = svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");

    var container = svg.append("g");

    force
    .nodes(graph.nodes)
    .links(graph.links)
    .start();

    var link = container.append("g")
    .attr("class", "links")
    .selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = container.append("g")
    .attr("class", "nodes")
    .selectAll(".node")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "node")
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .call(drag);

    node.append("circle")
    .attr("r", function(d) { return d.weight * 2+ 12; })
    .style("fill", function(d) { return "#00f"; });

    node.append("text")
     .attr("dx", 12)
     .attr("dy", ".35em")
     .text(function(d) { return d.name });


    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });

    var linkedByIndex = {};
    graph.links.forEach(function(d) {
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
