/* global L */
import Component from '@ember/component'
import { inject as service } from '@ember/service'
import { task, timeout } from 'ember-concurrency'
import { Promise, resolve, all } from 'rsvp'
import { computed } from '@ember/object'
import { A } from '@ember/array'
import html2canvas from 'html2canvas'
import { xml2js } from 'xml-js'
import { scheduleTask } from 'ember-lifeline'

const LAYERS = [
  'ch.sz.a055a.kantonsgrenze',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht.polygon',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer.position',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer.hilfslinie',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht_projektiert',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrecht_projektiert.polygon',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer_projektiert.position',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.selbstrechtnummer_projektiert.hilfslinie',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.grundstueck',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftsnummer.position',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftsnummer.hilfslinie',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft_projektiert',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft_projektiert.polygon',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftnummer_projektiert.position',
  'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaftnummer_projektiert.hilfslinie'
]

const CENTER = [47.020714, 8.652988]
const BOUNDS = [[47.486735, 8.21091], [46.77421, 9.20474]]

const EPSG3857toLatLng = (x, y) => L.CRS.EPSG3857.unproject(L.point(x, y))
const EPSG2056toLatLng = (x, y) => L.CRS.EPSG2056.unproject(L.point(x, y))

export default Component.extend({
  lat: CENTER[0],
  lng: CENTER[1],
  zoom: 11,
  opacity: 0.9,
  minZoom: 10,
  layers: LAYERS.join(','),
  maxBounds: BOUNDS,

  ajax: service(),
  notification: service(),

  _map: null,

  init() {
    this._super(...arguments)

    this.initSelection.perform()
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
          } = await this.ajax.request('/maps/main/wsgi/fulltextsearch', {
            method: 'GET',
            data: {
              query: parcel.egrid,
              limit: 1
            }
          })

          return {
            ...parcel,
            coordinates: coordinates.map(xy => EPSG2056toLatLng(...xy))
          }
        })
      )

      this.set('selected.parcels', parcels)
    }

    this.setProperties({
      parcels: this.selected.parcels || A(),
      points: this.selected.points || A(),
      _parcelLayers: A()
    })
  }).restartable(),

  parcelBounds: computed('_parcelLayers.[]', function() {
    return L.featureGroup(this._parcelLayers).getBounds()
  }),

  handleSearch: task(function*(query) {
    yield timeout(500)

    try {
      let { features } = yield this.ajax.request(
        '/maps/main/wsgi/fulltextsearch',
        {
          method: 'GET',
          data: {
            query,
            limit: 20
          }
        }
      )

      return features
    } catch (e) {
      this.notification.danger(
        'Es kann keine Verbindung zu GIS Server hergestellt werden'
      )
    }
  }).restartable(),

  handleSearchSelection: task(function*(result) {
    if (result.geometry.type === 'Point') {
      yield this.set('_point', EPSG2056toLatLng(...result.geometry.coordinates))
    }

    if (result.geometry.type === 'Polygon') {
      yield this.set(
        '_polygon',
        result.geometry.coordinates[0].map((x, y) => EPSG2056toLatLng(x, y))
      )
    }
  }).restartable(),

  handleLoad: task(function*({ target }) {
    yield this.set('_map', target)
  }),

  handleClick: task(function*(e) {
    if (this.readonly) {
      return
    }

    let { x: width, y: height } = e.target.getSize()
    let { x, y } = e.containerPoint

    let northEast = L.CRS.EPSG3857.project(e.target.getBounds().getNorthEast())
    let southWest = L.CRS.EPSG3857.project(e.target.getBounds().getSouthWest())

    let bbox = [southWest.x, southWest.y, northEast.x, northEast.y].join(',')

    try {
      let data = yield this.ajax.request(
        'https://map.geo.sz.ch/main/wsgi/mapserv_proxy',
        {
          dataType: 'xml',
          data: {
            x,
            y,
            bbox,
            width,
            height,
            version: '1.1.1',
            request: 'GetFeatureInfo',
            service: 'WMS',
            styles: 'default',
            layers:
              'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon',
            query_layers:
              'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon',
            srs: 'EPSG:3857',
            info_format: 'application/vnd.ogc.gml',
            feature_count: 1
          }
        }
      )

      const serializer = new XMLSerializer()

      const {
        msGMLOutput: {
          'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon_layer': {
            'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon_feature': {
              egrid: { _text: egrid },
              nummer: { _text: number },
              gde_nm: { _text: municipality },
              geometry: {
                'gml:Polygon': {
                  'gml:outerBoundaryIs': {
                    'gml:LinearRing': {
                      'gml:coordinates': { _text: rawCoordinates }
                    }
                  }
                }
              }
            }
          }
        }
      } = xml2js(serializer.serializeToString(data), { compact: true })

      const coordinates = rawCoordinates
        .split(' ')
        .map(xy => xy.split(',').map(Number))
        .filter(xy => xy.length === 2)
        .map(xy => EPSG3857toLatLng(...xy))

      const existing = this.parcels.findBy('egrid', egrid)

      if (!existing) {
        this.parcels.pushObject({ egrid, municipality, number, coordinates })
      }

      this.points.pushObject(e.latlng)
    } catch (e) {} // eslint-disable-line no-empty
  }).restartable(),

  handleAddParcelLayer: task(function*({ target }) {
    yield this._parcelLayers.pushObject(target)

    scheduleTask(this, 'actions', () => {
      this._map.fitBounds(this.parcelBounds)
    })
  }).enqueue(),

  centerLayerToPolygon: task(function*(e) {
    yield e.target._map.fitBounds(e.target.getBounds())
  }).enqueue(),

  centerLayerToPoint: task(function*(e) {
    yield e.target._map.panTo(e.target.getLatLng())
    yield e.target._map.setZoom(18)
  }).enqueue(),

  clear: task(function*() {
    yield this.setProperties({
      parcels: A(),
      points: A(),
      _parcelLayers: A(),
      _point: null,
      _feature: null
    })
  }).restartable(),

  reset: task(function*() {
    yield this.clear.perform()
    yield this.initSelection.perform()
  }).restartable(),

  submit: task(function*() {
    yield this._map.fitBounds(this.parcelBounds)

    yield timeout(500) // wait for the pan animation to finish

    let canvas = yield html2canvas(this._map._container, {
      logging: false,
      useCORS: true
    })

    let image = yield new Promise(resolve => canvas.toBlob(resolve))

    yield resolve(this['on-submit'](this.parcels, this.points, image))
  }).drop()
})
