let perejilo = undefined;

let consigue = (delegacion) => {
    d3.select("#pendiente").text("Cargando información...")
    d3.json("/api/consigue/", {
        method: "POST",
        body: JSON.stringify({
            deleg: delegacion
        }),
        headers: {
            "Content-type": "application/json"
        }
    }).then(json => {
        d3.select("#pendiente").text("")
        console.log(json.crimejson)

        // aqui se hace el mapa
        var container = L.DomUtil.get('mapid');
        if (container != null) {
            container._leaflet_id = null;
        }


        var lightmap = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            accessToken: API_KEY
        });


        heatArray = [];
        markerArray = [];


        json.crimejson.slice(0, 5000).forEach(m => {

            try {
                var markers = L.marker([m.latitud, m.longitud]).bindPopup(`<h5>Crime: ${m.tipoDelito}</h5>`)
                heatArray.push([m.latitud, m.longitud])
                markerArray.push(markers)

            } catch (e) {

            }
        })

        var heat = L.heatLayer(heatArray, {
            radius: 10,
            blur: 5
        });


        var mymap = L.map('mapid', {

            center: [19.432608, -99.133209],
            zoom: 10,
            layers: [lightmap]

        });


        var layers = {
            "Markers": L.layerGroup(markerArray),
            "Heatmap": heat
        };
        var lightlayer = {
            "Lightlayer": lightmap
        };
        L.control.layers(lightlayer, layers).addTo(mymap);

        perejilo = json.crimejson;
        let delitos_tipo = json.crimejson.map(x => x.tipoDelito)
        let conteo = [...new Set(delitos_tipo)]

        // var result = {}

        // conteo.forEach(function(item) {
        //     result[item] = 0
        // })

        // delitos_tipo.forEach(function(item) {
        //     if (result.hasOwnProperty(item)) {
        //         result[item]++
        //     }
        // })
        // console.log(result);

        let conteo_crimen = [];
        let suma = [];

        for (x of conteo) {
            suma.push(
                [x, delitos_tipo.filter(d => d == x).length]
            )
        }

        conteo_crimen = suma.sort(function(a, b) {
            return b[1] - a[1];
        });

        console.group("Resultados:")
        console.log(suma)
        console.log(conteo_crimen)
        console.groupEnd()
            // for (var l = 0; l < delitos_tipo.length; l++) {
            //     for (var k = 0; k < conteo.length; k++) {
            //         if (delitos_tipo[l] === conteo[k]) {
            //             suma = suma + 1
            //         }
            //         conteo_crimen.push(suma)
            //     }
            //     suma = 0
            // }

        // console.log(conteo_crimen)


        let trace1 = {
            x: conteo_crimen.map(d => d[0]).slice(0, 10),
            y: conteo_crimen.map(d => d[1]).slice(0, 10),
            type: "bar"
        };

        let datos = [trace1];

        Plotly.newPlot('myDiv', datos);




    });








}



// Escuchadores
d3.selectAll("#dropdown").on("change", function() {
    var delegacion = d3.selectAll("#dropdown option:checked").text()
    console.log(delegacion)
    consigue(delegacion)
});