/*
Este archivo tiene como objetivo asignar a cada registro que exista para la dimensión de agua una clave geoestadística.
*/

// Lo primero es generar una conexión a la base de datos en donde se encuentran las claves
// geo-estadísticas del INEGI.

var inegi = new Mongo().getDB("inegi");
var entidades_inegi_abr = 
	 inegi.cves_geo.aggregate([
	  { $group: {
	    _id: "$NOM_ABR"
	  }}
	 ]).toArray().map(function(d) { return d._id; });
   
// Después, se necesita guardar en una variable la conexión a la base de datos para la
// dimensión de agua.

var agua = new Mongo().getDB("agua");
var agua_cols = agua.getCollectionNames();

// Las colecciones dentro de la base de datos "agua" tienen ciertos nombres por entidad.
// Para facilitar la homologación de claves, se necesita checar qué datos tienen el mismo
// nombre.

function checharEntidades(col, entidad) {
  var a = agua.getCollection(col).find({ "entidad": entidad }).count();
  return a;
}

function vacios() {
  var arr = [];

  for(var i in agua_cols) {
    for(var j in entidades_inegi_abr) {
      var obj = {};
      obj.col = agua_cols[i];
      obj.ent = entidades_inegi_abr[j];
      obj.count = checharEntidades(agua_cols[i], entidades_inegi_abr[j]);
      arr.push(obj);
    }
  }

  arr = arr.filter(function(d) { return d.count == 0; })
    .map(function(d) { return {ent:d.ent, col:d.col}; }).sort()

  return arr;
}


function noMatch(col) {
  var INEGI = inegi.cves_geo.aggregate([ { "$group": { _id: "$NOM_ABR" } } ]).toArray()
                .map(function(d) { return d._id; });


  var AGUA = agua.getCollection(col).aggregate([ { $group: { _id: "$entidad" } } ])
		.toArray().map(function(d) { return d._id; });

  var arr = JSON.parse(JSON.stringify(INEGI));

  for(var i in INEGI) {
    for(var j in AGUA) {
      if( INEGI[i] == AGUA[j] ) arr[i] = null;
    }
  }

  return arr.filter(function(d) { return d != null; });
}

var nomEntidades = [
{ pigoo:"Aguascalientes",inegi:"Ags",resto:"Ags" },
{ pigoo:"Baja California",inegi:"BC",resto:"Bc" },
{ pigoo:"Baja California Sur",inegi:"BCS",resto:"Bcs" },
{ pigoo:"Campeche",inegi:"Camp",resto:"Cam" },
{ pigoo:"Chiapas",inegi:"Chis",resto:"Chis" },
{ pigoo:"Chihuahua",inegi:"Chih",resto:"Chih" },
{ pigoo:"Coahuila",inegi:"Coah",resto:"Coah" },
{ pigoo:"Colima",inegi:"Col",resto:"Col" },
{ pigoo:"Distrito Federal",inegi:"CDMX",resto:"CDMX" },
{ pigoo:"Durango",inegi:"Dgo",resto:"Dgo" },
{ pigoo:"Guanajuato",inegi:"Gto",resto:"Gto" },
{ pigoo:"Guerrero",inegi:"Gro",resto:"Gro" },
{ pigoo:"Hidalgo",inegi:"Hgo",resto:"Hgo" },
{ pigoo:"Jalisco",inegi:"Jal",resto:"Jal" },
{ pigoo:"Michoacán",inegi:"Mich",resto:"Mich" },
{ pigoo:"Morelos",inegi:"Mor",resto:"Mor" },
{ pigoo:"México",inegi:"Mex",resto:"Mex" },
{ pigoo:"Nayarit",inegi:"Nay",resto:"Nay" },
{ pigoo:"Nuevo León",inegi:"NL",resto:"Nl" },
{ pigoo:"Oaxaca",inegi:"Oax",resto:"Oax" },
{ pigoo:"Puebla",inegi:"Pue",resto:"Pue" },
{ pigoo:"Querétaro",inegi:"Qro",resto:"Qro" },
{ pigoo:"Quintana Roo",inegi:"Q. Roo",resto:"Qroo" },
{ pigoo:"San Luis Potosí",inegi:"SLP",resto:"Slp" },
{ pigoo:"Sinaloa",inegi:"Sin",resto:"Sin" },
{ pigoo:"Sonora",inegi:"Son",resto:"Son" },
{ pigoo:"Tabasco",inegi:"Tab",resto:"Tab" },
{ pigoo:"Tamaulipas",inegi:"Tamps",resto:"Tamps" },
{ pigoo:"Tlaxcala",inegi:"Tlax",resto:"Tlax" },
{ pigoo:"Veracruz",inegi:"Ver",resto:"Ver" },
{ pigoo:"Yucatán",inegi:"Yuc",resto:"Yuc" },
{ pigoo:"Zacatecas",inegi:"Zac",resto:"Zac" }
];

