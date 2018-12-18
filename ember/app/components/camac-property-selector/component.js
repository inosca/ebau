/* global L */
import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { task, timeout } from "ember-concurrency";
import { Promise, resolve, all } from "rsvp";
import { computed, setProperties } from "@ember/object";
import { A } from "@ember/array";
import html2canvas from "html2canvas";
import { xml2js } from "xml-js";

const LAYERS = [
  "ch.sz.a055a.kantonsgrenze",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht.polygon",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer.position",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer.hilfslinie",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht_projektiert",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht_projektiert.polygon",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer_projektiert.position",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer_projektiert.hilfslinie",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.grundstueck",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftsnummer.position",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftsnummer.hilfslinie",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft_projektiert",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft_projektiert.polygon",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftnummer_projektiert.position",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftnummer_projektiert.hilfslinie"
];

const QUERY_LAYERS = [
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon",
  "ch.sz.afk.afk_kigbo",
  "ch.sz.afk.afk_bhf",
  "ch.sz.afk.afk_isos",
  "ch.sz.a081a.icomos.gaerten",
  //"ch.sz.afu.nis.hochspannungsltg",
  //"ch.sz.afu.nis.trafostation",
  //"ch.sz.afu.nis.unterwerk",
  "ch.sz.a023a.egid",
  "ch.sz.a018.amtliche_vermessung.bodenbedeckung.gebaeudenummer_projektiert",
  "ch.sz.a018.amtliche_vermessung.bodenbedeckung.gebaeudenummer",
  "ch.sz.a006.swisstlm3d.gewaesser.stehendesgewaesser",
  "ch.sz.a006.swisstlm3d.gewaesser.fliessgewaesser",
  //"ch.sz.awb.grp.awb_gewaesserraum",
  //"ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft",
  //"ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft_projektiert",
  //"ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht",
  //"ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht_projektiert",
  "ch.sz.afu.nis.mobilfunkstandort",
  "ch.sz.afu.nis.rundfunksender",
  //"ch.sz.awn.a012.grp.naturgefahrenkarte.synoptisch",
  "ch.sz.anjf.anjf_kant_naturschutzgebiete",
  "ch.sz.anjf.anjf_kant_pflanzenschutzreservate",
  "ch.sz.anjf.komm_schutzzonen",
  "ch.sz.anjf.anjf_kant_biotope",
  "ch.sz.a005.nutzungsplanung.grundnutzung",
  "ch.sz.a013a.planerischergewaesserschutz.gwszonen.status.gwszone",
  "ch.sz.a013a.planerischergewaesserschutz.gwszonen.gwsareal",
  "ch.sz.a013a.planerischergewaesserschutz.gsbereiche.bereich.ao",
  "ch.sz.a013a.planerischergewaesserschutz.gsbereiche.bereich.au",
  //"ch.sz.afu.kbsprov.provisorische_standorte",
  "ch.sz.a006.swisstlm3d.oev.eisenbahn",
  "ch.sz.a078.wanderwege",
  //"ch.sz.chbafu.wildtierkorridor",
  //"ch.sz.a049.fischgewaesser",
  "ch.sz.a049.fischregionen",
  "ch.sz.anjf_reptiliengebiete.reptiliengebiet"
];

const CENTER = [47.020714, 8.652988];
const BOUNDS = [[47.486735, 8.21091], [46.77421, 9.20474]];

//const EPSG3857toLatLng = (x, y) => L.CRS.EPSG3857.unproject(L.point(x, y));
const LatLngToEPSG3857 = (lat, lng) =>
  L.CRS.EPSG3857.project(L.latLng(lat, lng));
const EPSG2056toLatLng = (x, y) => L.CRS.EPSG2056.unproject(new L.point(x, y));

