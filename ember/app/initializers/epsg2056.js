/* global L */

const RESOLUTIONS = [
  4000,
  3750,
  3500,
  3250,
  3000,
  2750,
  2500,
  2250,
  2000,
  1750,
  1500,
  1250,
  1000,
  750,
  650,
  500,
  250,
  100,
  50,
  20,
  10,
  5,
  2.5,
  2,
  1.5,
  1,
  0.5
]

export function initialize() {
  L.CRS.EPSG2056 = new L.Proj.CRS(
    'EPSG:2056',
    '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs',
    {
      resolutions: RESOLUTIONS,
      origin: [2420000, 1350000]
    }
  )
}

export default {
  initialize
}
