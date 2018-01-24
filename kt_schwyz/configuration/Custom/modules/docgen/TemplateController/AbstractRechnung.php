<?php

abstract class Docgen_TemplateController_AbstractRechnung extends Docgen_TemplateController_DocxController {

	protected function getTagNames() {
		return array();
	}

	protected function getIndividualTags() {

		$instLocMapper = new Application_Model_Mapper_InstanceLocation();
		$locations = $instLocMapper->getInstanceLocations($this->instanceId);
		$instanceLocation = $locations[0];

		// there is no mapper for location :(

		$dbAdapter = Zend_Db_Table::getDefaultAdapter();
		$locations = $dbAdapter->fetchAll(
			$dbAdapter->select()
			->from('LOCATION')
			->where('LOCATION_ID = ?', $instanceLocation->getLocationId())
		);

		// Calculate fees
		$billingMapper = new Billing_Model_Mapper_Entry();
		$fees = 0;
		foreach ($billingMapper->getUninvoicedEntries($this->instanceId, $this->getType()) as $entry) {
			$fees += $entry->actualAmount;
		}

		// Prepare intent
		if (isset($this->questionTags['c21q97i1'])) {
			$intent = implode(', ', $this->questionTags['c21q97i1']);
			if (strlen($this->questionTags['c21q98i1']) > 0) {
				$intent .= ', ' . $this->questionTags['c21q98i1'];
			}
		}
		elseif (isset ($this->questionTags['c101q98i1'])) {
			$intent = $this->questionTags['c101q98i1'];
		}
		elseif (isset($this->questionTags['c102q96i1'])) {
			$intent = $this->questionTags['c102q96i1'];
		}

		$tags = array(
			'community' => $locations[0]['NAME'],
			'date'      => date('d.m.Y'),
			'intent'    => $intent,
			'feeSum'    => sprintf('%01.2f', $fees)
		);

		return $tags;
	}

	protected function getMergeBlockData() {
		$billingEntryMapper   = new Billing_Model_Mapper_Entry();
		$billingAccountMapper = new Billing_Model_Mapper_Account();

		$result = array();
		foreach ($billingEntryMapper->getUninvoicedEntries($this->instanceId, $this->getType()) as $entry) {
			$account = $billingAccountMapper->getAccount($entry->billingAccountID);

			$row = array(
				'DEPARTMENT'     => $account->department,
				'NAME'           => $account->name,
				'ACCOUNT_NUMBER' => $account->accountNumber,
				'AMOUNT'         => sprintf('%01.2f', $entry->actualAmount)
			);

			$result[] = $row;
		}

		return array(
			'f' => $result
		);
	}

	abstract protected function getType();
}