function asignarClavesEntidades() { // Esta función va a tener que ejecutarse al final!!

//Para cada colección...
  for(var c in agua_cols) {
// .. obtener los nombres de las entidades federativas...
    var noms = agua.getCollection(agua_cols[c]).aggregate([
      { $group: { _id: "$entidad" } }
    ]).toArray().map(function(d) { return d._id; });

// ... y para cada una de esas entidades federativas ...
    for(var e in noms) {
      for(var i in nomEntidades) {
         var obj = nomEntidades[i];
	 var keys = Object.keys(obj);

// ... checar qué tipo de nombre tiene ...         
	 for(var j in keys) {
           if(obj[keys[j]] == noms[e]) {
             var cve_util = obj[keys[j]];

// ... para encontrar la clave geo-estadística que le corresponde <|=^D ...
             var cve_ent = inegi.cves_geo.find({ "NOM_ABR": obj["inegi"] }).limit(1).toArray()[0].CVE_ENT; 
	     var cuentaConCve = agua.getCollection(agua_cols[c]).find({ "entidad": cve_util, "cve_ent": { $exists: true } }).count();
	     var cuentaTotal = agua.getCollection(agua_cols[c]).find({ "entidad": cve_util }).count();

// ... si cada entidad de cada colección no tiene clave asígnala...
	     if( cuentaConCve == 0 ) {
	       agua.getCollection(agua_cols[c]).updateMany({ "entidad":cve_util },{"$set":{ "cve_ent":cve_ent }})	
	       print(agua_cols[c],cve_util,cve_ent,"... cve asignada!");
	     } else {
		print("con clave:",cuentaConCve, ". Total:",cuentaTotal,"-->",agua_cols[c],cve_util,cve_ent,"-->","diferencia:",cuentaTotal - cuentaConCve);
	     }
	   }
         }
      }
    }
  }
}


