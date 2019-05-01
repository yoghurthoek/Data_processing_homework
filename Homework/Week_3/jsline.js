// Name: Jochem van den Hoek
// Student number: 11066288

var fileName = "converted.json";
var txtFile = new XMLHttpRequest();
txtFile.onreadystatechange = function() {
    if (txtFile.readyState === 4 && txtFile.status == 200) {
        data = JSON.parse(txtFile.responseText);

        // Arrays to store graph data
        var dataX = [];
        var dataY = [];

        // Add data to arrays
        for(key in data){
          dataX.push(key);
          dataY.push(data[key]["SQ"])
        };

    }


    var canvas = document.getElementById('lineGraph');
    var ctx = canvas.getContext('2d');

    // Graph outline points
    var graphX = 0;
    var graphRefL = 15;
    var graphRefR = 585;
    var graphY = 35;
    var graphWidth = 600;
    var graphHeight = 550;

    // Draw the graph box
    ctx.strokeRect(graphX, graphY, graphWidth, graphHeight);

    // Draw reference lines
    ctx.beginPath();
    ctx.strokeStyle = "#BBB";
    ctx.moveTo(graphRefL, graphHeight);
    ctx.lineTo(graphRefR, graphHeight);
    ctx.stroke();


    function createTransform(domain, range){
      // domain is a two-element array of the data bounds [domain_min, domain_max]
      // range is a two-element array of the screen bounds [range_min, range_max]
      // this gives you two equations to solve:
      // range_min = alpha * domain_min + beta
      // range_max = alpha * domain_max + beta
      // a solution would be:
      var domain_min = domain[0]
      var domain_max = domain[1]
      var range_min = range[0]
      var range_max = range[1]
      // formulas to calculate the alpha and the beta
      var alpha = (range_max - range_min) / (domain_max - domain_min)
      var beta = range_max - alpha * domain_max

      // returns the function for the linear transformation (y= a * x + b)
      return function(x){
        return alpha * x + beta;
      }
    }
}
txtFile.open("GET", fileName);
txtFile.send();
