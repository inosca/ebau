<?php

class Documents_View_Helper_MakeLink extends Zend_View_Helper_Abstract {

	public function makeLink($attachment) {
		$urlHelper  = new Zend_Controller_Action_Helper_Url();
		$identifier = $attachment->identifier;
		$href       = $urlHelper->url(array('action' => 'download', 'attachmentid' => $identifier));
		$name       = $attachment->name;

		$extension = strtolower(pathinfo($name, PATHINFO_EXTENSION));
		$hasPreview = true;
		if ($extension == 'itf') {
			$baseUrl = new Zend_View_Helper_BaseUrl();
			$rel = $baseUrl->baseUrl("public/images/uri/interlisdatei.png");
		}
		else if (strtolower($extension) == 'docx') {
			$hasPreview = false;
		}
		else if (strtolower($extension) == 'jpg') {
			$rel = $href;
		}
		else {
			$rel = $urlHelper->url(array('action' => 'preview', 'attachmentid'  => $identifier));
		}

		return $hasPreview ?
			sprintf('<a class="screenshot" href="%s" rel="%s" target="_blank">%s</a>', 
			$href, $rel, $name) :
			sprintf('<a href="%s" target="_blank">%s</a>', $href, $name);
	}
}
