<?php

class Workflow_Model_DbTable_WorkflowItem extends Zend_Db_Table_Abstract {

	protected $_name = 'WORKFLOW_ITEM';

	protected $_primary = "WORKFLOW_ITEM_ID";

	protected $_sequence = "WORKFLOW_ITEM_SEQ";

}
