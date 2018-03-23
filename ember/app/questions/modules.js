/**
 * This file defines which modules contain which submodules and questions.
 */

export default {
  b: {
    title: 'Grundinformationen',
    questions: [],
    submodules: {
      1: {
        title: 'Lokalisierung',
        questions: []
      },
      2: {
        title: 'Kategorisierung',
        questions: [
          'kategorie-des-vorhabens',
          'art-der-nutzung',
          'vorhaben-mit-anlage',
          'art-der-anlage',
          'art-der-befestigten-flache',
          'zweck-der-leitungen',
          'art-der-warmepumpe',
          'tangiert-vorhaben-strasse',
          'pfahlfundation-vorgesehen',
          'baugrubenumschliessung-vorgesehen',
          'temporare-grundwasserabsenkung-notig',
          'anlagen-mit-erheblichen-schadstoffemissionen',
          'anlagen-mit-erheblichen-schadstoffemissionen-welche',
          'anlagen-mit-erheblichen-strahlungsemissionen',
          'anlagen-mit-erheblichen-strahlungsemissionen-welche',
          'anlagen-mit-erheblichen-larmemissionen',
          'larmbelastetes-gebiet',
          'aussenbeleuchtung',
          'wassergefahrdende-stoffe',
          'brandschutztechnisch-gefahrliche-stoffe',
          'bodenbelastungen',
          'boden-5000m2',
          'ordendliche-mindestabstande',
          'auswirkungen-auf-arbeitnehmer',
          '200m3-bauabfalle',
          'alarmierungseinrichtung-tangiert',
          'lebensmittel-umgehen',
          'trinkwasser-abgeben',
          'offentlich-duschanlage-oder-bad',
          'gewerbliche-nutzflachen',
          'hohe-der-anlage'
        ]
      },
      3: {
        title: 'Allgemeine Informationen zum Vorhaben',
        questions: [
          'geometer',
          'baugespann-errichtet',
          'kein-baugespann-begrundung',
          'baukosten',
          'gebaudevolumen'
        ]
      },
      4: {
        title: 'Ausnahmebewilligungen',
        questions: ['ausnahmen', 'ausnahmen-begrundung']
      }
    }
  },
  c: {
    title: 'Personalien',
    questions: [],
    submodules: {
      1: {
        title: 'Grundeigentümerschaft',
        questions: ['grundeigentumerschaft']
      },
      2: {
        title: 'Bauherrschaft',
        questions: ['bauherrschaft']
      },
      3: {
        title: 'Projektverfasser / Planer',
        questions: ['projektverfasser-planer']
      }
    }
  }
}
