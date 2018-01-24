<?php

class Billing_InstanceResource_Billing_Form extends Admin_Form_Resource_InstanceResource {


	public function populate(Camac_Model_Data_Resource_InstanceResource $resource) {

		$values = array();
	
		return parent::populate($values, $resource);
	}
}

