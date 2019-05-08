import Component from "@ember/component";
import { computed } from "@ember/object";

export default Component.extend({
  classNames: ["gis-map"],

  link: computed(function() {
    const isReadOnly = false;
    const eGrid = "EGRID";
    return (
      "https://www.map.apps.be.ch/pub/client_mapwidget/default.jsp?baseURL=https://www.map.apps.be.ch/pub" +
      "&project=a42pub_ebau_cl" +
      "&map_adv=true" +
      "&useXD=true" +
      "&linked_view=true" +
      "&view=Grundstuecke / Parcelles 1:6000" +
      "&basemapview=HK_Hintergrund_bunt" +
      "&activetools=NAVIGATION%20VIEW" +
      (!isReadOnly ? "%20ADDREMOVE%20FTS" : "") +
      (!isReadOnly ? "&startmode=FTS" : "") +
      "&callback_active_tool=activeToolResult" +
      "&query=Suche_EBAU_DIPANU" +
      "&keyname=EGRID" +
      "&keyvalue=" +
      eGrid +
      "&returnkey=EGRID;GSTBEZ;PROJSTAT" +
      "&callback_addremove_mw=addremoveResult" +
      "&retainSelection=true" +
      (!isReadOnly ? "&callback_fts_mw=ftsResult&fts_search=true" : "")
    ); // Full-text search
  })
});
