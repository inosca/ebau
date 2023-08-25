import { CRS } from "proj4leaflet";

export const LV95 = {
  epsg: "EPSG:2056",
  def: [
    "+proj=somerc",
    "+lat_0=46.95240555555556",
    "+lon_0=7.439583333333333",
    "+k_0=1",
    "+x_0=2600000",
    "+y_0=1200000",
    "+ellps=bessel",
    "+towgs84=674.374,15.056,405.346,0,0,0,0",
    "+units=m",
    "+no_defs",
  ].join(" "),
  resolutions: [
    4000, 2000, 1000, 500, 250, 100, 50, 20, 10, 5, 2.5, 1.0, 0.5, 0.25, 0.1,
    0.05,
  ],
  origin: [2420000, 1350000],
};

export const LV95_CRS = new CRS(LV95.epsg, LV95.def, {
  resolutions: LV95.resolutions,
  origin: LV95.origin,
});
