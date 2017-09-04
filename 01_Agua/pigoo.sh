## FUENTE: Programa de Indicadores de Organismos Operadores de Agua.

## OBJETIVO: Descargar toda la información contenida en el sitio del Programa de Indicadores 
## de Organismos Operadores de Agua para almacenarlos en MongoDB.

obtenerLigas() {

## El primer paso consiste en obtener los hipervínculos que contienen la información para cada
## una de las ciudades disponibles.

## Si no existe el archivo con las ligas que contienen la información de agua para cada ciudad entonces hay que crearlo.
  if [[ ! -f ciudades ]]; then

   curl -s "http://www.pigoo.gob.mx" | grep "ciudades" | cut -d '/' -f2 | cut -d'/' -f2 | cut -d'"' -f4 | sed 's/>//g' | sed 's/<//g' | sed '/src/d' > nombres;
   echo "Nombres de ciudades obtenidos."

   curl -s "http://www.pigoo.gob.mx/" | grep "ciudades" | cut -d'/' -f2 | cut -d'"' -f1 | sed 's/amp;//g' | sed '/content/d' > ligas;
   echo "Ligas con información sobre ciudades obtenidas.";

   paste -d"," ligas nombres > ciudades;
   rm ligas nombres;
  fi

## Esto extrae las ligas para obtener la información de unas tablas en las que se enlistan
## los valores de cada una de las variables de interés.
  if [[ ! -f tablas ]]; then
   while read line; do
     liga=$(echo $line | cut -d',' -f1);
     nombre=$(echo $line | cut -d',' -f2);
     echo "";
     echo "$nombre:";
     tabla=$(curl -s "http://www.pigoo.gob.mx/$liga" | grep 'dashboard' | cut -d '"' -f 2);
     echo $tabla;
     echo "";
     curl -s "http://www.pigoo.gob.mx/$liga" | grep 'dashboard' | cut -d '"' -f 2 >> tablas;
   done < ciudades
  fi
}

procesar() {
 mkdir json;
 while read liga; do
  #sleep 3;
  resultado=$(node pigoo "${liga}");
  echo $resultado
  while [[ $resultado == 'error' || $resultado == 'error0' ]]; do
     resultado=$(node pigoo "${liga}")
     echo $resultado;
  done
#  sleep 3;
 done < tablas
}

almacenar() {
 for i in json/*.json; do
   mongoimport -d agua -c pigoo --type=json --jsonArray "$i";
 done
}

limpiar() {
  rm tablas ciudades
  rm -r json node_modules
}

todo() {
 obtenerLigas
 procesar
 almacenar
 limpiar
}
