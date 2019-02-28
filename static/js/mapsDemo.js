"use strict";

/**
 * This function will be called once the Google Maps API is finished loading.
 *
 * It adds a Google Map to the DOM with markers for each Hackbright campus.
 * Clicking on a marker will open an information window.
 */
function initMap() {
  const sfBayCoords = { lat: 37.601773, lng: -122.202870 };

  const map = new google.maps.Map(document.getElementById('map'), {
    center: sfBayCoords,
    zoom: 8
  });

  const sfMarker = addMarker('static/imgs/marker.png', sfBayCoords, 'SF Bay', map);
  sfMarker.addListener('click', () => alert('Hi!'));

  const hackbrightLocations = [
    {
      name: 'San Francisco',
      coords: { lat: 37.7887501, lng: -122.4137792 }
    },
    {
      name: 'South Bay',
      coords: { lat: 37.3797848, lng: -121.9432011 }
    },
    {
      name: 'East Bay',
      coords: { lat: 37.8028806, lng: -122.2691348 }
    },
  ];

  // Loop over hackbrightLocations to make lots of markers
  const markers = [];
  for (let hbLocation of hackbrightLocations) {
    markers.push(addMarker('static/imgs/marker.png', hbLocation.coords, hbLocation.name, map));
  }

  // Loop over markers list to attach click handlers
  for (let marker of markers) {
    const aboutLocation = `<h1>Hackbright - ${marker.title}</h1>
      <p>Located at</p>
      <ul>
        <li><b>Lat:</b> ${marker.position.lat()}</li>
        <li><b>Lng:</b> ${marker.position.lng()}</li>
      </ul>
      `;

    addInfoWindowToMarker(aboutLocation, marker, map);
  }

  // Un-comment this to execute code in moreDemos.js
  // initMoreDemos(map);
}


/**
 * Utility/helper functions
 */

function addMarker(icon, position, title, map) {
  const marker = new google.maps.Marker({ position, map, title, icon });

  return marker;
}

function addInfoWindowToMarker(content, marker, map) {
  const infoWindow = new google.maps.InfoWindow({
    content,
    maxWidth: 200
  });

  marker.addListener('click', () => infoWindow.open(map, marker));
}

