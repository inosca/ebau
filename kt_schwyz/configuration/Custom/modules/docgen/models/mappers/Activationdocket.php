<?php
/**
 * Docgen_Model_Mapper_Activationdocket class file.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\Mapper
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Model_Mapper_Activationdocket class.
 * Data mapper for dockets.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\Mapper
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Model_Mapper_Activationdocket
{
	protected $model;

	/**
	 * Constructor.
	 */
	public function __construct() {
		$this->model = new Docgen_Model_DbTable_Activationdocket();
	}

	/**
	 * Inserts a new activation docket
	 * into database.
	 *
	 * @param Docgen_Model_Data_Activationdocket
	 * $activationDocket The activation docket model containing the data.
	 *
	 * @return int The result of the database insertion whereas 0 means not
	 *             successful and 1 means successful.
	 */
	public function insert(Docgen_Model_Data_Activationdocket $activationDocket) {
		$data = array(
			'INSTANCE_ID'   => $activationDocket->instanceId,
			'TEXT'          => $activationDocket->text
		);

		if (!empty($activationDocket->activationId)) {
			$data['ACTIVATION_ID'] = $activationDocket->activationId;
		}

		return $this->model->insert($data);
	}

	/**
	 * Updates an existing activation docket
	 * within database.
	 *
	 * @param Docgen_Model_Data_Activationdocket
	 * $activationDocket The activation docket model containing the data.
	 *
	 * @return int The result of the database update whereas 0 means not
	 *             successful and 1 means successful.
	 */
	public function update(Docgen_Model_Data_Activationdocket $activationDocket) {
		$data = array(
			'INSTANCE_ID'                 => $activationDocket->instanceId,
			'TEXT'                        => $activationDocket->text
		);

		if (!empty($activationDocket->activationId)) {
			$data['ACTIVATION_ID'] = $activationDocket->activationId;
		}

		return $this->model->update(
			$data,
			array(
				'DOCGEN_ACTIVATION_DOCKET_ID = ?'
				=> $activationDocket->activationDocketId
			)
		);
	}

	/**
	 * Deletes an existing activation docket
	 * from database.
	 *
	 * @param Docgen_Model_Data_Activationdocket
	 * $activationDocket The activation docket object to delete.
	 *
	 * @return int The result of the database deletion whereas 0 means not
	 *             successful and 1 means successful.
	 */
	public function delete(Docgen_Model_Data_Activationdocket $activationDocket) {
		return $this->model->delete(
			array(
				'DOCGEN_ACTIVATION_DOCKET_ID = ?'
				=> $activationDocket->activationDocketId
			)
		);
	}

	/**
	 * Gets a single entry of an activation docket
	 * from database.
	 *
	 * @param int $instanceId   The identifier of the instance of the docket.
	 * @param int $activationId The identifier of the activation of the docket.
	 *
	 * @return Docgen_Model_Data_Activationdocket The found activation docket object.
	 */
	public function getEntry($instanceId, $activationId=null) {
		$select = $this->model->select();
		$select->where('INSTANCE_ID = ?', $instanceId);

		// @codingStandardsIgnoreStart
		if (empty($activationId)) {
			$select->where('ACTIVATION_ID IS NULL');
		}
		else {
			$select->where('ACTIVATION_ID = ?', $activationId);
		}
		// @codingStandardsIgnoreEnd
		
		$rows = $this->model->fetchAll($select);

		$result = null;

		foreach ($rows as $row) {
			$result = new Docgen_Model_Data_Activationdocket(
				$row->DOCGEN_ACTIVATION_DOCKET_ID,
				$row->INSTANCE_ID,
				$row->ACTIVATION_ID,
				$row->TEXT
			);
		}

		return $result;
	}
}
