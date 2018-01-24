<?php

class Bab_Model_DbTable_BabUsage extends Zend_Db_Table_Abstract {

	protected $_name = 'BAB_USAGE';

	protected $_primary = ['INSTANCE_ID', 'USAGE_TYPE'];

}
