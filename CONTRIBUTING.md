# Contributing

Contributions to this project are very welcome! For minor changes like bugfixes, typos, etc. feel free to open a Pull Reqeuest directly. If you'd like to change the behaviour of an existing module or add an entirely new feature, please open an issue with a summary of the proposed changes first - that way, the proposal can be discussed with the various cantons using this project before implementation starts.

This repository is currently created from a separate, private repo using `git filter-repo`. Once all legacy components have been replaced, this repository can become the single source of truth - until then, the contribution process won't be as smooth as it should be, so we kindly ask you for a little extra patience.

Another important thing that is currently not part of the Open Source repository is a continuous integration (CI) setup. Until CI has been implemented, we ask you to run the needed tests locally. If you'd like to contribute CI support using GitHub actions, you have our full support!

## What to consider when testing
The word "change" is used for any feature, fix or update that can impact the behavior or visuals of an application, package, etc. Any code change, template or configuration falls into this category.

Testing should happen continuously during implementation and also after the last code change before merging! During implementation, testing and reviewing the same or similar points are of importance. This list isn't complete and doesn't go into detail on code quality.

- **What are the risks associated with the change?**

    <details><summary><i>Further explanation</i></summary>

    The higher the risk associated with the change, the more in-depth it should be looked at. If you are unsure, try to involve more experienced developers in the review.
    - **Low risk**:
       * Visual changes, reading data, data processing with no lasting effect on data, etc.
       * Can be fixed easily, no lasting effects (bugs still can be annoying for users though!)
    - **Medium risk**: Data handling / logic changes with small effect on newly generated data, changes that might affect how existing data is read (e.g. form changes), etc.
       * Can usually be fixed with migrations and fix scripts
    - **High risk**: Changes to visibility & permission layer, migrations with large data changes, etc.
       * Opens up application to vulnerabilities and affects large parts of application
       * Can cause damage to existing data at a larger scale, which is harder or maybe impossible to fix

    </details>

- **Does the change work as expected?**

    - **Frontend & Backend:**
        - **Visuals** *(frontend only)*
        - **Behavior**
        - **Role/service etc. specific differences**
        - **Application area specific differences**
        - **Data validation, handling & formatting**
        - **Error handling**
        - **Translations**
        - **Performance**
        - **Database migrations** *(backend only)*

        <details><summary><i>Further explanation</i></summary>

        - **Visuals:** Does it look as expected? *(frontend only)*
        - **Behavior:** Does it behave as expected? Do actions or state changes trigger the expected behavioral or visual changes? Is the correct data fetched, filtered, and displayed as expected? Does the implemented change do what it is supposed to (filtering, data manipulation, state changes etc.)?
        - **Role/service etc. specific differences:** Are differences between users, roles, groups, services and service groups reflected correctly in their abilities, visible elements, permissions and visibilities?
        - **Application area specific differences:** Are differences between application areas reflected correctly (internal vs. portal, global vs. instance, reusable components/code logic)?
        - **Data validation, handling & formatting:** Are inputs validated as expected and are unexpected inputs either rejected or handled appropriately? Is data validated and formatted correctly on read and write?
        - **Error handling:** Are errors triggered and handled as expected?
        - **Translations:** Are new texts added or changed, that require a translation? Are the translations included in all necessary languages? Have the translations been delivered by a translation service (e.g. by the canton)?
        - **Performance:** Does the change affect the performance of the application negatively? Examples of common performance issues:
            - Query explosions which can be prevented by testing with production-like data and using `django-silk`
            - Unnecessary frontend requests or too many frontend requests (error loops or similar situations) which can be prevented by keeping an eye on the network tab during implementation
        - **Database migrations:** Does the MR include migrations? Were they tested against existing data? Can they be rolled back safely? *(backend only)*

        </details>

    - **Workflow / form configuration:**
        - **Visuals**
        - **Behavior**
        - **Translations**
        - **Handling of differences in pre-existing data**
        - **Migrations**

        <details><summary><i>Further explanation</i></summary>

        - **Visuals:** Is the document and its questions rendered as expected?
        - **Behavior:** Are the work-items generated as expected with the expected configuration (addressed & controlling groups, deadline etc.)? Does the document apply the expected configuration (JEXL logic etc.)?
        - **Translations:** Are new texts added or changed, that require a translation? Are the translations included in all necessary languages? Have the translations been delivered by a translation service (e.g. by the canton)?
        - **Handling of differences in pre-existing data:** Do the changes affect how pre-existing data is handled? Are differences in pre-existing data accounted for and handled appropriately?
        - **Migrations:** Are migrations necessary to prevent breaking existing data?

        </details>

- **Does the change affect other cantons or other parts of the application (and work as expected)?**
    - **Effects on other parts of code base**
    - **Effects on other cantons**

    <details><summary><i>Further explanation</i></summary>

    - **Effects on other parts of code base:** Does the change affect other parts of the code base (changes to shared code, configuration or settings)? Which application areas are affected (caluma portal, ember internal area, camac internal area, eCH-0211, etc.)? Should the change be visible / noticeable, **and does it work as expected in all affected areas**?
    - **Effects on other cantons:** Does the change affect other cantons (changes to shared code, configuration or settings)? Which cantons are affected? Are new and old cantons affected? Should the change be visible / noticeable, **and does it work as expected in all affected cantons**?

    </details>

- **Code quality**: Reusability, separation of concerns / encapsulation, readability / simplicity, test coverage, etc.