function asignarClavesMunicipios() {
  var array = [];
  var clavesEnt = inegi.cves_geo.aggregate([
    { $group: { _id: "$CVE_ENT" } }
  ]).toArray().map(function(d) { return d._id; });

// Para cada colección...
  for(var c in agua_cols) {
// ... y para cada entidad ...
   for(var e in clavesEnt) {
// .. obtener las claves municipales de esa entidad y los datos de cada entidad ..
    var cveMun = inegi.cves_geo.find({ "CVE_ENT":clavesEnt[e] },{ "NOM_MUN":1 }).toArray();
    var col = agua.getCollection(agua_cols[c]).find({ "cve_ent": clavesEnt[e] }).toArray();

// .. si existen los datos de esa colección para esa entidad...
    if( col.length != 0 ) {
// .. ver si los nombres de los municipios coinciden con los mismos del INEGI, si coinciden
//    asignar la clave geo-estadística municipal a los datos de de la colección.
      for(var i in col) {
        for(var j in cveMun) {
          if(col[i].municipio == cveMun[j].NOM_MUN || col[i].ciudad == cveMun[j].NOM_MUN ) col[i].cve_mun = cveMun[j]._id;

        }
      }

// .. para los nombres que no coinciden, asignarlos a una variable..
      var noIgual = col.filter(function(d) { return !d.cve_mun; });
// .. y guardar cada uno de los registros sin clave en una lista para observarlos fuera de la
// .. función ...
      noIgual.forEach(function(d) { array.push({col:agua_cols[c],dato:d}); });
      //print(agua_cols[c], clavesEnt[e], col.length, noIgual.length);

// ... añadir claves municipales si no hay ninguna...
      coll = col.filter(function(d) { return d.cve_mun; });
      print(agua_cols[c], " | ENT:", clavesEnt[e], "| total:", col.length," | con_cve:",coll.length," | sin_cve:", noIgual.length);
      
      var siCve_mun = agua.getCollection(agua_cols[c]).find({ "cve_ent":clavesEnt[e], cve_mun: { $exists:true } }).count();

      if(true) { print("actualizados: ",siCve_mun);

          coll.forEach(function(d) {
	     agua.getCollection(agua_cols[c]).update({_id:d._id},{ $set: { cve_mun: d.cve_mun } });
	  });


      }

    }

   } 

  }
  array = array.filter(function(d) {
	if( d.dato.municipio != "Estado" && d.dato.municipio != "Ciudad de México" && d.dato.municipio != "Resto de los municipios" && d.dato.municipio != "Resto de municipios" ) return d;
  });
  return array;
}

////////////////////////////////////////////////////////////////////////////////////////
// LAS SIGUIENTES FUNCIONES SERÁN ÚTILES SI UTILIZO LA COLECCIÓN "pigoo".
///////////////////////////////////////////////////////////////////////////////////////


function buscarMun(ent,string) {
  var INEGI = inegi.cves_geo.find({ CVE_ENT: ent }).toArray();
  var arr = [];

  INEGI.forEach(function(d) {
    var str = d.NOM_MUN;
    var patt = new RegExp(string);

    if(patt.test(str)) {
      arr.push(d);
    };

   // return arr;
  });
  return arr;
}


function pulirConRegExpParaMunicipios(b,ent) {

  var forPrint = b.filter(function(d) { return d.cve_ent==ent; })
   .map(function(d) { return d.ciudad; })
   .reduce(function(a,b) { if (a.indexOf(b) < 0 ) a.push(b); return a; }, [])

  print(forPrint);

  var arr = [];

  b.filter(function(d) { return d.cve_ent==ent; })
   .map(function(d) { return d.ciudad; })
   .reduce(function(a,b) { if (a.indexOf(b) < 0 ) a.push(b); return a; }, [])
   .forEach(function(d) {
     d = d.split(" ");

     if(p.length == 1) arr.push(p[0]);
  });

  return arr;
};



//////////////////////////////////////////////////////
// COTEJAR CON LAS CLAVES DEL SUN
/////////////////////////////////////////////////

function cotejoSUN() {
  var test = new Mongo().getDB("test");

  var arr = test.SUN.aggregate([
    { $project: {
         nom_sun : "$Nombre de la ciudad (zona metropolitana)",
         cve_sun : "$Número de registro en el Sistema Urbano Nacional 2010",
         nom_mun: "$Nombre del municipio",
	 cve_mun: "$Clave del municipio",
         _id:0
    } },
    {
      $group: { _id: "$cve_sun", muns: { $push: { cve:"$cve_mun" } } },
    }
   ]);

   arr = arr.toArray();

   for(var c in agua_cols) {
     var cves = agua.getCollection(agua_cols[c]).find({ cve_mun: { $exists: true} },{ _id:0, cve_mun:1 }).toArray().map(function(d) { return d.cve_mun; });

   //if(VAR) {
     arr.forEach(function(d) {
      for(var i in d.muns) {
        var cve = String(d.muns[i].cve);
        if( cve.length == 4 ) cve = "0" + cve;
        d.muns[i].cve = cve;

        for( var j in cves ) {
          if(d.muns[i].cve == cves[j]) d.muns[i][agua_cols[c]] = true;     
        }

      }

     });
   }
/**/
   return arr;
}


