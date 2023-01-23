export function getAnswer(document, slugOrSlugs) {
  const slugs = Array.isArray(slugOrSlugs) ? slugOrSlugs : [slugOrSlugs];
  return document.answers.edges.find((edge) =>
    slugs.includes(edge.node.question.slug)
  );
}

export function getAnswerDisplayValue(document, slug, useLabel = true) {
  const answer = document.answers?.edges
    .map(({ node }) => node)
    .find((answer) => answer.question.slug === slug);

  if (!answer) {
    return null;
  }

  if (useLabel && answer.selectedOption) {
    return answer.selectedOption.label;
  }
  if (useLabel && answer.selectedOptions) {
    return answer.selectedOptions.edges.map((item) => item.node.label);
  }
  if (answer.tableValue) {
    return answer.tableValue.map((item) =>
      item.answers.edges.map((edge) => edge.node.stringValue)
    );
  }

  const valueKey = Object.keys(answer).find((key) => /^\w+Value$/.test(key));

  return answer[valueKey];
}
