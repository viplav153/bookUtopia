"use strict";

/**
 * This function will be called once the Google Maps API is finished loading.
 *
 * It adds a Google Map to the DOM with markers for each Hackbright campus.
 * Clicking on a marker will open an information window.
 */
function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8
    center: {lat: -34.397, lng: 150.644}
  });

  var geocoder = new google.maps.Geocoder():

  document.getElementById('submit').addEventListener('click', function() {
    geocoderAddress(geocoder, map)；
  })；


 function geocodeAddress(geocoder, resultsMap) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });
      }



  // const markers = [];
  // for (let hbLocation of hackbrightLocations) {
  //   markers.push(addMarker('static/imgs/marker.png', hbLocation.coords, hbLocation.name, map));
  // }

  // // Loop over markers list to attach click handlers
  // for (let marker of markers) {
  //   const aboutLocation = `<h1>Hackbright - ${marker.title}</h1>
  //     <p>Located at</p>
  //     <ul>
  //       <li><b>Lat:</b> ${marker.position.lat()}</li>
  //       <li><b>Lng:</b> ${marker.position.lng()}</li>
  //     </ul>
  //     `;

  //   addInfoWindowToMarker(aboutLocation, marker, map);
  // }

  // Un-comment this to execute code in moreDemos.js
  // initMoreDemos(map);
}


/**
//  * Utility/helper functions
//  */

// function addMarker(icon, position, title, map) {
//   const marker = new google.maps.Marker({ position, map, title, icon });

//   return marker;
// }

// function addInfoWindowToMarker(content, marker, map) {
//   const infoWindow = new google.maps.InfoWindow({
//     content,
//     maxWidth: 200
//   });

//   marker.addListener('click', () => infoWindow.open(map, marker));
// }

