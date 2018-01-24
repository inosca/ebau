<?php

abstract class Custom_CamacMapper {

	protected $model;
	protected $pk_method;
	protected $pk_prop;

	public function __construct() {
		$this->model = new $this->dbTable();
	}

	public function save($model) {
		$pk = $this->pk_method ? $model->{$this->pk_method}() : $model->{$this->pk_prop};
		if ($pk !== null) {
			return $this->update($model);
		}

		return $this->model->insert($this->modelToRow($model));
	}

	public function update($model) {
		$search = array();
		$pk = $this->pk_method ?
			$model->{$this->pk_method}() :
			$model->{$this->pk_prop};

		if (!$pk) {
			throw new Exception('Could not retrieve a primary key: Check if "pk_prop" or "pk_method"
				are specified and valid');
		}
		$search[$this->pk_col.' = ?'] = $pk;
		return $this->model->update(
			$this->modelToRow($model),
			$search
		);
	}

	public function getEntry($id) {
		$row = $this->model->find($id)->current();
		return $row
			? $this->rowToModel($row->toArray())
			: NULL;
	}

	public function getAll($select = NULL) {
		$select = $select ? $select : $this->model->select();

		return array_map(array($this, 'rowToModel'), $this->model->fetchAll($select)->toArray());
	}

	public function delete($id) {
		$search = array();
		$search[$this->pk_col.' = ?'] = $id;
		$this->model->delete($search);
	}

	abstract function rowToModel($row);
	abstract function modelToRow($model);

}
