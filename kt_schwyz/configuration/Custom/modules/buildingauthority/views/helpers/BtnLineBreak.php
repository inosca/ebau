<?php

class Buildingauthority_View_Helper_BtnLineBreak extends Zend_View_Helper_Abstract {

	public function btnLineBreak($text) {
		return str_replace(',', '<br>', $text);
	}
}
