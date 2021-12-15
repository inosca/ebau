import EmberRouter from "@ember/routing/router";

import config from "./config/environment";

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

const resetNamespace = true;

/* eslint-disable-next-line array-callback-return */
Router.map(function () {
  this.route("login");
  this.route("logout");
  this.route("app-shell");
  this.route("notfound", { path: "/*path" });

  this.route("protected", { path: "/" }, function () {
    this.route("index", { path: "/", resetNamespace });
    this.route("publications", { path: "/publikationen", resetNamespace });
    this.route("instances", { path: "/gesuche", resetNamespace }, function () {
      this.route("new");
      this.route("edit", { path: "/:instance_id" }, function () {
        this.route("grundinformationen", function () {
          this.route("lokalisierung");
          this.route("kategorisierung");
          this.route("kategorisierung-vorabklarung");
          this.route("gwr");
          this.route("gwr-v2");
          this.route("allgemeine-informationen-zum-vorhaben");
          this.route("allgemeine-informationen-zum-vorhaben-v2");
          this.route("allgemeine-informationen-zum-vorhaben-v3");
          this.route("ausnahmebewilligungen");
          this.route("migriertes-dossier");
        });
        this.route("migriertes-dossier");
        this.route("personalien", function () {
          this.route("grundeigentumerschaft");
          this.route("bauherrschaft");
          this.route("bauherrschaft-v2");
          this.route("projektverfasser-planer");
          this.route("projektverfasser-planer-v2");
          this.route("gesuchsteller");
          this.route("konzessionsnehmer");
          this.route("bewilligungsnehmer");
          this.route("vertreter-mit-vollmacht");
        });
        this.route("fachthemen", function () {
          this.route("landwirtschaft");
          this.route(
            "nicht-landwirtschaftliche-bauten-und-anlagen-ausserhalb-bauzone"
          );
          this.route("umweltschutz");
          this.route("natur-und-landschaftsschutz");
          this.route("wald");
          this.route("naturgefahren");
          this.route("verkehr");
          this.route("energie");
          this.route("arbeitssicherheit-und-gesundheitsschutz");
          this.route("zivilschutz");
          this.route("brandschutz");
          this.route("liegenschaftsentwasserung");
          this.route("gewasserschutz");
          this.route("grundwasser-und-altlasten");
          this.route("reklamen");
          this.route("denkmalschutz-und-archaeologie");
          this.route("lebensmittel-und-hygienesicherheit");
          this.route("fischerei");
        });
        this.route("geschaeftskontrolle");
        this.route("gesuchsunterlagen");
        this.route("gesuchsunterlagen-ve-va");
        this.route("anlassbewilligungen-verkehrsbewilligungen");
        this.route("baumeldung-fur-geringfugige-vorhaben");
        this.route("baumeldung-fur-geringfugige-vorhaben-v2");
        this.route("konzession-fur-wasserentnahme");
        this.route("projektanderung");
        this.route("projektgenehmigungsgesuch");
        this.route("plangenehmigungsverfahren");
        this.route("technische-bewilligung");
        this.route("vorentscheid");
        this.route("submit");

        // Routes for the horizontal nav
        this.route("involvierte-personen");
        this.route("freigegebene-unterlagen");
        this.route("publikationsdokumente");
        this.route("work-items", { path: "/aufgaben" }, function () {
          this.route("detail", { path: "/:work_item_id" });
        });
      });
    });
  });
});
