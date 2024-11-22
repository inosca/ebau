const { L } = window;

export function LatLngToEPSG2056(coordinates) {
  const arr = Array.isArray(coordinates)
    ? coordinates
    : [coordinates.lat, coordinates.lng];
  return L.CRS.EPSG2056.project(L.latLng(arr));
  // let arr = null;
  // if (Array.isArray(coordinates)) {
  //   arr = coordinates;
  // } else if (coordinates.lat) {
  //   arr = [coordinates.lat, coordinates.lng];
  // } else if (coordinates.j) {
  //   arr = [coordinates.x, coordinates.y];
  // } else {
  //   console.error("Did not find any coordinates in", coordinates);
  //   throw new Error("Missing coordinates");
  // }
  // return L.CRS.EPSG2056.project(L.latLng(arr));
}

export function EPSG2056toLatLng([x, y]) {
  return L.CRS.EPSG2056.unproject(new L.point(x, y));
}

// convert a bounding box string like BOX(2749071.92 1202980.44,2760298.25 1211211.74) to a nested array of coordinates
export function boxToBounds(boxString) {
  return boxString
    .replace("BOX(", "")
    .replace(")", "")
    .split(",")
    .map((s) => s.split(" ").map(parseFloat))
    .map(EPSG2056toLatLng);
}

export function getCenter(markers, geometry) {
  if (!markers || !markers.length) {
    return null;
  }
  if (geometry === "POLYGON" && markers.length > 2) {
    return LatLngToEPSG2056(L.polygon(markers).getBounds().getCenter());
  } else if (geometry === "POINT") {
    return LatLngToEPSG2056(markers[0]);
  }
  return LatLngToEPSG2056(L.polyline(markers).getBounds().getCenter());
}
