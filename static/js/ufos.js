
function createMap(ufo1940s, ufo1950s, ufo1960s, ufo1970s, ufo1980s) {
    // ufo1990s, ufo2000s, ufo2010s

    // console.log('create map function start')


    //create tile layer that will be the background of our map
    var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "light-v10",
        accessToken: API_KEY
    });

    var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "dark-v10",
        accessToken: API_KEY
    });

    var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        maxZoom: 18,
        id: "mapbox/streets-v11",
        accessToken: API_KEY
    });

    //create a basemaps object to hold the lightmap layer
    var baseMaps = {
        "Dark Map": darkmap,
        "Light Map": lightmap,
        "Street Map": streetmap
    };

    //create an overlaymaps object to hold the ufo layer
    var overlayMaps = {
        "UFO 1940s": ufo1940s,
        "UFO 1950s": ufo1950s,
        "UFO 1960s": ufo1960s,
        "UFO 1970s": ufo1970s,
        "UFO 1980s": ufo1980s
        // "UFO 1990s": ufo1990s,
        // "UFO 2000s": ufo2000s,
        // "UFO 2010-2013": ufo2010s

    };

    //create the map object with options
    var map = L.map("map-id", {
        center: [36.85, 4.00],
        zoom: 2,
        layers: [darkmap]
    });

    //create a layer control, pass in basemaps and overlaymaps
    L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
    }).addTo(map);

}


function createMarkers(response) {

    ufo1940s = [];
    ufo1950s = [];
    ufo1960s = [];
    ufo1970s = [];
    ufo1980s = [];
    // ufo1990s = [];
    // ufo2000s = [];
    // ufo2010s = [];

    console.log(response[1]);
    for (var index = 0; index < response.length; index++) {

        var features = response[index];

        var coordinateList = []
        coordinateList.push(features[10]);
        coordinateList.push(features[11]);


        var ufoMarker = L.marker(coordinateList).bindPopup("<h3>Date: " + features[0] + "</h3><h3>Place: " + features[4] + " : " + features[3] + " : " + features[2] + "</h3><h3>Shape: " + features[5] + "</h3><h3>Comments: " + features[8] + "</h3>");
            
        var t = parseInt(features.slice(0,3));
        
        console.log(t);

        switch (true) {
            case (t < 195):
                ufo1940s.push(ufoMarker);
                // console.log('1940s');
                break;
            case (t < 196):
                ufo1950s.push(ufoMarker);
                // console.log('1950s');
                break;
            case (t < 197):
                ufo1960s.push(ufoMarker);
                // console.log('1960s');
                break;
            case (t < 198):
                ufo1970s.push(ufoMarker);
                // console.log('1970s');
                break;
            case (t < 199):
                ufo1980s.push(ufoMarker);
                // console.log('1980s');
                break;
            // case (t < 200):
            //     ufo1990s.push(ufoMarker);
            //     // console.log('1990s');
            //     break;
            // case (t < 201):
            //     ufo2000s.push(ufoMarker);
            //     //console.log('2000s');
            //     break;
            // case (t < 202):
            //     ufo2010s.push(ufoMarker);
            //     // console.log('2010s');
                break;
            default:
                // console.log('Not working?')
                break;
        };

    };

    console.log(ufo1940s);

// Display total earthquakes for 30 day period
    var textArea1 = document.getElementById("1940sCount");
    textArea1.append(`1940s: ${ufo1940s.length}`);
    var textArea2 = document.getElementById("1950sCount");
    textArea2.append(`1950s: ${ufo1950s.length}`);
    var textArea3 = document.getElementById("1960sCount");
    textArea3.append(`1960s: ${ufo1960s.length}`);
    var textArea4 = document.getElementById("1970sCount");
    textArea4.append(`1970s: ${ufo1970s.length}`);
    var textArea5 = document.getElementById("1980sCount");
    textArea5.append(`1980s: ${ufo1980s.length}`);
    // var textArea6 = document.getElementById("1990sCount");
    // textArea6.append(`1990s: ${ufo1990s.length}`);
    // var textArea7 = document.getElementById("2000sCount");
    // textArea7.append(`2000s: ${ufo2000s.length}`);
    // var textArea8 = document.getElementById("2010sCount");
    // textArea8.append(`2010-2013: ${ufo2010s.length}`);
    
    //Create a layer group made from the array, pass it into the createmap function
    createMap(L.layerGroup(ufo1940s), L.layerGroup(ufo1950s), L.layerGroup(ufo1960s), L.layerGroup(ufo1970s), 
              L.layerGroup(ufo1980s));
};
// , L.layerGroup(ufo1990s), L.layerGroup(ufo2000s), L.layerGroup(ufo2010s)

// urlUFO = '/api/v1.0/ufos'

// // Perform an API call to the API to get information. Call createMarkers when complete
// createMarkers(d3.json(urlUFO));


 //  Was using an async function to delay lad up due to large data. Causes map to not load in Heroku
  // reduced decades and removed to deploy
async function readUrl() {
    let promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve(d3.json('/api/v1.0/ufos')), 10)
    });

    let result = await promise; // wait until the promise resolves (*)
    createMarkers(result);
    // alert(result); // "done!"
}

readUrl();
