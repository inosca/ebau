<?php
/**
 * Docgen_Action_Activation_DbTable class file.
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
 * Docgen_Action_Activation_DbTable class.
 * Mapper between backend application and database 
 * for activation actions.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_DbTable extends Zend_Db_Table_Abstract
{
	// @codingStandardsIgnoreStart
	protected $_name = 'DOCGEN_ACTIVATIONACTION_ACTION';
	protected $_primary = 'ACTION_ID';
	// @codingStandardsIgnoreEnd
}
