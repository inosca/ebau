from django.conf import settings

from camac.caluma.extensions.permissions import CustomPermission
from camac.caluma.form_import_utils import FormImportLabeler, FormImportWriter
from camac.instance.master_data import MasterData
from camac.settings.utils import is_module_enabled


def _rpg2_work_item(instance):
    """Return the rpg2 work item for the given instance."""
    return instance.case.work_items.filter(task_id=settings.RPG2.task).first()


def has_rpg2_edit_permission(request, instance):
    if not is_module_enabled("RPG2") or not settings.RPG2.import_mapping:
        return False

    work_item = _rpg2_work_item(instance)
    if work_item is None:
        return False

    return CustomPermission(request).has_camac_edit_permission(
        work_item.document, request.caluma_info
    )


class RPG2ImportReader:
    """
    Read rpg2 related answers from the main form document or another work item document.

    Relies on MasterData answer_resolver and table_resolver methods but keeps the mapping in the rpg2 module config
    to avoid further loading the master data config, maintain separate transforms and strip option slugs for
    passing to labeler in the same way as for GIS.
    """

    def __init__(self, instance):
        self.md = MasterData.from_case_id(instance.case)

    def resolve_all(self):
        """Return {target_slug: labeled_value} for every import_mapping entry."""
        unlabeled_data = {}
        for target_slug, source_config in settings.RPG2.import_mapping.items():
            value = self._resolve_source(source_config)
            if value is not None:
                unlabeled_data[target_slug] = value
        return RPG2Labeler().label(unlabeled_data)

    def _resolve_source(self, source_config):
        """Resolve source value(s) for one import_mapping entry."""
        if source_config.row_mapping:
            return self._resolve_table(source_config)

        value = self.md.answer_resolver(
            lookup=source_config.source_slugs,
            document_from_work_item=source_config.from_work_item,
        )
        return self._apply_transform_and_strip(value=value, config=source_config)

    def _resolve_table(self, source_config):
        """Resolve a table entry into a list[dict] of resolved rows or None."""
        column_mapping = {
            target_column: column_config.source_slugs
            for target_column, column_config in source_config.row_mapping.items()
        }
        source_rows = self.md.table_resolver(
            lookup=source_config.source_slugs,
            column_mapping=column_mapping,
            document_from_work_item=source_config.from_work_item,
        )
        resolved_rows = []
        for source_row in source_rows:
            row = self._parse_row(
                source_row=source_row, row_mapping=source_config.row_mapping
            )
            if row:
                resolved_rows.append(row)
        return resolved_rows or None

    def _parse_row(self, source_row, row_mapping):
        """Apply transform & strip each cell."""
        resolved_row = {}
        for target_column, column_config in row_mapping.items():
            cell = self._apply_transform_and_strip(
                value=source_row.get(target_column), config=column_config
            )
            if cell is not None:
                resolved_row[target_column] = cell
        return resolved_row

    def _apply_transform_and_strip(self, value, config):
        if value is None:
            return None
        if config.transform:
            value = RPG2Transform.apply(transform_name=config.transform, value=value)

        # check value again after applying transform
        if config.is_option_target and value is not None:
            value = (
                [
                    self._strip_source_root(
                        option_slug=v, source_slugs=config.source_slugs
                    )
                    for v in value
                ]
                if isinstance(value, list)
                else self._strip_source_root(
                    option_slug=value, source_slugs=config.source_slugs
                )
            )
        return value

    @staticmethod
    def _strip_source_root(option_slug, source_slugs):
        """
        Strip the source's option slug root so the labeler can rebuild it on the target via {question.slug}-{value}.

        The import does not map option values so every source option (-{value}) must exist as a target option. "
        (e.g. source: 'kantonale-pruefung-gesuchscodes-a01' => target: 'rpg2-bewilligungsgrund-a01')
        """
        for source_question in source_slugs:
            prefix = f"{source_question}-"
            if option_slug.startswith(prefix):
                return option_slug.removeprefix(prefix)
        return option_slug


class RPG2Labeler(FormImportLabeler):
    def lookup_dynamic_choice(self, question, value):
        raise NotImplementedError(
            "rpg2 does not support Question.TYPE_DYNAMIC_CHOICE questions"
        )


class RPG2Transform:
    """
    Transform functions for the rpg2 import.

    Can be extended with further transforms if needed.
    """

    @staticmethod
    def first_choice_from_multiple(value):
        """Multiple-choice answer (list of option slugs) to single-choice (first option)."""
        if value and isinstance(value, list):
            return value[0]
        return None

    @classmethod
    def apply(cls, transform_name, value):
        """Lookup a transform by name and apply it."""
        fn = getattr(cls, transform_name, None)
        if not callable(fn):
            raise ValueError(
                f"Unknown rpg2 transform: {transform_name}. "
                f"Please define {transform_name} as a @staticmethod in RPG2Transform"
            )
        return fn(value)


def get_rpg2_import_data(instance):
    """Read from main form document/other work item document and build preview data."""
    return {"data": RPG2ImportReader(instance).resolve_all()}


def apply_rpg2_import(instance, request):
    """Read again from main form document/other work item document and write the rpg2 document answers."""
    work_item = _rpg2_work_item(instance)
    # GIS pases convert_answer_value to match type of question and convert the value accordingly, for integer and float.
    # Since question types match in the rpg2 config currently, this convert is left out but can be
    # passed if target and source question types diverge.
    writer = FormImportWriter(
        user=request.caluma_info.context.user,
        instance_pk=instance.pk,
        meta_key="rpg2-import",
    )
    written = set()
    for question_slug, labeled in RPG2ImportReader(instance).resolve_all().items():
        if writer.write_answer(work_item.document, question_slug, labeled):
            written.add(question_slug)
    return {"questions": list(written)}
