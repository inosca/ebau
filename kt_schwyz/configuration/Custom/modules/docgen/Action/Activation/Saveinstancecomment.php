<?php
/**
 * Docgen_Action_Activation_Saveinstancecomment class file.
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
 * Docgen_Action_Activation_Saveinstancecomment class.
 * Saves comments for instances submitted by POST.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_Saveinstancecomment
{
	/**
	 * Handles the saving of a comment for an instance.
	 *
	 * @param bool $previousSuccess Indicator whether the previous
	 *                              action was successful or not.
	 *
	 * @return void
	 *
	 * @SuppressWarnings(UnusedFormalParameter)
	 */
	public function handleAction($previousSuccess) {
		$request     = Zend_Controller_Front::getInstance()->getRequest();
		$instanceId  = $request->getPost('instance_id');
		$commentText = nl2br($request->getPost('instance_comment_text'));
		$result      = true;

		try {
			$commentMapper = new Docgen_Model_Mapper_Activationdocket();
			$instanceComment = $commentMapper->getEntry(
				$instanceId
			);

			// @codingStandardsIgnoreStart
			// The ignoring of coding standards
			// is set as PHP CodeSniffer does not
			// seem to like the 'else' keyword on its
			// own line.
			if (isset($instanceComment)) {
				if (!empty($commentText)) {
					$instanceComment->text = $commentText;
					$commentMapper->update($instanceComment);
				}
				else {
					$commentMapper->delete($instanceComment);
				}
			}
			else {
				if (!empty($commentText)) {
					$instanceComment = new Docgen_Model_Data_Activationdocket(
						null,
						$instanceId,
						null,
						$commentText
					);
					$commentMapper->insert($instanceComment);
				}
			}
			// @codingStandardsIgnoreEnd
		}
		catch (\Exception $e) {
			Zend_Registry::get('log')->log(
				sprintf(
					'There was an error saving the instance comment: %s',
					$e->getMessage()
				),
				Zend_Log::ERR
			);
			$result = false;
		}

		return $result;
	}
}
