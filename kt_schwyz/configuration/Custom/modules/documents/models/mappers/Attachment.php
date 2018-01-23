<?php


class Documents_Model_Mapper_Attachment extends Custom_CamacMapper {

	const TYPE_APPLICANT = 1;
	const TYPE_DEPARTMENT = 2;
	const TYPE_COMMUNITY = 3;
	const TYPE_PARCEL_PICTURE = 4;
	const TYPE_LISAG = 5;

	protected $dbTable = "Documents_Model_DbTable_Attachment";
	protected $pk_prop = "attachmentID";
	protected $pk_col  = "ATTACHMENT_ID";

	public function rowToModel($row) {
		$name = $row['NAME'];
		if (class_exists('Normalizer')) {
			$name = \Normalizer::normalize($name);
		}
		return new Documents_Model_Data_Attachment(
			$row['ATTACHMENT_ID'],
			$name,
			$row['INSTANCE_ID'],
			$row['PATH'],
			$row['SIZE'],
			Camac_Date::getDateTimeFromDbString($row['DATE']),
			$row['USER_ID'],
			$row['IDENTIFIER'],
			$row['MIME_TYPE'],
			$row['ATTACHMENT_SECTION_ID'],
			$row['SERVICE_ID'],
			$row['IS_PARCEL_PICTURE'],
			$row['DIGITAL_SIGNATURE'],
			$row['IS_CONFIDENTIAL']
		);
	}

	public function modelToRow($attachment) {
		$name = $attachment->name;
		if (class_exists('Normalizer')) {
			$name = \Normalizer::normalize($name);
		}
		return array(
			'NAME'                  => $name,
			'INSTANCE_ID'           => $attachment->instanceID,
			'PATH'                  => $attachment->path,
			'SIZE'                  => intval($attachment->size),
			'DATE'                  => Camac_Date::getDbStringFromDateTime($attachment->date),
			'USER_ID'               => $attachment->userID,
			'IDENTIFIER'            => $attachment->identifier,
			'MIME_TYPE'             => $attachment->mimeType,
			'ATTACHMENT_SECTION_ID' => $attachment->attachmentSectionID,
			'SERVICE_ID'            => $attachment->serviceID,
			'IS_PARCEL_PICTURE'     => $attachment->isParcelPicture,
			'DIGITAL_SIGNATURE'     => (int)$attachment->digitalSignature,
			'IS_CONFIDENTIAL'       => (int)$attachment->isConfidential,
		);
	}

	public function getParcelPictures($instanceId) {
		$select = $this->model->select()
			->where('"INSTANCE_ID" = ?', $instanceId)
			->where('"IS_PARCEL_PICTURE" = 1');

		$rows = $this->model->fetchAll($select);

		# apparently it's ok to deliver more than one
		$results = array();
		foreach ($rows as $row) {
			$results[] = $this->rowToModel($row);
		}

		return $results;

	}

	public function getAttachments($instanceId, $attachmentSectionID) {
		$select = $this->model->select()
			->where('"INSTANCE_ID" = ?', $instanceId)
			->where('"ATTACHMENT_SECTION_ID" = ?', $attachmentSectionID );

		$rows = $this->model->fetchAll($select);

		$results = array();
		foreach ($rows as $row) {
			$results[] = $this->rowToModel($row);
		}

		return $results;
	}

	public function findByIdentifier($identifier) {
		$res = $this->model->fetchRow($this->model->select()
			->where('IDENTIFIER = ? ', $identifier)
		);

		return $res ? $this->rowToModel($res) : null;
	}
}
