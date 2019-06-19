import { warn } from "@ember/debug";

export function getCaseTypeSlug(doc) {
  const rootDocument = doc.rootDocument || doc;

  return rootDocument.raw.form.slug;
}

export function getCaseType(doc) {
  const rootDocument = doc.rootDocument || doc;

  return rootDocument.raw.form.name;
}

export function parseFields(doc) {
  return doc.fields
    .map(parseQuestion)
    .filter(question => question && !question.hidden);
}

/**
 * This is the wrapper function that invokes the right parser function
 * for the type of the given field.
 *
 * @param {Field} field
 */
function parseQuestion(field) {
  switch (field.question.__typename) {
    case "FormQuestion":
      return parseFormQuestion(field);

    case "TextQuestion":
    case "TextareaQuestion":
    case "IntegerQuestion":
    case "FloatQuestion":
    case "DateQuestion":
      return parseSimpleQuestion(field);

    case "ChoiceQuestion":
      return parseChoiceQuestion(field);

    case "DynamicChoiceQuestion":
      return parseChoiceQuestion(field, true);

    case "MultipleChoiceQuestion":
      return parseMultipleChoiceQuestion(field);

    case "DynamicMultipleChoiceQuestion":
      return parseMultipleChoiceQuestion(field, true);

    case "StaticQuestion":
      return parseStaticQuestion(field);

    case "TableQuestion":
      return parseTableQuestion(field);

    default:
      warn(field);
  }
}

function parseSimpleQuestion(field) {
  return {
    type: field.question.__typename,
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label,
    value: field.answer.value
  };
}

function parseStaticQuestion(field) {
  return {
    type: field.question.__typename,
    hidden: field.hidden,
    slug: field.question.slug,
    content: field.question.staticContent
  };
}

function parseTableQuestion(field) {
  return {
    type: field.question.__typename,
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label,
    columns: field.question.rowForm.questions.edges.map(edge => ({
      label: edge.node.label
    })),
    rows: (field.answer.value || []).map(doc =>
      doc.fields.map(field => parseQuestion(field))
    )
  };
}

function parseChoiceQuestion(field, flatten = false, limit = undefined) {
  const choices =
    field.question.__typename === "ChoiceQuestion"
      ? field.question.choiceOptions.edges
      : field.question.dynamicChoiceOptions.edges;

  const mapped = {
    type: flatten ? "TextQuestion" : "ChoiceQuestion",
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label
  };

  if (flatten) {
    mapped.value =
      choices
        .filter(edge => edge.node.slug === field.answer.value)
        .map(edge => edge.node.label)
        .join(", ") || null;
  } else {
    mapped.choices = choices
      .map(choice => ({
        label: choice.node.label,
        checked: choice.node.slug === field.answer.value
      }))
      .slice(0, limit);
  }

  return mapped;
}

function parseMultipleChoiceQuestion(field, flatten = false, limit) {
  const choices =
    field.question.__typename === "MultipleChoiceQuestion"
      ? field.question.multipleChoiceOptions.edges
      : field.question.dynamicMultipleChoiceOptions.edges;

  const mapped = {
    type: flatten ? "TextQuestion" : "MultipleChoiceQuestion",
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label
  };

  if (flatten) {
    mapped.value =
      choices
        .filter(edge => field.answer.value.includes(edge.node.slug))
        .map(edge => edge.node.label)
        .join(", ") || null;
  } else {
    mapped.choices = choices
      .map(choice => ({
        label: choice.node.label,
        checked:
          Array.isArray(field.answer.value) &&
          field.answer.value.includes(choice.node.slug)
      }))
      .slice(0, limit);
  }

  return mapped;
}

function parseFormQuestion(field) {
  return {
    type: field.question.__typename,
    hidden: field.hidden,
    slug: field.question.slug,
    label: field.question.label,
    children: parseFields(field.childDocument)
  };
}