//////////////////////////////////////////////////////////////////////////////////
//////// Si no existe la base de datos con el registro de qué datos existen para cada mun
///////  pues que se haga.
////////////////////////////////////////////////////////////////////////////////////
var cualesHay = agua.cuales.find().count();

if(cualesHay == 0) {
  var cuales = cotejoSUN();
  agua.cuales.insert(cuales);
  print("0");
};
//////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////



//Asignar clave del SUN a cada municipio
function asignarCveSUN() {  
  var cuales = agua.cuales.find().toArray();
  for(var j in cuales) {

    cuales[j].muns.forEach(function(d) {
      var cols = Object.keys(d);
      cols.splice(cols.indexOf("cve"),1);
      for(var i in cols) {
        agua.getCollection(cols[i]).updateMany({ 'cve_mun': d.cve },
	{'$set': { 'cve_sun': String(cuales[j]._id) } });
      } 
    });

  }
};

// Asignar el nombre de la colección a la que cada registro pertenece.
function asignarNomCol() {
  var colecciones = agua.getCollectionNames();
  colecciones.splice(colecciones.indexOf("cuales",1));
  
  for(var i in colecciones) {
    agua.getCollection(colecciones[i]).updateMany({},{ '$set':
    { 'collection':colecciones[i] } 
    });
  }

};

// Conjuntar todos los datos del SUN disponibles.
function concatenarSUN() {
  var a = [];
  var colecciones = agua.getCollectionNames();
  colecciones.splice(colecciones.indexOf("cuales",1));

  for(var i in colecciones) {
    var b = agua.getCollection(colecciones[i]).find({ 'cve_sun': { '$exists':1  } }).toArray();
    a = a.concat(b);
  }
  
  return a;
};


// Si no existe una colección con todos los datos para los municipios del SUN, crearlo..
var SUN_agua = agua.SUN_agua.find().count();
if(SUN_agua == 0) {
  var a = concatenarSUN();
  agua.SUN_agua.insert(a);
};


function checarDobles() {
  var cols = agua.getCollectionNames();
  cols.splice(0,1);
  cols.splice(0,1);

  for(var i in cols) {
    var mun = agua.getCollection(cols[i]).find({ 'cve_mun': { '$exists':1 } }).limit(1).toArray()[0].cve_mun;
    var query = agua.getCollection(cols[i]).find({ "cve_mun": mun }).count();

    print(cols[i],query);
  }
}


