export default {
  'art-des-vorhabens': {
    label: 'Handelt es sich beim Bauvorhaben um eine Baute oder/und Anlage?',
    type: 'select',
    required: true,
    config: {
      options: ['Baute(n)', 'Anlage(n)']
    }
  },
  'vorgesehene-nutzung': {
    label: 'Welchem Zweck dient das Vorhaben?',
    type: 'text',
    required: true,
    config: {
      options: [
        'Wohnen',
        'Gewerbe / Dienstleistung',
        'Industrie',
        'Landwirtschaft',
        'Öffentliche Nutzung',
        'Forstwirtschaft',
        'Tourismus'
      ]
    }
  }
}
