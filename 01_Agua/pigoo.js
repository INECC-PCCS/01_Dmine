var jsdom = require("jsdom");
var fs = require("fs");
var phantom = require('phantom');
var url = String(process.argv[2]);
//console.log(url);

phantom.create().then(function(ph) {
  ph.createPage().then(function(page) {
    page.open(url).then(function(status) {

      page.property('content').then(function(content) {


        jsdom.env({
	 scripts: ["https://d3js.org/d3.v3.min.js"],
	 features:{QuerySelector:true},
	 html: content,
	 done: function(errors, window) {
          if(errors) console.log(errors);

          var d3 = window.d3;
	  var array = [];
	  var title = d3.select("#tituloTab");
          if(title[0][0] == null) { console.log("error0"); process.exit(); }
          title = title.text();
	  title = title.split(", ");
//	  console.log(title);

	  setTimeout(HOLA, 2500);

function HOLA() {
	var chunk = d3.select("#flex1 tbody"); 

        if(chunk[0][0]==null) { console.log("error"); process.exit();}
          var flex1 = chunk.html();

          flex1 = flex1.split("<tr");
	  flex1.shift();
          for(var i in flex1) {
	    flex1[i] = flex1[i].split("<td");
	    flex1[i].splice(0,2);
	    flex1[i][0] = flex1[i][0].replace(' align="left" abbr="indicador" class="sorted"><div style="text-align: left; width: 202px;">','');
	    flex1[i][0] = flex1[i][0].replace('</div></td>','');

	    for(var j=1; j < flex1[i].length; j++) {
	      flex1[i][j] = flex1[i][j].replace(' align="center" abbr="n','');
	      flex1[i][j] = flex1[i][j].replace('"><div style="text-align: center; width: 30px;">',',');
	      flex1[i][j] = flex1[i][j].replace('</div></td>','');
	      if(j == flex1[i].length - 1) {
		flex1[i][j] = flex1[i][j].replace('</tr>','');
	      }

	      var añoYval = flex1[i][j].split(",");
	      var obj = {};
	      obj[añoYval[0]] = añoYval[1];
	      obj["variable"] = flex1[i][0]
	      obj["entidad"] = title[1];
	      obj["ciudad"] = title[0];
	      flex1[i][j] = obj;
	    }
	    flex1[i].shift();
//	    console.log(flex1[i].length);
	    array = array.concat(flex1[i]);
          }
	  
 	  fs.writeFileSync('./json/' + title[1] + '_' + title[0] + '.json', JSON.stringify(array))
	  console.log(title);
}
	  //process.exit();
         }
        });

        page.close();
        ph.exit();
//	process.exit();
      });
    });
  });
});
