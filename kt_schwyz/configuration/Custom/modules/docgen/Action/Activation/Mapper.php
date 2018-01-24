<?php
/**
 * Docgen_Action_Activation_Mapper class file.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Action_Activation_Mapper class.
 * Mapper for handling activation actions
 * within the CAMAC backend.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_Mapper
{

	protected $model;

	/**
	 * Constructor.
	 */
	public function __construct()
	{
		$this->model = new Docgen_Action_Activation_DbTable();
	}

	/**
	 * Saves an activation action for the given action.
	 *
	 * @param Docgen_Action_Activation_Data $activationAction The
	 * object holding the activation action data.
	 *
	 * @return void
	 */
	public function save(Docgen_Action_Activation_Data $activationAction)
	{
		$data = array(
			'DOCGEN_ACTIVATION_ACTION_ID'
			=> $activationAction->getActivationactionId(),
			'ACTION_ID'   => $activationAction->getActionId()
		);

		$this->model->insert($data);
	}

	/**
	 * Updates an activation action for the given action.
	 *
	 * @param Docgen_Action_Activation_Data $activationAction The
	 * object holding the activation action data.
	 *
	 * @return void
	 */
	public function update(Docgen_Action_Activation_Data $activationAction)
	{
		$data = array(
			'DOCGEN_ACTIVATION_ACTION_ID'
			=> $activationAction->getActivationactionId(),
		);

		$this->model->update(
			$data,
			array(
				'ACTION_ID = ?' => $activationAction->getActionId()
			)
		);
	}

	/**
	 * Deletes the action by the given identifier.
	 *
	 * @param int $actionId The identifier of the action.
	 *
	 * @return void
	 */
	public function delete($actionId)
	{
		$this->model->delete(array('ACTION_ID = ?' => $actionId));
	}

	/**
	 * Gets the activation action identified by the given
	 * identifier if existing.
	 *
	 * @param int $actionId The identifier of the activation action.
	 *
	 * @return Docgen_Action_Activation_Data The object containing the activation
	 *                                       action data.
	 */
	public function getActivationAction($actionId)
	{
		$sel = $this->model->select()
			->from('DOCGEN_ACTIVATIONACTION_ACTION', "*")
			->joinLeft(
				'ACTION',
				'ACTION.ACTION_ID = DOCGEN_ACTIVATIONACTION_ACTION.ACTION_ID'
			)
			->where('DOCGEN_ACTIVATIONACTION_ACTION.ACTION_ID = ?', $actionId)
			->setIntegrityCheck(false);
		$row = $this->model->fetchAll($sel)->current();

		$result = new Docgen_Action_Activation_Data(
			$row->ACTION_ID,
			$row->AVAILABLE_ACTION_ID,
			$row->BUTTON_ID,
			$row->NAME,
			$row->DESCRIPTION,
			$row->SUCCESS_MESSAGE,
			$row->ERROR_MESSAGE,
			$row->EXECUTE_ALWAYS,
			$row->SORT,
			$row->DOCGEN_ACTIVATION_ACTION_ID
		);

		return $result;
	}
}
