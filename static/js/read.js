// d3.json("carpetas-de-investigacion-pgj-de-la-ciudad-de-mexico.geojson", d => {
//     console.log(d)
// });

let delitos = [];
let categorias = [];
let años = [];
let delegacion = [];
let myurl1 = "./carpetas-de-investigacion-pgj-de-la-ciudad-de-mexico.geojson"
let uniqueDelitos = [];
let uniqueCategorias = [];
let uniqueAños = [];
let uniqueDelegacion = [];
let CDMXdel = [];

d3.json(myurl1, d => {
            d.features.forEach(m => {
                    if (m.properties.alcaldia_hechos == "Azcapotzalco") {
                        delitos.push(m.properties.delito)
                        categorias.push(m.properties.categoria_delito)
                        años.push(m.properties.ao_hechos)
                        delegacion.push(m.properties.alcaldia_hechos)

                    })

                uniqueDelitos = Array.from(new Set(delitos)); uniqueCategorias = Array.from(new Set(categorias)); uniqueAños = Array.from(new Set(años)); uniqueDelegacion = Array.from(new Set(delegacion));
                // CDMXdel = Array.from(delegacion.filter("Azcapotzalco"))
            });