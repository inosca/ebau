import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import getPersonals from "caluma-portal/gql/queries/get-personals.graphql";

function findAnswerByRegex(answers, regexp) {
  const re = new RegExp(regexp);

  return answers.find((answer) => re.test(answer.question.slug))?.value;
}

function preparePerson(document) {
  const answers = document.answers.edges.map(({ node }) => node);

  return {
    firstName: findAnswerByRegex(
      answers,
      mainConfig.personalSuggestions.firstNameRegexp
    ),
    lastName: findAnswerByRegex(
      answers,
      mainConfig.personalSuggestions.lastNameRegexp
    ),
    juristicName: findAnswerByRegex(
      answers,
      mainConfig.personalSuggestions.juristicNameRegexp
    ),
    email: findAnswerByRegex(
      answers,
      mainConfig.personalSuggestions.emailRegexp
    ),
  };
}

export default class PersonalSuggestionsComponent extends Component {
  @queryManager apollo;

  suggestions = trackedTask(this, this.fetchSuggestions, () => [
    this.args.instanceId,
  ]);

  @dropTask
  *fetchSuggestions() {
    const response = yield this.apollo.query(
      {
        query: getPersonals,
        fetchPolicy: "network-only",
        variables: {
          instanceId: this.args.instanceId,
          tableQuestions: mainConfig.personalSuggestions.tableQuestions,
        },
      },
      "allCases.edges"
    );

    return (response[0]?.node.document.answers.edges ?? []).map(
      ({ node: table }) => {
        return {
          label: table.question.label,
          suggestions: table.value.map(preparePerson),
        };
      }
    );
  }
}
