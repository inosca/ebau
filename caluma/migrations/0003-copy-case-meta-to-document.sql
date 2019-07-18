update form_document set meta=workflow_case.meta from workflow_case where workflow_case.document_id = form_document.id;