function combinarDobles(col) {
  var a;

  if( col == 'disponibilidadYacceso' ) {

    a = agua.SUN_agua.aggregate([
      { $match: {
        "collection":col
      } },
      { $group: {
          _id: '$cve_mun',
          info: { $push: "$$ROOT" }
      } },
      { $project: {
          uno: { '$arrayElemAt':['$info',0] },
          dos: { '$arrayElemAt':['$info',1] }
  
      } },
      { $project: {
	  _id: 1,
	  año: "$uno.año",
	  entidad: "$uno.entidad",
	  municipio: "$uno.municipio",
	  total: "$uno.total",
	  entubada_total: "$uno.entubada_total",
	  entubada_dentro_de_vivienda: "$uno.entubada_dentro_de_vivienda",
	  entubada_fuera_de_vivienda_dentro_de_terreno: "$uno.entubada_fuera_de_vivienda_dentro_de_terreno",
	  acarreo_total: "$uno.acarreo_total",
	  acarreo_llave_comunitaria: "$uno.acarreo_llave_comunitaria",
	  acarreo_otra_vivienda: "$uno.acarreo_otra_vivienda",
	  acarreo_pipa: "$dos.acarreo_pipa",
	  acarreo_pozo: "$dos.acarreo_pozo",
	  acarreo_rio_lago_arroyo: "$dos.acarreo_rio_lago_arroyo",
	  acarreo_lluvia: "$dos.acarreo_lluvia",
	  acarreo_no_especificado: "$dos.acarreo_no_especificado",
	  no_especificado: "$dos.no_especificado",
	  cve_ent: "$dos.cve_ent",
	  cve_mun: "$dos.cve_mun",
	  cve_sun: "$dos.cve_sun",
	  collection: "$dos.collection"
      } }
    ]).toArray();

  }

  if( col == 'plantasDeTratamiento' ) {
    
    a = agua.SUN_agua.aggregate([
      { $match: {
        "collection":col,
	'año': 2015
      } },
      { $group: {
          _id: '$cve_mun',
          info: { $push: "$$ROOT" }
      } }
    ]).toArray();

  

  a.filter(function(d) { return d.info.length == 1; })
  .forEach(function(d) {
    var keys = Object.keys(d.info[0]);
    for(var i in keys) {
      if(keys[i] != "_id") {
        d[keys[i]] = d.info[0][keys[i]];
      } 
    }
    delete d.info
  });

  a.filter(function(d) { if(d.info && d.info.length == 2) return d; })
    .forEach(function(d) {

      var keys = [];
      keys = keys.concat(Object.keys(d.info[0]));
      keys = keys.concat(Object.keys(d.info[1]));

      var unique = keys.reduce(function(a,b) {
        if(a.indexOf(b) < 0) a.push(b); return a; },
	[]);

      var sorted_arr = keys.slice().sort();
      var results = [];

      for(var i=0; i<sorted_arr.length-1; i++) {
        if(sorted_arr[i+1] == sorted_arr[i]) {
	  results.push(sorted_arr[i]);
        }
      }

      for(var i in results) {
        for(var j in unique) {
	  if(results[i] == unique[j]) {
	    unique.splice(unique.indexOf(unique[j]),1);
	  }
        }
      }

      for(var i in results) {
	d[results[i]] = d.info[0][results[i]]
      }

      for(var i in d.info) {
       for(var j in d.info[i]) {
        for(var k in unique) {
	  if(unique[k] == j) d[unique[k]] = d.info[i][j]
        }
       }
      }
 
      delete d.info;
      d._id = d.cve_mun;	
    });

  }

  return a;
}


function combinarTodos() {
  var a = agua.SUN_agua.aggregate([
    { $match: { "año": 2015 } },
    { $group: {
        _id: "$cve_mun",
	info: { $push: "$$ROOT" }
    } }
  ]).toArray();

  a.forEach(function(d) { 
      var keys = [];

      for(var i in d.info) { keys = keys.concat(Object.keys(d.info[i])); }

      var unique = keys.reduce(function(a,b) {
	if(a.indexOf(b) < 0) a.push(b); return a; }, []);

      var sorted_arr = keys.slice().sort();
      var results = [];

      for(var i=0; i<sorted_arr.length-1; i++) {
        if(sorted_arr[i+1] == sorted_arr[i]) {
          results.push(sorted_arr[i]);
        }
      }

      var results = results.reduce(function(a,b) {
	if(a.indexOf(b) < 0) a.push(b); return a; }, []);

      for(var i in results) {
        for(var j in unique) {
          if(results[i] == unique[j]) {
            unique.splice(unique.indexOf(unique[j]),1);
          }
        }
      }

      for(var i in results) {
        d[results[i]] = d.info[0][results[i]]
      }

      for(var i in d.info) {
       for(var j in d.info[i]) {
        for(var k in unique) {
          if(unique[k] == j) d[unique[k]] = d.info[i][j]
        }
       }
      }

      delete d.info;

      d._id = d.cve_mun;

  });

  return a;
}
