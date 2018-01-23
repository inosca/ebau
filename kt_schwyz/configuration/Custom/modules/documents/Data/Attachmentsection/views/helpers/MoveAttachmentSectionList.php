<?php

class Zend_View_Helper_MoveAttachmentSectionList extends Zend_View_Helper_Abstract {

	/**
	 * Generates the first level of the list.
	 *
	 * @return string
	 */
	public function moveattachmentSectionList() {
		$attachmentSectionMapper = new Documents_Model_Mapper_AttachmentSection();
		$attachmentSections  = $attachmentSectionMapper->getEntries();

		$output = '';

		if ($attachmentSections) {

			$i = 0;
			$last = count($attachmentSections);
			$output .= '<div class="row">';
			foreach ($attachmentSections as $attachmentSection) {

				$output .= '<div class="row-container' . ($attachmentSection->attachmentSectionID == $this->view->attachmentSectionID ? ' current' : '') . '">
								<div class="content-row">
									<div class="column column-100">
										<a class="move-item" href="' . $this->view->url(array(
														'action' => 'move',
														'attachmentSection-list-id' => $this->view->attachmentSectionID,
														'target-id' => $attachmentSection->attachmentSectionID,
														'mode' => 'before')) . '"
											>
											<span>
											' . $this->view->translate('Move here') . '
											</span>
										</a>
									</div>
								</div>
								<div class="content-row item">
									<div class="column column-100">
										<span>' . $this->view->escape($attachmentSection->name) . '</span>
									</div>
								</div>';
				$i++;
				if ($i == $last) {
					$output .= '<div class="content-row">
									<div class="column column-100">
										<a class="move-item" href="' . $this->view->url(array(
													'action' => 'move',
													'attachmentSection-list-id' => $this->view->attachmentSectionID,
													'target-id' => $attachmentSection->attachmentSectionID,
													'mode' => 'after')) . 
											'">
											<span>
											' . $this->view->translate('Move here') . '
											</span>
										</a>
									</div>
								</div>';
				}
				$output .= '</div>';
			}
			$output .= '</div>';
		}
		else {
			$output.='<div class="row-container">
								<div class="content-row">
									<div class="column column-100">
										<a class="move-item" href="' . $this->view->url(array('action' => 'move', 'attachmentSection-list-id' => $this->view->attachmentSectionId, 'target-attachmentSection-list-id' => NULL, 'mode' => 'before')) . '">
											<span>
											' . $this->view->translate('Move here') . '
											</span>
										</a>
									</div>
								</div>';
		}

		return $output;

	}

}
