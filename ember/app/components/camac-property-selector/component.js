/* global L */
import { A } from "@ember/array";
import Component from "@ember/component";
import { computed, setProperties } from "@ember/object";
import { inject as service } from "@ember/service";
import ENV from "citizen-portal/config/environment";
import { task, timeout } from "ember-concurrency";
import html2canvas from "html2canvas";
import { Promise, resolve, all } from "rsvp";
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
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftnummer_projektiert.hilfslinie",
];

const QUERY_LAYERS = [
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon",
  "ch.sz.a133a.kantonales_schutzinventar",
  "ch.sz.a132b.bauernhausinventar",
  "ch.sz.afk.afk_isos",
  "ch.sz.a081a.icomos.gaerten",
  "ch.sz.a135a.nis.hochspannungsleitung",
  "ch.sz.a023a.egid",
  "ch.sz.a018.amtliche_vermessung.bodenbedeckung.gebaeudenummer_projektiert",
  "ch.sz.a018.amtliche_vermessung.bodenbedeckung.gebaeudenummer",
  "ch.sz.a154a.referenzgeometrie_standgewaesser.uferlinie",
  "ch.sz.a041b.gewaessernetz.mwert.karto",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon_oereb",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft_projektiert.polygon",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht.polygon",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht.polygon_oereb",
  "ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht_projektiert.polygon",
  "ch.sz.a012.naturgefahrenkarte.synoptisch",
  "ch.sz.anjf.anjf_kant_naturschutzgebiete",
  "ch.sz.anjf.anjf_kant_pflanzenschutzreservate",
  "ch.sz.anjf.komm_schutzzonen",
  "ch.sz.anjf.anjf_kant_biotope",
  "ch.sz.a013a.planerischergewaesserschutz.gwszonen.status.gwszone",
  "ch.sz.a013a.planerischergewaesserschutz.gwszonen.gwsareal",
  "ch.sz.a013a.planerischergewaesserschutz.gsbereiche.bereich.au",
  "ch.sz.a006.swisstlm3d.oev.eisenbahn",
  "ch.sz.a078.wanderwege",
  "ch.sz.chbafu.wildtierkorridor.national",
  "ch.sz.chbafu.wildtierkorridor.regional",
  "ch.sz.chbafu.wildtierkorridor.verbindung",
  "ch.sz.a049.fischgewaesser_bestehend",
  "ch.sz.a049.fischgewaesser_pot",
  "ch.sz.a049.fischregionen",
  "ch.sz.a143a.reptiliengebiet",
  "ch.sz.a082a.schutzbauten.gemeinde_sammelschutzraum",
  "ch.sz.a082a.schutzbauten.kulturgueter_schutzraum",
  "ch.sz.a082a.schutzbauten.oeffentlicher_sammelschutzraum",
  "ch.sz.a082a.schutzbauten.pflicht_schutzraum",
  "ch.sz.a082a.schutzbauten.pflicht_schutzraum_vor_twp",
  "ch.sz.a082a.schutzbauten.schutzanlage",
  "ch.sz.a105a.sirenen",
  "ch.sz.awb.awb_beh_verb_gewaesserraum",
  "ch.sz.a020a.kataster_belasteter_standorte",
  "ch.sz.a020a.kataster_belasteter_standorte_pnt",
];

const PARCEL_LAYER =
  "ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon";

const CENTER = [47.020714, 8.652988];

const LatLngToEPSG3857 = (lat, lng) =>
  L.CRS.EPSG3857.project(L.latLng(lat, lng));
const EPSG2056toLatLng = (x, y) => L.CRS.EPSG2056.unproject(new L.point(x, y));

