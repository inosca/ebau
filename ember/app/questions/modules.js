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
        questions: ['art-des-vorhabens', 'vorgesehene-nutzung']
      },
      3: {
        title: 'Allgemeine Informationen zum Vorhaben',
        questions: []
      },
      4: {
        title: 'Ausnahmebewilligungen',
        questions: []
      }
    }
  },
  c: {
    title: 'Personalien',
    questions: [],
    submodules: {
      1: {
        title: 'Grundeigentümerschaft',
        questions: []
      }
    }
  }
}
