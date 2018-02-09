import LeafletMapComponent from 'ember-leaflet/components/leaflet-map'

const LEAFLET_OPTIONS = ['center', 'zoom', 'preferCanvas']

export default LeafletMapComponent.extend({
  preferCanvas: true,
  leafletOptions: LEAFLET_OPTIONS
})
