// copied from ember-camac-ng
//TODO move to core
export default function getAnswer(document, slugOrSlugs) {
  const slugs = Array.isArray(slugOrSlugs) ? slugOrSlugs : [slugOrSlugs];
  return document.answers.edges.find((edge) =>
    slugs.includes(edge.node.question.slug),
  );
}
