import { helper } from "@ember/component/helper";

const getFieldTree = (field, childFields = []) => {
  if (field.document.field) {
    return getFieldTree(field.document.field, [field, ...childFields]);
  }

  return [field, ...childFields];
};

export function getFieldPath([field]) {
  const tree = getFieldTree(field);
  const sections = tree.slice(0, -1);

  return {
    link: {
      section: sections[0] && sections[0].question.slug,
      subSection: sections[1] && sections[1].question.slug
    },
    label: tree.map(f => f.question.label).join(" > ")
  };
}

export default helper(getFieldPath);
