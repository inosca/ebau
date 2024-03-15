from caluma.caluma_workflow import models as workflow_models
from django.conf import settings

from camac.core.utils import canton_aware, generate_sort_key
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Instance
from camac.instance.utils import (
    copy_instance,
    fill_ebau_number,
    get_lead_authority,
    set_construction_control,
)
from camac.user.models import Group, Service


class DecisionLogic:
    @classmethod
    def post_complete_decision_building_permit(
        cls, instance, work_item, user, camac_user
    ):
        if cls.should_continue_after_decision(instance, work_item):
            if settings.APPLICATION_NAME == "kt_bern":
                construction_control = set_construction_control(instance)
                instance.set_instance_state("sb1", camac_user)

                # copy municipality tags for sb1
                cls.copy_municipality_tags(instance, construction_control)
                cls.copy_responsible_person_lead_authority(
                    instance, construction_control
                )
            else:
                instance.set_instance_state(
                    settings.DECISION["INSTANCE_STATE_AFTER_DECISION"],
                    camac_user,
                )
        elif (
            settings.WITHDRAWAL
            and instance.instance_state.name == settings.WITHDRAWAL["INSTANCE_STATE"]
        ):
            instance.set_instance_state(
                settings.WITHDRAWAL["INSTANCE_STATE_CONFIRMED"], camac_user
            )
        else:
            instance.set_instance_state("finished", camac_user)

        cls.handle_appeal_decision(instance, work_item, user, camac_user)

    @classmethod
    @canton_aware
    def should_continue_after_decision(
        cls, instance: Instance, work_item: workflow_models.WorkItem
    ) -> bool:
        decision = (
            work_item.document.answers.filter(
                question_id=settings.DECISION["QUESTIONS"]["DECISION"]
            )
            .values_list("value", flat=True)
            .first()
        )

        if not decision:  # pragma: no cover
            return False

        return decision == settings.DECISION["ANSWERS"]["DECISION"]["APPROVED"]

    @classmethod
    def should_continue_after_decision_so(
        cls, instance: Instance, work_item: workflow_models.WorkItem
    ) -> bool:
        if instance.instance_state.name == settings.WITHDRAWAL["INSTANCE_STATE"]:
            return False

        decision = (
            work_item.document.answers.filter(
                question_id=settings.DECISION["QUESTIONS"]["DECISION"]
            )
            .values_list("value", flat=True)
            .first()
        )

        if not decision:  # pragma: no cover
            return False

        if settings.APPEAL and work_item.case.meta.get("is-appeal"):
            previous_instance = work_item.case.document.source.case.instance
            previous_state = previous_instance.previous_instance_state.name

            return (
                decision == settings.APPEAL["ANSWERS"]["DECISION"]["CONFIRMED"]
                and previous_state == "construction-monitoring"
            ) or decision == settings.APPEAL["ANSWERS"]["DECISION"]["CHANGED"]

        construction_tee = (
            work_item.document.answers.filter(
                question_id=settings.DECISION["QUESTIONS"]["BAUABSCHLAG"]
            )
            .values_list("value", flat=True)
            .first()
        )

        return (
            decision
            in [
                settings.DECISION["ANSWERS"]["DECISION"]["APPROVED"],
                settings.DECISION["ANSWERS"]["DECISION"]["PARTIALLY_APPROVED"],
            ]
        ) or (
            decision == settings.DECISION["ANSWERS"]["DECISION"]["REJECTED"]
            and construction_tee
            == settings.DECISION["ANSWERS"]["BAUABSCHLAG"]["MIT_WIEDERHERSTELLUNG"]
        )

    @classmethod
    def should_continue_after_decision_be(
        cls, instance: Instance, work_item: workflow_models.WorkItem
    ) -> bool:
        decision = (
            work_item.document.answers.filter(
                question_id=settings.DECISION["QUESTIONS"]["DECISION"]
            )
            .values_list("value", flat=True)
            .first()
        )

        if not decision:  # pragma: no cover
            return False

        if settings.APPEAL and work_item.case.meta.get("is-appeal"):
            previous_instance = work_item.case.document.source.case.instance
            previous_state = previous_instance.previous_instance_state.name

            if decision == settings.APPEAL["ANSWERS"]["DECISION"]["CONFIRMED"]:
                return previous_state == "sb1"
            elif decision == settings.APPEAL["ANSWERS"]["DECISION"]["CHANGED"]:
                return previous_state != "sb1"
            elif decision == settings.APPEAL["ANSWERS"]["DECISION"]["REJECTED"]:
                return False

        approval_type = (
            work_item.document.answers.filter(
                question_id=settings.DECISION["QUESTIONS"]["APPROVAL_TYPE"]
            )
            .values_list("value", flat=True)
            .first()
        )

        return (
            decision == settings.DECISION["ANSWERS"]["DECISION"]["APPROVED"]
            and approval_type
            != settings.DECISION["ANSWERS"]["APPROVAL_TYPE"]["BUILDING_PERMIT_FREE"]
        ) or approval_type in [
            settings.DECISION["ANSWERS"]["APPROVAL_TYPE"][
                "CONSTRUCTION_TEE_WITH_RESTORATION"
            ],
            settings.DECISION["ANSWERS"]["APPROVAL_TYPE"][
                "PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION"
            ],
        ]

    @classmethod
    def copy_municipality_tags(cls, instance, construction_control):
        municipality_tags = instance.tags.filter(
            service=Service.objects.filter(
                service_group__name="municipality",
                trans__language="de",
                trans__name=construction_control.trans.get(language="de").name.replace(
                    "Baukontrolle", "Leitbehörde"
                ),
            ).first()
        )

        for tag in municipality_tags:
            instance.tags.create(service=construction_control, name=tag.name)

    @classmethod
    def copy_responsible_person_lead_authority(cls, instance, construction_control):
        lead_authority = get_lead_authority(construction_control)

        responsible_service = instance.responsible_services.filter(
            service=lead_authority
        ).first()

        if lead_authority.responsibility_construction_control and responsible_service:
            instance.responsible_services.create(
                service=construction_control,
                responsible_user=responsible_service.responsible_user,
            )

    @classmethod
    def handle_appeal_decision(cls, instance, work_item, user, camac_user):
        if not settings.APPEAL or not instance.case.meta.get("is-appeal"):
            return

        if work_item.document.answers.filter(
            question_id=settings.APPEAL["QUESTIONS"]["DECISION"],
            value=settings.APPEAL["ANSWERS"]["DECISION"]["REJECTED"],
        ).exists():
            new_instance = copy_instance(
                instance=instance,
                group=Group.objects.get(pk=user.camac_group),
                user=camac_user,
                caluma_user=user,
                skip_submit=True,
                # Mark the new instance as result of a rejected appeal so the
                # frontend can find it in the copies of the previous instance to
                # redirect after the decision was submitted.
                new_meta={"is-rejected-appeal": True},
            )

            if settings.APPLICATION_NAME == "kt_bern":
                fill_ebau_number(
                    instance=new_instance,
                    ebau_number=instance.case.meta.get("ebau-number"),
                    caluma_user=user,
                )
            else:
                identifier = CreateInstanceLogic.generate_identifier(new_instance)
                new_instance.case.meta["dossier-number"] = identifier
                new_instance.case.meta["dossier-number-sort"] = generate_sort_key(
                    identifier
                )
                new_instance.case.save()
