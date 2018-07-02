import EmberRouter from '@ember/routing/router'
import config from './config/environment'

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
})

const resetNamespace = true

Router.map(function() {
  this.route('login')
  this.route('app-shell')
  this.route('notfound', { path: '/*path' })

  this.route('protected', { path: '/' }, function() {
    this.route('index', { path: '/', resetNamespace })
    this.route('instances', { path: '/dossiers', resetNamespace }, function() {
      this.route('new')
      this.route('edit', { path: '/:instance_id' }, function() {
        this.route('grundinformationen', function() {
          this.route('lokalisierung')
          this.route('kategorisierung')
          this.route('gwr')
          this.route('allgemeine-informationen-zum-vorhaben')
          this.route('ausnahmebewilligungen')
        })
        this.route('personalien', function() {
          this.route('grundeigentumerschaft')
          this.route('bauherrschaft')
          this.route('projektverfasser-planer')
          this.route('gesuchsteller')
          this.route('konzessionsnehmer')
          this.route('bewilligungsnehmer')
        })
        this.route('fachthemen', function() {
          this.route('landwirtschaft')
          this.route(
            'nicht-landwirtschaftliche-bauten-und-anlagen-ausserhalb-bauzone'
          )
          this.route('umweltschutz')
          this.route('wald')
          this.route('naturgefahren')
          this.route('verkehr')
          this.route('energie')
          this.route('arbeitssicherheit-und-gesundheitsschutz')
          this.route('zivilschutz')
          this.route('brandschutz')
          this.route('liegenschaftsentwasserung')
          this.route('gewasserschutz')
          this.route('grundwasser-und-altlasten')
          this.route('reklamen')
          this.route('lebensmittel-und-hygienesicherheit')
        })
        this.route('gesuchsunterlagen')
        this.route('gesuchsunterlagen-ve-va')
        this.route('anlassbewilligungen-verkehrsbewilligungen')
        this.route('baumeldung-fur-geringfugige-vorhaben')
        this.route('konzession-fur-wasserentnahme')
        this.route('projektanderung')
        this.route('projektgenehmigungsgesuch')
        this.route('plangenehmigungsverfahren')
        this.route('technische-bewilligung')
        this.route('vorentscheid')
        this.route('submit')
      })
    })
  })
})

export default Router
