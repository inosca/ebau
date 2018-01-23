<?php
/**
 * Docgen_Action_Activation_Savedocketcomment class file.
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
 * Docgen_Action_Activation_Savedocketcomment class.
 * Saves comments for dockets based upon a given instance and
 * activation which have to be submitted as POST.
 *
 * PHP VERSION 5
 *
 * @category Docgen
 * @package  Docgen\Action\Activation
 * @author   Sven Osterwalder <sven.osterwalder@adfinis-sygroup.ch>
 * @license  http://www.gnu.org/licenses/lgpl.html LGPLv3
 * @link     None
 */
class Docgen_Action_Activation_Savedocketcomment
{
	/**
	 * Handles the saving of a comment for a docket.
	 *
	 * @param bool $previousSuccess Indicator whether the previous
	 *                              action was successful or not.
	 *
	 * @return void
	 *
	 * @SuppressWarnings(UnusedFormalParameter)
	 */
	public function handleAction($previousSuccess)
	{
		$request           = Zend_Controller_Front::getInstance()->getRequest();
		$instanceId        = $request->getParam('instance-id');
		$activationId      = $request->getPost('activation_id');
		$docketCommentText = nl2br($request->getPost($activationId . '_docket_text'));
		$result            = true;

		try {
			$docketMapper = new Docgen_Model_Mapper_Activationdocket();
			$activationDocket = $docketMapper->getEntry(
				$instanceId,
				$activationId
			);

			// @codingStandardsIgnoreStart
			// The ignoring of coding standards
			// is set as PHP CodeSniffer does not
			// seem to like the 'else' keyword on its
			// own line.
			if (isset($activationDocket)) {
				if (!empty($docketCommentText)) {
					$activationDocket->text = $docketCommentText;
					$docketMapper->update($activationDocket);
				}
				else {
					$docketMapper->delete($activationDocket);
				}
			}
			else {
				if (!empty($docketCommentText)) {
					$activationDocket = new Docgen_Model_Data_Activationdocket(
						null,
						$instanceId,
						$activationId,
						$docketCommentText
					);
					$docketMapper->insert($activationDocket);
				}
			}
			// @codingStandardsIgnoreEnd
		}
		catch (\Exception $e) {
			Zend_Registry::get('log')->log(
				'There was an error saving the docket comment: ' . $e->getMessage(),
				Zend_Log::ERR
			);
			$result = false;
		}

		return $result;
	}
}
