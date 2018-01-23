<?php

/**
 * This class implements session handling for i-web portal users
 *
 * @author Christian Zosel <christian.zosel@adfinis-sygroup.ch>
 * @package Portal\Model\Mapper
 */
class Portal_Model_Mapper_Session {

	/**
	 * Generate a new hash for a given portal user ID
	 *
	 * @param string $portalId The portal user ID
	 * @return String hash
	 */
	public static function getNewSession($portalId) {
		$hash = bin2hex(openssl_random_pseudo_bytes(32));
		self::add($portalId, $hash);
		return $hash;
	}

	/**
	 * Get overview of saved dossiers for given portal user ID
	 *
	 * @param string $portalId The portal user ID
	 * @return array
	 */
	public static function getOverview($portalId) {
		$instancePortalTable = new Portal_Model_DbTable_InstancePortal();
		$select = $instancePortalTable->select(Zend_Db_Table::SELECT_WITH_FROM_PART)
			->setIntegrityCheck(false)
			->join('INSTANCE', 'INSTANCE.INSTANCE_ID = INSTANCE_PORTAL.INSTANCE_ID')
			->join('INSTANCE_STATE_DESCRIPTION', 'INSTANCE_STATE_DESCRIPTION.INSTANCE_STATE_ID = INSTANCE.INSTANCE_STATE_ID',
				array('DESCRIPTION')
			)
			->join('FORM', 'FORM.FORM_ID = INSTANCE.FORM_ID', array('NAME'))
			->joinLeft('ANSWER_DOK_NR', 'INSTANCE_PORTAL.INSTANCE_ID = ANSWER_DOK_NR.INSTANCE_ID', array('ANSWER'))
			->joinLeft('INSTANCE_LOCATION', 'INSTANCE_PORTAL.INSTANCE_ID = INSTANCE_LOCATION.INSTANCE_ID', array('LOCATION_ID'))
			->joinLeft('LOCATION', 'LOCATION.LOCATION_ID = INSTANCE_LOCATION.LOCATION_ID', array('COMMUNITY' => 'NAME'))
			->where('PORTAL_IDENTIFIER = ?', $portalId)
			->where('INSTANCE.INSTANCE_STATE_ID NOT IN (?)', array(
				Custom_UriConstants::INSTANCE_STATE_ARCH,
				Custom_UriConstants::INSTANCE_STATE_DEL
			))
			->order('INSTANCE_PORTAL.INSTANCE_ID ASC');
		$result = $instancePortalTable->fetchAll($select)->toArray();

		return array_map(function ($row) {
			return array(
				'id'            => $row['INSTANCE_ID'],
				'nr'            => $row['ANSWER'],
				'name'          => self::makeFormTitle($row['NAME']),
				'last_modified' => Custom_Date::dbDateToView($row['MODIFICATION_DATE']),
				'status'        => $row['DESCRIPTION'],
				'community'     => $row['COMMUNITY']
			);
		}, $result);
	}

	/**
	 * Only return the first part of the form
	 *
	 * see configuration/views/helpers/FormTitle::formTitle for
	 * further documentation
	 * @return first part of the form title
	 */
	protected static function makeFormTitle($formTitle) {
		$formTitleParts = explode(' ', $formTitle);

		return $formTitleParts[0];
	}

	/**
	 * Returns if a portal user has access to a specific instance.
	 *
	 * @param string $instanceId
	 * @return bool
	 */
	public static function hasAccess($instanceId) {
		$session = new Zend_Session_Namespace('portal');
		$instancePortalTable = new Portal_Model_DbTable_InstancePortal();
		$row = $instancePortalTable->find($instanceId)->current();
		return $row && $row->PORTAL_IDENTIFIER === $session->id;
	}

	/**
	 * Returns the portal user ID for a given hash, or false if no valid
	 * user was found.
	 *
	 * @param string $hash The session hash
	 * @return string|boolean the portal user ID or false
	 */
	public static function getUserByHash($hash) {
		$table = new Portal_Model_DbTable_PortalSession();
		$lifetime = Zend_Registry::get('config')->portal->session->lifetime;

		$select = $table->select()
			->where('PORTAL_SESSION_ID = ?', $hash)
			->where('LAST_ACTIVE > ?', Camac_Date::getDbStringFromDateTime(
				date_sub(
					new DateTime(),
					date_interval_create_from_date_string($lifetime)
				)
			));

		$row = $table->fetchRow($select);

		if (!$row) {
			return false;
		}

		$row->LAST_ACTIVE = Camac_Date::getDbStringFromDateTime(new DateTime());
		$row->save();
		return $row->PORTAL_IDENTIFIER;
	}

	/**
	 * Save a portalId-hash pair.
	 *
	 * @param string $portalId The portal user ID
	 * @param string $hash The session hash
	 * @return void
	 */
	private static function add($portalId, $hash) {
		$table = new Portal_Model_DbTable_PortalSession();
		$data = array(
			'PORTAL_SESSION_ID' => $hash,
			'PORTAL_IDENTIFIER' => $portalId,
			'LAST_ACTIVE'       => Camac_Date::getDbStringFromDateTime(new DateTime())
		);

		$table->insert($data);
	}

	/**
	 * Delete a session
	 *
	 * @param string $hash The session hash
	 * @return boolean true if session was found and deleted
	 */
	public static function logout($hash) {
		$table = new Portal_Model_DbTable_PortalSession();
		$row = $table->find($hash)->current();
		if ($row) {
			$row->delete();
			return true;
		} else {
			return false;
		}
	}
}

?>
