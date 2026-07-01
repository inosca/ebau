from camac.agsmartservice import tasks
from camac.caluma.api import CalumaApi
from camac.instance.master_data import MasterData
from camac.settings.utils import is_module_enabled


def build_procedure_title(instance):
    master_data = MasterData(instance.case)
    application_type = master_data.application_type
    dossier_number = master_data.dossier_number
    municipality_name = master_data.municipality_name
    proposal = master_data.proposal

    return f"{application_type} {dossier_number} ({municipality_name}): {proposal}"


def _schedule(task, instance, *args):
    if not is_module_enabled("AGSMARTSERVICE") or CalumaApi().is_paper(instance):
        return None

    return task.delay_on_commit(instance.pk, build_procedure_title(instance), *args)


def submit(instance, assignee_id):
    return _schedule(tasks.submit_procedure_task, instance, assignee_id)


def complete_preliminary_check(instance):
    return _schedule(tasks.complete_preliminary_check_task, instance)


def start_construction_monitoring(instance):
    return _schedule(tasks.start_construction_monitoring_task, instance)


def complete(instance):
    return _schedule(tasks.complete_procedure_task, instance)


def delete_procedure(instance):
    if not is_module_enabled("AGSMARTSERVICE") or CalumaApi().is_paper(instance):
        return None

    return tasks.delete_procedure_task.delay_on_commit(instance.pk)