export default Component.extend({
  lat: CENTER[0],
  lng: CENTER[1],
  zoom: 11,
  opacity: 0.9,
  minZoom: 10,
  layers: LAYERS.join(","),
  maxBounds: BOUNDS,
  points: A(),
  parcels: A(),
  affectedLayers: null,
  selectedSearchResult: null,
  selectedMunicipality: null,

  ajax: service(),
  notification: service(),

  _map: null,

  init() {
    this._super(...arguments);

    this.initSelection.perform();
  },

  initSelection: task(function*() {
    if (this.selected.parcels) {
      let parcels = yield all(
        this.selected.parcels.map(async parcel => {
          let {
            features: [
              {
                geometry: {
                  coordinates: [coordinates]
                }
              }
            ]
          } = await this.ajax.request("/maps/main/wsgi/fulltextsearch", {
            method: "GET",
            data: {
              query: parcel.egrid,
              limit: 1
            }
          });

          return {
            ...parcel,
            coordinates: coordinates.map(xy => EPSG2056toLatLng(...xy))
          };
        })
      );

      this.set("selected.parcels", parcels);
    }

    this.setProperties({
      parcels: this.selected.parcels || A(),
      points: this.selected.points || A()
    });

    if (this.selected.municipality) {
      this.selectedMunicipality = this.selected.municipality;
    }
  }).restartable(),

  parcelBounds: computed("parcels.[]", function() {
    if (this.get("parcels")) {
      return L.featureGroup(
        this.get("parcels").map(p => L.polyline(p.coordinates))
      ).getBounds();
    }
  }),

  /**
   * The selection needs to be a plain js array because
   * ember-leaflet can not handle EmberArrays
   */
  selection: computed("points.@each.{lat,lng}", function() {
    return this.get("points").toArray();
  }),

  municipalities: computed("parcels.[]", function() {
    return this.get("parcels").reduce((muniList, parcel) => {
      if (!muniList.includes(parcel.municipality)) {
        muniList.push(parcel.municipality);
      }
      return muniList;
    }, []);
  }),

  setMunicipality: task(function*(municipality) {
    yield this.set("selectedMunicipality", municipality);
  }),

  handleSearch: task(function*(query) {
    yield timeout(500);

    try {
      let { features } = yield this.ajax.request(
        "/maps/main/wsgi/fulltextsearch",
        {
          method: "GET",
          data: {
            query,
            limit: 50
          }
        }
      );

      return features;
    } catch (e) {
      this.notification.danger(
        "Die Verbindung zum GIS Server ist fehlgeschlagen"
      );
    }
  }).restartable(),

  handleSearchSelection: task(function*(result) {
    this.set("selectedSearchResult", result);

    if (!result) {
      yield this.parcels.length && this.focusOnParcels.perform();
      return;
    }

    if (result.geometry.type === "Point") {
      yield this.setProperties(
        EPSG2056toLatLng(...result.geometry.coordinates)
      );
      yield this.set("zoom", 18);
    }

    if (result.geometry.type === "Polygon") {
      yield this._map.fitBounds(
        result.geometry.coordinates[0].map((x, y) => EPSG2056toLatLng(x, y))
      );
    }
  }).restartable(),

  handleLoad: task(function*({ target }) {
    yield this.set("_map", target);
  }),

  addPoint: task(function*(e) {
    if (this.readonly) {
      return;
    }

    yield this.points.pushObject({ ...e.latlng });
  }).enqueue(),

  getLayers: task(function*() {
    const coordinates = this.get("points")
      .map(p => {
        const coor = LatLngToEPSG3857(p.lat, p.lng);
        return `${coor.x},${coor.y}`;
      })
      .join(" ");

    let type = "Polygon";
    let geometryFilter = `<gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>${coordinates}</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs>`;

    if (this.get("points").length === 1) {
      type = "Point";
      geometryFilter = `<gml:coordinates>${coordinates}</gml:coordinates>`;
    } else if (this.get("points").length === 2) {
      type = "LineString";
      geometryFilter = `<gml:coordinates>${coordinates}</gml:coordinates>`;
    }

    const fuzzyFilter = `<ogc:Filter xmlns="http://www.opengis.net/ogc"><ogc:DWithin><ogc:Distance units="meter">15</ogc:Distance><ogc:PropertyName>*</ogc:PropertyName><gml:${type} srsName="urn:ogc:def:crs:EPSG::3857">${geometryFilter}</gml:${type}></ogc:DWithin></ogc:Filter>`;

    const exactFilter = `<ogc:Filter xmlns="http://www.opengis.net/ogc"><ogc:Intersects><ogc:PropertyName>*</ogc:PropertyName><gml:${type} srsName="urn:ogc:def:crs:EPSG::3857">${geometryFilter}</gml:${type}></ogc:Intersects></ogc:Filter>`;

    const layers = QUERY_LAYERS.map(l => {
      const exact =
        l ===
        "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon";
      return `<wfs:Query typeName="${l}">${
        exact ? exactFilter : fuzzyFilter
      }</wfs:Query>`;
    }).join(",");

    const response = yield this.ajax.request(
      "https://map.geo.sz.ch/main/wsgi/mapserv_proxy",
      {
        method: "POST",
        dataType: "xml",
        contentType: "text/xml",
        data: `<wfs:GetFeature version="1.1.0" service="wfs" srsName="EPSG:3857">${layers}</wfs:GetFeature>`
      }
    );
    const serializer = new XMLSerializer();
    const responseObject = xml2js(serializer.serializeToString(response), {
      compact: true
    });

    this._parseAffectedLayers(responseObject);
    this._parseAffectedParcels(responseObject);
  }).restartable(),

  _parseAffectedLayers(wfsResponse) {
    const layers = wfsResponse["wfs:FeatureCollection"][
      "gml:featureMember"
    ].map(fm => {
      return Object.getOwnPropertyNames(fm).firstObject;
    });
    const layerSet = new Set(layers);
    this.set("affectedLayers", [...layerSet]);
  },

  _parseAffectedParcels(wfsResponse) {
    const parcels = A();

    wfsResponse["wfs:FeatureCollection"]["gml:featureMember"].forEach(fm => {
      if (
        !fm.hasOwnProperty(
          "ms:ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon"
        )
      ) {
        return;
      }

      const {
        "ms:ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon": {
          "ms:egrid": { _text: egrid },
          "ms:gde_nm": { _text: municipality },
          "ms:nummer": { _text: number },
          "ms:geometry": {
            "gml:Polygon": {
              "gml:exterior": {
                "gml:LinearRing": {
                  "gml:posList": { _text: rawCoordinates }
                }
              }
            }
          }
        }
      } = fm;

      const coordinatesEPSG2056 = rawCoordinates
        .split(" ")
        .filter(point => point)
        .map(Number);

      const coordinatesLatLng = [];
      for (let i = 0; i < coordinatesEPSG2056.length; i += 2) {
        coordinatesLatLng.push(
          EPSG2056toLatLng(...coordinatesEPSG2056.slice(i, i + 2))
        );
      }

      parcels.pushObject({
        egrid,
        municipality,
        number,
        coordinates: coordinatesLatLng
      });
    });

    this.set("parcels", parcels);
    this.focusOnParcels.perform();
  },

  focusOnParcels: task(function*() {
    yield this._map.fitBounds(this.parcelBounds);
  }).enqueue(),

  clear: task(function*() {
    yield this.setProperties({
      parcels: A(),
      points: A(),
      affectedLayers: null,
      selectedMunicipality: null
    });
  }).restartable(),

  reset: task(function*() {
    yield this.clear.perform();
    yield this.initSelection.perform();
  }).restartable(),

  submit: task(function*() {
    yield this.focusOnParcels.perform();

    yield timeout(500); // wait for the pan animation to finish

    let canvas = yield html2canvas(this._map._container, {
      logging: false,
      useCORS: true
    });

    let image = yield new Promise(resolve => canvas.toBlob(resolve));

    // If no municipality is selected, choose the first possible one
    const municipality = this.selectedMunicipality
      ? this.selectedMunicipality
      : this.municipalities.get("firstObject");

    yield resolve(
      this["on-submit"](this.parcels, this.points, image, municipality)
    );
  }).drop(),

  updatePoint: task(function*(point, e) {
    const location = e.target.getLatLng();
    yield setProperties(this.points.find(p => p === point), location);
  }).enqueue()
});
