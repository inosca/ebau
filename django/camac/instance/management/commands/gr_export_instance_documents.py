from caluma.caluma_form.models import Answer
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from camac.instance.master_data import MasterData
from camac.instance.models import Instance, InstanceAlexandriaDocument as Doc


class Command(BaseCommand):
    """Management command to generate a statistic for the Kt. GR.

    This management command checks how many instances have a positive decision but:
    - have no documents in 'Alle Beteiligten'
    - have documents in 'Alle Beteiligten' but NOT in 'Beteiligte Behörden'

    This statistics was needed in GR to check if municipalities are following the correct workflows of moving documents around in the dossier after the decision in a dossier was made.
    """

    def handle(self, *args, **options):
        def print_instances_info(title, q):
            print(f"\n# {title} - {q.count()} dossier(s)")
            for instance in q.iterator(chunk_size=50):
                # format instance name
                instance_name = (
                    instance.case.meta.get("dossier-number")
                    if instance.case and instance.case.meta.get("dossier-number")
                    else f"instance-{str(instance.pk)}"
                )
                master_data = MasterData(instance.case)
                municipality_name = master_data.municipality_name
                responsible_service = instance.responsible_service().get_name()

                # collect instance documents
                docs_q = instance.alexandria_instance_documents.all().order_by(
                    "document__category__slug", "document__title"
                )
                instance_docs = [doc.document for doc in docs_q if doc.document]

                # print instance output
                print(f"\n - {instance_name}: {len(instance_docs)} document(s)")
                print(f" - Municipality: {municipality_name}")
                print(f" - Responsible service: {responsible_service}")
                if len(instance_docs) > 0:
                    for doc in instance_docs:
                        category_slug = (
                            doc.category.slug if doc.category else "no-category"
                        )
                        print(f"   > {category_slug} - {doc.title}")
                    print("\n")

        # filter only positive decision instances.
        base_qs = Instance.objects.annotate(
            has_positive_decision=Exists(
                Answer.objects.filter(
                    document__work_item__case__instance=OuterRef("pk"),
                    question_id="decision-decision",
                    value__in=[
                        "decision-decision-approved",
                        "decision-decision-approved-with-reservation",
                        "decision-decision-positive",
                        "decision-decision-positive-with-reservation",
                    ],
                )
            )
        ).filter(has_positive_decision=True)

        # Dossiers with no documents in 'Alle Beteiligten'
        print_instances_info(
            title="Dossiers with no documents in 'Alle Beteiligten'",
            q=(
                base_qs.annotate(
                    has_doc_in_alle_beteiligten=Exists(
                        Doc.objects.filter(
                            instance_id=OuterRef("pk"),
                            document__category__slug__in=["alle-beteiligten"],
                        )
                    ),
                )
                .filter(has_doc_in_alle_beteiligten=False)
                .prefetch_related("alexandria_instance_documents")
            ),
        )

        # Dossiers with documents in 'Alle Beteiligten' but not in 'Beteiligte Behörden'
        print_instances_info(
            title="Dossiers with documents in 'Alle Beteiligten' but not in 'Beteiligte Behörden'",
            q=(
                base_qs.annotate(
                    has_doc_in_alle_beteiligten=Exists(
                        Doc.objects.filter(
                            instance_id=OuterRef("pk"),
                            document__category__slug__in=["alle-beteiligten"],
                        )
                    ),
                    has_doc_in_beteiligte_behorden=Exists(
                        Doc.objects.filter(
                            instance_id=OuterRef("pk"),
                            document__category__slug__in=["beteiligte-behörden"],
                        )
                    ),
                )
                .filter(
                    has_doc_in_alle_beteiligten=True,
                    has_doc_in_beteiligte_behorden=False,
                )
                .prefetch_related("alexandria_instance_documents")
            ),
        )

        self.stdout.write("\n")
        self.stdout.write(self.style.SUCCESS("Export complete"))
