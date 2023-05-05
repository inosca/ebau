import { getAnswerDisplayValue } from "ember-ebau-core/utils/get-answer";

export default function getFormTitle(document, answerSlugs) {
  const oerebProcedure = getAnswerDisplayValue(
    document,
    answerSlugs.oerebProcedure
  );
  const staticForestBoundaryMunicipality =
    getAnswerDisplayValue(
      document,
      "waldfeststellung-mit-statischen-waldgrenzen-gemeinde"
    ) === "Ja";
  const staticForestBoundaryCanton =
    getAnswerDisplayValue(
      document,
      "waldfeststellung-mit-statischen-waldgrenzen-kanton"
    ) === "Ja";
  const oerebTopics =
    staticForestBoundaryCanton || staticForestBoundaryMunicipality
      ? "Statische Waldgrenze"
      : getAnswerDisplayValue(document, answerSlugs.oerebTopicsCanton) ||
        getAnswerDisplayValue(document, answerSlugs.oerebTopicsMunicipality);

  const oerebPartialState = getAnswerDisplayValue(
    document,
    answerSlugs.oerebPartialState
  );
  const procedureCanton = getAnswerDisplayValue(
    document,
    answerSlugs.procedureCanton
  );
  const procedureConfederation = getAnswerDisplayValue(
    document,
    answerSlugs.procedureConfederation
  );

  if (oerebProcedure && oerebTopics) {
    const base = `${oerebTopics} - ${oerebProcedure}`;
    return oerebPartialState ? `${base} (${oerebPartialState})` : base;
  } else if (procedureCanton) {
    return procedureCanton;
  } else if (procedureConfederation) {
    return procedureConfederation;
  }
}
