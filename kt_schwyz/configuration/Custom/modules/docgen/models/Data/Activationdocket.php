<?php
/**
 * Docgen_Model_Data_Activationdocket
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\Data
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */

/**
 * Docgen_Model_Data_Activationdocket
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Model\Data
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Model_Data_Activationdocket
{
	public $activationDocketId;
	public $instanceId;
	public $activationId;
	public $text;

	/**
	 * Constructor.
	 *
	 * @param int    $activationDocketId The ID of the docket.
	 * @param int    $instanceId         The ID of the instance.
	 * @param int    $activationId       The ID of the activation.
	 * @param string $text               The comment text for the
	 *                                   docket.
	 */
	public function __construct(
		$activationDocketId,
		$instanceId,
		$activationId,
		$text
	) {
		$this->activationDocketId = $activationDocketId;
		$this->instanceId         = $instanceId;
		$this->activationId       = $activationId;
		$this->text               = $text;
	}
}
