<?php

class Portal_Model_DbTable_ProjectSubmitterData extends Zend_Db_Table_Abstract {

	/**
	 * The table name.
	 *
	 * @var string
	 */
	protected $_name = 'PROJECT_SUBMITTER_DATA';

	/**
	 * The primary key column or columns.
	 * A compound key should be declared as an array.
	 * You may declare a single-column primary key
	 * as a string.
	 *
	 * @var mixed
	 */
	protected $_primary = 'INSTANCE_ID';

	protected $_sequence = false;
}
