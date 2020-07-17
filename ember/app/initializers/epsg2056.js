/* global L */

const RESOLUTIONS = [50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.05];

export function initialize() {
  L.CRS.EPSG2056 = new L.Proj.CRS(
    "EPSG:2056",
    "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs",
    {
      resolutions: RESOLUTIONS,
      origin: [2420000, 1350000],
    }
  );

  L.CRS.EPSG21781 = new L.Proj.CRS(
    "EPSG:21781",
    "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +towgs84=674.4,15.1,405.3,0,0,0,0 +units=m +no_defs",
    {
      resolutions: RESOLUTIONS,
      origin: [420000, 350000],
    }
  );
}

export default {
  initialize,
};
