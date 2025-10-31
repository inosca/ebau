# Fristenmanagement module

Initial MR version: https://git.adfinis.com/camac-ng/camac-ng/-/merge_requests/10438

## Commands

### migrate_deadlines

Migration command to initialize deadlines for old dossiers.

`dc exec django python manage.py migrate_deadlines --verbosity 2 --commit`

### update_deadline_progression

Command to recalculate deadlines in case something needs to be corrected.

- Optionally add flag `--all` to not only process open deadlines.

`dc exec django python manage.py update_deadline_progression --verbosity 2 --commit`

## Feature overview

### Events

| Event                        | Default                                                                                                                                                               | AG                                                                                                                                                                      | GR                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Applicant request withdrawal | Close all open suspensions                                                                                                                                            | Default                                                                                                                                                                 | Default                                                          |
| Create additional demand     | Open suspension                                                                                                                                                       | Default                                                                                                                                                                 | Default                                                          |
| Cancel additional demand     | Close open suspension                                                                                                                                                 | Default                                                                                                                                                                 | Default                                                          |
| Fill additional demand       | Close open suspension                                                                                                                                                 | Default                                                                                                                                                                 | Default                                                          |
| Create publication           | None                                                                                                                                                                  | Default                                                                                                                                                                 | Reset start-date for responsible service + Recalculate deadlines |
| Fill publication             | Reset start-date for responsible service + Recalculate deadlines                                                                                                      | Default                                                                                                                                                                 | Default                                                          |
| Fill formal exam             | Reset start-date for responsible service + Recalculate deadlines                                                                                                      | Default                                                                                                                                                                 | Default                                                          |
| Fill decision date           | Recalculate deadlines                                                                                                                                                 | Default                                                                                                                                                                 | Default                                                          |
| Create inquiry               | Create deadline for AfB/ARE                                                                                                                                           | Default                                                                                                                                                                 | Default                                                          |
| Inquiry re-do                | None                                                                                                                                                                  | If the inquiry decision is not "Unterlagenergänzung",<br> Create a claim suspension between<br>original inquiry close till redo inquiry.<br>Close all claim suspensions | Default                                                          |
| Inquiry re-invite            | If the inquiry decision is not "Unterlagenergänzung",<br>Create a claim suspension between<br>previous inquiry close till new inquiry.<br>Close all claim suspensions | Default                                                                                                                                                                 | Default                                                          |
| Inquiry answered             | None                                                                                                                                                                  | If decision answer is "Unterlagenergänzung",<br>immediately create a claim suspension with<br>start-date now, and end-date open                                         | Default                                                          |

### Logic

| Feature                        | Default                                                                           | AG                                                                                                     | GR                                                                                                                                                                        |
| ------------------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| End date inquired service      | Inquiry close date                                                                | If an open claim suspension exists (Unterlagenergänzung), no end-date.<br>Otherwise Inquiry close date | Default                                                                                                                                                                   |
| Start date responsible service | Submit date                                                                       | Default                                                                                                | Publication end-date for simplified dossier or no publication applicable,<br>submit date for other dossiers.<br>If the formal exam is not completed don't set a startdate |
| Deadline visibility            | Own service for responsible service deadline or inquired service AFB_ARE deadline | Service and parent service for<br>responsible service deadline.<br>Cantonal service for AFB deadline   | Default                                                                                                                                                                   |
| Has write access               | Permission<br> `suspensions-write`+`deadlines-write`                              | Municipality/municipality/lead + AfB roles                                                             | Municipality/ARE service group & municipality-lead/service-lead role                                                                                                      |
| Has read access                | Permission<br> `suspensions-read`+`deadlines-read`                                | service-cantonal \| subservice role                                                                    | municipality/ARE service group & municipality-lead/service-lead role                                                                                                      |
| Can override deadline end-date | No, permission:<br> `deadlines-write-custom-enddate`                              | write access + form in [`plangenehmigungsverfahren-gas`,`plangenehmigungsverfahren-bund`]              | Default                                                                                                                                                                   |
| Use end-date in case header    | False                                                                             | Default                                                                                                | True                                                                                                                                                                      |
| Public holidays                | Python `holidays` package                                                         | A `AargauAdministrationHolidays` <br>which alters the `holidays` package result                        | Default                                                                                                                                                                   |

## Documentation

### Working days:

On the deadline type you can configure `exclude_weekends` and `exclude_public_holidays` which will be used in all calculations for that deadline type. These values are set when creating a new deadline in the django admin.

When set to True all calculations will not take weekends and(or) public holidays into account.

### Deadline types:

You can configure these in the Django admin. Can be limited to either a service group or specific service.

The first standard deadline type for a service will be automatically set when a new deadline is created.

The deadline type `lead_time` defines the total number of (working) days are expected.

**Config dump:**

Originally there was a dump config to dump deadline types. Has been removed, just create manually through Django admin

### Sistiert flag on the case

In the topleft a mark `Sistiert` will show when an instance has an open suspension. This is saved on the case meta per service. So this flag can be different for the responsible service or for ARE/AfB.

### Workitem list

Workitems belonging to a case that is currently suspended will be greyed out in the workitem list.

### Recalculation

Will update:

- Start date
- Target deadline date
- Progression values (total days of suspension, process deadline date, process deadline days)
- Case meta (list of service ID's for who the case is suspended, a.k.a. has an open suspension)

Automatically triggered by:

- manually changing a suspension/deadline
- through any of the event side effects
- at midnight through celery-beat periodic task (for running deadlines)

### Celery / celery beat

Periodic task will run at midnight to recalculate deadlines with open suspensions.

Local or for GR a separate docker container `celery-beat` will run, using the new entrypoint `celery-beat-dev` (or `celery-beat` in prod).

### Progression calculation

**Sistierte Tage seit Start**: sum of suspended non-overlapping (working) days
**Durchlaufzeit**: number of (working) days since the start date
**Fristende**: start date + lead time (working) days + suspended (working) days ignoring holidays/weekends
**Verfahrensende**: set during events based on decision_date for responsible service, inquiry_close_date for AfB/ARE (In AG False when an open claim suspension exists for AfB)

### Frontend

- Config setting: `enabled` enables the case header visibility
- Config setting: `useEndDate`. Controls the case header display format like:
  - Eingereicht am / Fristende: 23.09.2024 / 14.08.2025
  - Eingereicht am / Durchlaufzeit: 23.09.2024 / 5 Tage
- Config setting: `showTargetDeadlineDate`: show/hide the Fristende on the detail page
- Config setting: `showProcessDeadlineDate`: show/hide the Verfahrensfrist on the detail page
- Config setting: `allowFutureStartDate`: allows to set the deadline start date in the future (default: false)