export default Component.extend({
  crs: L.CRS.EPSG2056,
  lat: CENTER[0],
  lng: CENTER[1],
  zoom: 0,
  minZoom: 0,
  maxZoom: 11,
  layers: LAYERS.join(","),
  points: null,
  parcels: A(),
  affectedLayers: A(),
  searchObject: null,
  selectedSearchResult: null,
  selectedMunicipality: null,
  gisURL: `https://${ENV.APP.gisHost}/mapserv_proxy?ogcserver=source for image/png`,
  tileURL: `https://${ENV.APP.gisHost}/tiles/1.0.0/ch_sz_avg_ortsplan_farbig/default/201610/swissgrid_2056/{z}/{y}/{x}.png`,

  ajax: service(),
  notification: service(),

  _map: null,

  init(...args) {
    this._super(...args);
    this.points = [[]];
    this.initSelection.perform();
  },

  initSelection: task(function* () {
    if (this.selected.parcels) {
      const parcels = yield all(
        this.selected.parcels.map(async (parcel) => {
          const {
            features: [
              {
                geometry: {
                  coordinates: [coordinates],
                },
              },
            ],
          } = await this.ajax.request("/maps/search", {
            method: "GET",
            data: {
              query: parcel.egrid,
              limit: 1,
            },
          });

          return {
            ...parcel,
            coordinates: coordinates.map((xy) => EPSG2056toLatLng(...xy)),
          };
        })
      );

      this.set("selected.parcels", parcels);
    }

    // Backwards compatibilty check, for single polygon forms
    if (this.selected.points && "lat" in this.selected.points[0]) {
      this.selected.points = [this.selected.points];
    }

    this.setProperties({
      parcels: this.selected.parcels || A(),
      points: this.selected.points || [[]],
    });

    if (this.selected.municipality) {
      this.set("selectedMunicipality", this.selected.municipality);
    }
  }).restartable(),

  parcelBounds: computed("parcels.[]", function () {
    if (this.parcels) {
      return L.featureGroup(
        this.parcels.map((p) => L.polyline(p.coordinates))
      ).getBounds();
    }
    return [];
  }),

  pointsFlat: computed("points.@each.length", function () {
    // We use this instead of array.flat() to ensure support of older browsers
    return [].concat(...this.points);
  }),

  coordinates: computed("pointsFlat.@each.{lat,lng}", function () {
    // This computed property is used to update the polygons when a point is moved
    // we return a object with the flat array, because otherwise the computed property
    // doesn't get recomputed if we only return the points.
    return {
      points: this.points.map((p) => p.toArray()),
      flat: this.pointsFlat,
    };
  }),

  municipalities: computed("parcels.[],specialForm", function () {
    const municipalities = [
      ...new Set(this.parcels.map((p) => p.municipality)),
    ];
    let location = this.specialForm;

    if (this.specialForm === "district") {
      location = ENV.APP.districtMapping[municipalities.get("firstObject")];
    }

    return this.specialForm ? [location] : municipalities;
  }),

  setMunicipality: task(function* (municipality) {
    yield this.set("selectedMunicipality", municipality);
  }),

  handleSearch: task(function* (query) {
    yield timeout(500);

    try {
      const { features } = yield this.ajax.request("/maps/search", {
        method: "GET",
        data: {
          query,
          limit: 50,
        },
      });

      return features;
    } catch (e) {
      this.notification.danger(
        "Die Verbindung zum GIS Server ist fehlgeschlagen"
      );
    }
  }).restartable(),

  handleSearchSelection: task(function* (result) {
    this.set("selectedSearchResult", result);

    if (!result) {
      this.set("searchObject", null);
      yield this.parcels.length && this.focusOnParcels.perform();
      return;
    }

    if (result.geometry.type === "Point") {
      const latLngPoint = EPSG2056toLatLng(...result.geometry.coordinates);

      yield this.set("searchObject", latLngPoint);
      yield this._map.setView(latLngPoint, 11);
    }

    if (result.geometry.type === "Polygon") {
      const latLngPoints = result.geometry.coordinates[0].map((x, y) =>
        EPSG2056toLatLng(x, y)
      );

      yield this.set("searchObject", latLngPoints);
      yield this._map.fitBounds(latLngPoints);
    }
  }).restartable(),

  handleLoad: task(function* ({ target }) {
    yield this.set("_map", target);
  }),

  addPoint: task(function* (e) {
    if (this.readonly) {
      return;
    }

    yield this.get("points.lastObject").pushObject({ ...e.latlng });
  }).enqueue(),

  getLayers: task(function* () {
    this.setProperties({ parcels: A(), layers: A() });

    yield this.points.forEach(async (pointSet) => {
      if (!pointSet.length) {
        return;
      }

      const coordinates = pointSet
        .map((p) => {
          const coor = LatLngToEPSG3857(p.lat, p.lng);
          return `${coor.x},${coor.y}`;
        })
        .join(" ");

      let type = "Polygon";
      let geometryFilter = `<gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>${coordinates}</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs>`;

      if (pointSet.length === 1) {
        type = "Point";
        geometryFilter = `<gml:coordinates>${coordinates}</gml:coordinates>`;
      } else if (pointSet.length === 2) {
        type = "LineString";
        geometryFilter = `<gml:coordinates>${coordinates}</gml:coordinates>`;
      }

      const fuzzyFilter = `<ogc:Filter xmlns="http://www.opengis.net/ogc"><ogc:DWithin><ogc:Distance units="meter">15</ogc:Distance><ogc:PropertyName>*</ogc:PropertyName><gml:${type} srsName="urn:ogc:def:crs:EPSG::3857">${geometryFilter}</gml:${type}></ogc:DWithin></ogc:Filter>`;

      const exactFilter = `<ogc:Filter xmlns="http://www.opengis.net/ogc"><ogc:Intersects><ogc:PropertyName>*</ogc:PropertyName><gml:${type} srsName="urn:ogc:def:crs:EPSG::3857">${geometryFilter}</gml:${type}></ogc:Intersects></ogc:Filter>`;

      const layers = QUERY_LAYERS.map((layer) => {
        const exact = layer === PARCEL_LAYER;
        return `<wfs:Query typeName="${layer}">${
          exact ? exactFilter : fuzzyFilter
        }</wfs:Query>`;
      }).join(",");

      const response = await this.ajax.request(this.gisURL, {
        method: "POST",
        dataType: "xml",
        contentType: "text/xml",
        data: `<wfs:GetFeature version="1.1.0" service="wfs" srsName="EPSG:3857">${layers}</wfs:GetFeature>`,
      });
      const serializer = new XMLSerializer();
      const responseObject = xml2js(serializer.serializeToString(response), {
        compact: true,
      });

      if (
        !Array.isArray(
          responseObject["wfs:FeatureCollection"]["gml:featureMember"]
        )
      ) {
        responseObject["wfs:FeatureCollection"]["gml:featureMember"] = [
          responseObject["wfs:FeatureCollection"]["gml:featureMember"],
        ];
      }

      this._parseAffectedLayers(responseObject);
      this._parseAffectedParcels(responseObject);
    });
  }).restartable(),

  _parseAffectedLayers(wfsResponse) {
    const layers = wfsResponse["wfs:FeatureCollection"][
      "gml:featureMember"
    ].map((fm) => {
      return Object.getOwnPropertyNames(fm).firstObject;
    });
    const layerSet = new Set([...this.affectedLayers, ...layers]);
    this.set("affectedLayers", [...layerSet]);
  },

  _parseAffectedParcels(wfsResponse) {
    const parcels = A();

    wfsResponse["wfs:FeatureCollection"]["gml:featureMember"].forEach((fm) => {
      if (!Object.prototype.hasOwnProperty.call(fm, `ms:${PARCEL_LAYER}`)) {
        return;
      }

      const {
        "ms:ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon": {
          "ms:egrid": { _text: egrid },
          "ms:gde_nm": { _text: municipality },
          "ms:nummer": { _text: number },
          "ms:geom": {
            "gml:Polygon": {
              "gml:exterior": {
                "gml:LinearRing": {
                  "gml:posList": { _text: rawCoordinates },
                },
              },
            },
          },
        },
      } = fm;

      const coordinatesEPSG2056 = rawCoordinates
        .split(" ")
        .filter(Boolean)
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
        coordinates: coordinatesLatLng,
      });
    });

    this.set("parcels", [...this.parcels, ...parcels].uniqBy("egrid"));
    this.focusOnParcels.perform();
  },

  focusOnParcels: task(function* () {
    yield this._map.fitBounds(this.parcelBounds);
  }).enqueue(),

  addPointSet: task(function* () {
    if (this.get("points.lastObject.length")) {
      yield this.points.pushObject([]);

      this.notification.success(
        "Ein zusätzlicher Standort kann jetzt erfasst werden"
      );
    }
  }),

  clear: task(function* () {
    yield this.setProperties({
      points: [[]],
      parcels: A(),
      affectedLayers: A(),
      selectedMunicipality: null,
      searchObject: null,
    });
  }).restartable(),

  reset: task(function* () {
    yield this.clear.perform();
    yield this.initSelection.perform();
  }).restartable(),

  submit: task(function* () {
    yield this.focusOnParcels.perform();

    yield timeout(500); // wait for the pan animation to finish

    /**
     * Important note for html2canvas usage!
     * When the element you want to "screenshot" is not in the viewport when
     * you are a the top of the page, it will not find the element and create
     * an empty image. To fix this, manually add the x and y positions with
     * the `window.scrollX|Y` offset.
     */
    const canvas = yield html2canvas(this._map._container, {
      logging: false,
      useCORS: true,
      x: window.scrollX + this._map._container.getBoundingClientRect().left,
      y: window.scrollY + this._map._container.getBoundingClientRect().top,
    });
    const image = yield new Promise((resolve) => canvas.toBlob(resolve));

    // If no municipality is selected, choose the first possible one
    const municipality = this.selectedMunicipality
      ? this.selectedMunicipality
      : this.municipalities.get("firstObject");

    yield resolve(
      this["on-submit"](
        this.parcels,
        this.points.filter((p) => p.length),
        image,
        municipality,
        this.affectedLayers
      )
    );
  }).drop(),

  updatePoint: task(function* (point, e) {
    const location = e.target.getLatLng();
    yield setProperties(
      this.get("points.lastObject").find((p) => p === point),
      location
    );
  }).enqueue(),

  // Temporary function to check if the selected municipality is active
  checkMunicipality: computed("municipality", function () {
    if (!this.municipality) {
      return true;
    }

    return ENV.APP.municipalityNames.indexOf(this.municipality) >= 0;
  }),

  municipality: computed("municipalities", "selectedMunicipality", function () {
    return this.selectedMunicipality
      ? this.selectedMunicipality
      : this.municipalities.get("firstObject");
  }),
});
