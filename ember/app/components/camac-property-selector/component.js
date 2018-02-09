/* global L, leafletImage */
import Component from '@ember/component'
import { inject as service } from '@ember/service'
import { scheduleOnce } from '@ember/runloop'
import { task, timeout } from 'ember-concurrency'
import { Promise } from 'rsvp'

const LAYERS = [
  'ch.sz.a055a.kantonsgrenze',
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
  classNames: ['uk-width-1-1', 'uk-width-xxlarge@m', 'uk-card-default'],
  lat: CENTER[0],
  lng: CENTER[1],
  zoom: 11,
  opacity: 0.9,
  minZoom: 10,
  layers: LAYERS.join(','),
  maxBounds: BOUNDS,

  ajax: service(),

  point: null,
  feature: null,
  property: null,

  handleSearch: task(function*(query) {
    yield timeout(500)

    try {
      let { features } = yield this.get('ajax').request(
        // TODO: Proxy to backend
        'https://cors-anywhere.herokuapp.com/https://map.geo.sz.ch/main/wsgi/fulltextsearch',
        {
          method: 'GET',
          data: {
            query,
            limit: 20
          }
        }
      )

      return features
    } catch (e) {} // eslint-disable-line no-empty
  }).restartable(),

  handleSearchSelection: task(function*(result) {
    if (
      result.geometry.type === 'Polygon' &&
      LAYERS.includes(result.properties.layer_name)
    ) {
      let { bbox, properties: { label }, geometry: { coordinates } } = result

      let [, number, municipality] = label.match(/^(\d+) (.+) (?=\()/)

      let property = {
        polygon: coordinates[0].map(xy => EPSG2056toLatLng(...xy)),
        bounds: [[bbox[0], bbox[1]], [bbox[2], bbox[3]]],
        number,
        municipality
      }

      scheduleOnce('afterRender', () => {
        this.set('property', property)
      })
    } else if (result.geometry.type === 'Point') {
      let point = {
        label: result.properties.label,
        coordinates: EPSG2056toLatLng(...result.geometry.coordinates)
      }

      scheduleOnce('afterRender', () => {
        this.set('point', point)
      })
    } else if (result.geometry.type === 'Polygon') {
      let feature = result.geometry.coordinates[0].map(xy =>
        EPSG2056toLatLng(...xy)
      )

      scheduleOnce('afterRender', () => {
        this.set('feature', feature)
      })
    }

    yield this.get('clear').perform()
  }),

  handleClick: task(function*(e) {
    let { x: width, y: height } = e.target.getSize()
    let { x, y } = e.containerPoint

    let northEast = L.CRS.EPSG3857.project(e.target.getBounds().getNorthEast())
    let southWest = L.CRS.EPSG3857.project(e.target.getBounds().getSouthWest())

    let bbox = [southWest.x, southWest.y, northEast.x, northEast.y].join(',')

    try {
      let data = yield this.get('ajax').request(
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

      let infos = data.getElementsByTagName(
        'ch.sz.a018.amtliche_vermessung.liegenschaften.liegenschaft.polygon_feature'
      )[0]

      if (infos) {
        let property = {
          bounds: infos
            .querySelector('boundedBy')
            .querySelector('coordinates')
            .textContent.split(' ')
            .map(xy => xy.split(',').map(Number))
            .filter(xy => xy.length === 2),
          polygon: infos
            .querySelector('geometry')
            .querySelector('coordinates')
            .textContent.split(' ')
            .map(xy => xy.split(',').map(Number))
            .filter(xy => xy.length === 2)
            .map(xy => EPSG3857toLatLng(...xy)),
          number: infos.querySelector('nummer').textContent,
          municipality: infos.querySelector('gde_nm').textContent
        }

        yield this.get('clear').perform()

        scheduleOnce('afterRender', () => {
          this.set('property', property)
        })
      }
    } catch (e) {} // eslint-disable-line no-empty
  }).restartable(),

  centerLayerToPolygon: task(function*(e) {
    this.set('point', null) // remove marked point since we selected a property

    e.target._map.fitBounds(e.target.getBounds())

    yield timeout(500) // wait for the pan animation to finish
  }).enqueue(),

  centerLayerToPoint: task(function*(e) {
    e.target._map.panTo(e.target.getLatLng())

    yield timeout(500) // wait for the pan animation to finish
  }).enqueue(),

  clear: task(function*() {
    yield this.setProperties({ point: null, property: null, feature: null })
  }).restartable(),

  submit: task(function*() {
    yield timeout()

    let image = yield this.get('createImage.last')

    this.get('on-submit')(image)
  }).drop(),

  createImage: task(function*(e) {
    yield this.get('centerLayerToPolygon').perform(e)

    return yield new Promise(resolve => {
      leafletImage(e.target._map, (_, canvas) => resolve(canvas.toDataURL()))
    })
  }).restartable()
})
