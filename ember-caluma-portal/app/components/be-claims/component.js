import Component from "@ember/component";
import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";

export default class BeClaimsComponent extends Component {
  @reads("field.question.meta.columnsToDisplay") displayedColumns;
  @reads("field.question.rowForm.questions.edges") questions;

  @computed("questions.[]", "displayedColumns.[]")
  get columns() {
    return this.questions
      .map(({ node }) => node)
      .filter(({ slug }) => this.displayedColumns.includes(slug));
  }
}
