export default {
  name: "gr",
  languages: ["de", "it", "rm"],
  fallbackLanguage: "de",
  prodUrl: "ebau.admin.gr.ch",
  allowApplicantManualWorkItem: false,
  serviceGroups: {
    authorityBaB: 3,
  },
  answerSlugs: {
    objectStreet: "strasse-flurname",
    objectNumber: "nr",
    objectZIP: "plz-grundstueck-v3",
    objectLocation: "ort-grundstueck",
    description: "beschreibung-bauvorhaben",
    municipality: "gemeinde",
    specialId: "ebau-number",
    parcelNumber: "parzellennummer",
    firstNameApplicant: "vorname-gesuchstellerin",
    lastNameApplicant: "name-gesuchstellerin",
    juristicNameApplicant: "name-juristische-person-gesuchstellerin",
    isJuristicApplicant: "juristische-person-gesuchstellerin",
    isJuristicApplicantYes: "juristische-person-gesuchstellerin-ja",
    personalDataApplicant: "personalien-gesuchstellerin",
  },
  intentSlugs: ["beschreibung-bauvorhaben"],
};