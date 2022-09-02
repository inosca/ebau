import { getAnswerDisplayValue } from "ember-ebau-core/utils/get-answer";

export default function getFormTitle(document, answerSlugs) {
  const oerebProcedure = getAnswerDisplayValue(
    document,
    answerSlugs.oerebProcedure
  );
  const oerebTopics = getAnswerDisplayValue(document, answerSlugs.oerebTopics);
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
    const base = `${oerebTopics?.join(", ")} - ${oerebProcedure}`;
    return oerebPartialState ? `${base} (${oerebPartialState})` : base;
  } else if (procedureCanton) {
    return procedureCanton;
  } else if (procedureConfederation) {
    return procedureConfederation;
  }
}
