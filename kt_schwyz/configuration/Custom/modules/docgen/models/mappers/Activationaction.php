<?php
/**
 * Docgen_Model_Mapper_Activationaction class file.
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
 * Docgen_Model_Mapper_Activationaction class.
 * Data mapper for activation actions.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\Mapper
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Model_Mapper_Activationaction
{
	protected $model;

	/**
	 * Constructor.
	 */
	public function __construct()
	{
		$this->model = new Docgen_Model_DbTable_Activationaction();
	}

	/**
	 * Inserts a new activation action
	 * into database.
	 *
	 * @param Docgen_Model_Data_Activationaction
	 * $activationAction The activation action model containing the data.
	 *
	 * @return int The result of the database insertion whereas 0 means not
	 *             successful and 1 means successful.
	 */
	public function insert(Docgen_Model_Data_Activationaction $activationAction)
	{
		$data = array(
			'NAME' => $activationAction->name
		);

		return $this->model->insert($data);
	}

	/**
	 * Updates an existing activation action
	 * within database.
	 *
	 * @param Docgen_Model_Data_Activationaction
	 * $activationAction The activation action model containing the data.
	 *
	 * @return int The result of the database update whereas 0 means not
	 *             successful and 1 means successful.
	 */
	public function update(Docgen_Model_Data_Activationaction $activationAction)
	{
		$data = array(
			'NAME' => $activationAction->name
		);

		return $this->model->update(
			$data,
			array('DOCGEN_ACTIVATION_ACTION_ID = ?' => $activationAction->actionId)
		);
	}

	/**
	 * Deletes an existing activation action
	 * from database.
	 *
	 * @param int $actionId The identifier of the activation action.
	 *
	 * @return int The result of the database deletion whereas 0 means not
	 *             successful and 1 means successful.
	 */
	public function delete($actionId)
	{
		return $this->model->delete(
			array(
				'DOCGEN_ACTIVATION_ACTION_ID = ?' => $actionId
			)
		);
	}

	/**
	 * Fetches all existing activation actions
	 * from database.
	 *
	 * @return array All available activation actions from database
	 *               in form of an array.
	 */
	public function getActivationActions()
	{
		$rows = $this->model->fetchAll();

		$results = array();

		foreach ($rows as $row) {
			$results[] = new Docgen_Model_Data_Activationaction(
				$row->DOCGEN_ACTIVATION_ACTION_ID,
				$row->NAME
			);
		}

		return $results;
	}

	/**
	 * Fetches a single activation action
	 * by a given identifier if it exists.
	 *
	 * @param int $actionId The identifier of the activation action.
	 *
	 * @return Docgen_Model_Data_Activationaction The found activation action object.
	*/
	public function getActivationAction($actionId)
	{
		$row = $this->model->find($actionId)->current();

		if (!$row) {
			throw new Exception(
				sprintf("Activation action with id %s not found", $actionId)
			);
		}
		$activationAction = new Docgen_Model_Data_Activationaction(
			$row->DOCGEN_ACTIVATION_ACTION_ID,
			$row->NAME
		);

		return $activationAction;
	}

}
