--------------------------------------------------------
--  File created - Wednesday-July-30-2014   
--------------------------------------------------------
-- Unable to render TYPE DDL for object CAMAC_DEV.JSON with DBMS_METADATA attempting internal generator.
CREATE TYPE JSON as object (
  /*
  Copyright (c) 2010 Jonas Krogsboell

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  */

  /* Variables */
  json_data json_value_array,
  check_for_duplicate number,
  
  /* Constructors */
  constructor function json return self as result,
  constructor function json(str varchar2) return self as result,
  constructor function json(str in clob) return self as result,
  constructor function json(cast json_value) return self as result,
  constructor function json(l in out nocopy json_list) return self as result,
    
  /* Member setter methods */  
  member procedure remove(pair_name varchar2),
  member procedure put(self in out nocopy json, pair_name varchar2, pair_value json_value, position pls_integer default null),
  member procedure put(self in out nocopy json, pair_name varchar2, pair_value varchar2, position pls_integer default null),
  member procedure put(self in out nocopy json, pair_name varchar2, pair_value number, position pls_integer default null),
  member procedure put(self in out nocopy json, pair_name varchar2, pair_value boolean, position pls_integer default null),
  member procedure check_duplicate(self in out nocopy json, v_set boolean),
  member procedure remove_duplicates(self in out nocopy json),

  /* deprecated putter use json_value */
  member procedure put(self in out nocopy json, pair_name varchar2, pair_value json, position pls_integer default null),
  member procedure put(self in out nocopy json, pair_name varchar2, pair_value json_list, position pls_integer default null),

  /* Member getter methods */ 
  member function count return number,
  member function get(pair_name varchar2) return json_value, 
  member function get(position pls_integer) return json_value,
  member function index_of(pair_name varchar2) return number,
  member function exist(pair_name varchar2) return boolean,

  /* Output methods */ 
  member function to_char(spaces boolean default true, chars_per_line number default 0) return varchar2,
  member procedure to_clob(self in json, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true),
  member procedure print(self in json, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null), --32512 is maximum
  member procedure htp(self in json, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null),
  
  member function to_json_value return json_value,
  /* json path */
  member function path(json_path varchar2, base number default 1) return json_value,

  /* json path_put */
  member procedure path_put(self in out nocopy json, json_path varchar2, elem json_value, base number default 1),
  member procedure path_put(self in out nocopy json, json_path varchar2, elem varchar2  , base number default 1),
  member procedure path_put(self in out nocopy json, json_path varchar2, elem number    , base number default 1),
  member procedure path_put(self in out nocopy json, json_path varchar2, elem boolean   , base number default 1),
  member procedure path_put(self in out nocopy json, json_path varchar2, elem json_list , base number default 1),
  member procedure path_put(self in out nocopy json, json_path varchar2, elem json      , base number default 1),

  /* json path_remove */
  member procedure path_remove(self in out nocopy json, json_path varchar2, base number default 1),

  /* map functions */
  member function get_values return json_list,
  member function get_keys return json_list

) not final;
-- Unable to render TYPE DDL for object CAMAC_DEV.JSON_LIST with DBMS_METADATA attempting internal generator.
CREATE TYPE JSON_LIST as object (
  /*
  Copyright (c) 2010 Jonas Krogsboell

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  */

  list_data json_value_array,
  constructor function json_list return self as result,
  constructor function json_list(str varchar2) return self as result,
  constructor function json_list(str clob) return self as result,
  constructor function json_list(cast json_value) return self as result,
  
  member procedure append(self in out nocopy json_list, elem json_value, position pls_integer default null),
  member procedure append(self in out nocopy json_list, elem varchar2, position pls_integer default null),
  member procedure append(self in out nocopy json_list, elem number, position pls_integer default null),
  member procedure append(self in out nocopy json_list, elem boolean, position pls_integer default null),
  member procedure append(self in out nocopy json_list, elem json_list, position pls_integer default null),

  member procedure replace(self in out nocopy json_list, position pls_integer, elem json_value),
  member procedure replace(self in out nocopy json_list, position pls_integer, elem varchar2),
  member procedure replace(self in out nocopy json_list, position pls_integer, elem number),
  member procedure replace(self in out nocopy json_list, position pls_integer, elem boolean),
  member procedure replace(self in out nocopy json_list, position pls_integer, elem json_list),

  member function count return number,
  member procedure remove(self in out nocopy json_list, position pls_integer),
  member procedure remove_first(self in out nocopy json_list),
  member procedure remove_last(self in out nocopy json_list),
  member function get(position pls_integer) return json_value,
  member function head return json_value,
  member function last return json_value,
  member function tail return json_list,

  /* Output methods */ 
  member function to_char(spaces boolean default true, chars_per_line number default 0) return varchar2,
  member procedure to_clob(self in json_list, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true),
  member procedure print(self in json_list, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null), --32512 is maximum
  member procedure htp(self in json_list, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null),

  /* json path */
  member function path(json_path varchar2, base number default 1) return json_value,
  /* json path_put */
  member procedure path_put(self in out nocopy json_list, json_path varchar2, elem json_value, base number default 1),
  member procedure path_put(self in out nocopy json_list, json_path varchar2, elem varchar2  , base number default 1),
  member procedure path_put(self in out nocopy json_list, json_path varchar2, elem number    , base number default 1),
  member procedure path_put(self in out nocopy json_list, json_path varchar2, elem boolean   , base number default 1),
  member procedure path_put(self in out nocopy json_list, json_path varchar2, elem json_list , base number default 1),

  /* json path_remove */
  member procedure path_remove(self in out nocopy json_list, json_path varchar2, base number default 1),

  member function to_json_value return json_value
  /* --backwards compatibility
  ,
  member procedure add_elem(self in out nocopy json_list, elem json_value, position pls_integer default null),
  member procedure add_elem(self in out nocopy json_list, elem varchar2, position pls_integer default null),
  member procedure add_elem(self in out nocopy json_list, elem number, position pls_integer default null),
  member procedure add_elem(self in out nocopy json_list, elem boolean, position pls_integer default null),
  member procedure add_elem(self in out nocopy json_list, elem json_list, position pls_integer default null),

  member procedure set_elem(self in out nocopy json_list, position pls_integer, elem json_value),
  member procedure set_elem(self in out nocopy json_list, position pls_integer, elem varchar2),
  member procedure set_elem(self in out nocopy json_list, position pls_integer, elem number),
  member procedure set_elem(self in out nocopy json_list, position pls_integer, elem boolean),
  member procedure set_elem(self in out nocopy json_list, position pls_integer, elem json_list),
  
  member procedure remove_elem(self in out nocopy json_list, position pls_integer),
  member function get_elem(position pls_integer) return json_value,
  member function get_first return json_value,
  member function get_last return json_value
--  */
  
) not final;
-- Unable to render TYPE DDL for object CAMAC_DEV.JSON_VALUE with DBMS_METADATA attempting internal generator.
CREATE TYPE JSON_VALUE as object
( 
  /*
  Copyright (c) 2010 Jonas Krogsboell

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  */

  typeval number(1), /* 1 = object, 2 = array, 3 = string, 4 = number, 5 = bool, 6 = null */
  str varchar2(32767),
  num number, /* store 1 as true, 0 as false */
  object_or_array sys.anydata, /* object or array in here */
  extended_str clob,
  
  /* mapping */
  mapname varchar2(4000),
  mapindx number(32),  
  
  constructor function json_value(object_or_array sys.anydata) return self as result,
  constructor function json_value(str varchar2, esc boolean default true) return self as result,
  constructor function json_value(str clob, esc boolean default true) return self as result,
  constructor function json_value(num number) return self as result,
  constructor function json_value(b boolean) return self as result,
  constructor function json_value return self as result,
  static function makenull return json_value,
  
  member function get_type return varchar2,
  member function get_string(max_byte_size number default null, max_char_size number default null) return varchar2,
  member procedure get_string(self in json_value, buf in out nocopy clob),
  member function get_number return number,
  member function get_bool return boolean,
  member function get_null return varchar2,
  
  member function is_object return boolean,
  member function is_array return boolean,
  member function is_string return boolean,
  member function is_number return boolean,
  member function is_bool return boolean,
  member function is_null return boolean,
  
  /* Output methods */ 
  member function to_char(spaces boolean default true, chars_per_line number default 0) return varchar2,
  member procedure to_clob(self in json_value, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true),
  member procedure print(self in json_value, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null), --32512 is maximum
  member procedure htp(self in json_value, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null),
  
  member function value_of(self in json_value, max_byte_size number default null, max_char_size number default null) return varchar2
  
) not final;
-- Unable to render TYPE DDL for object CAMAC_DEV.JSON_VALUE_ARRAY with DBMS_METADATA attempting internal generator.
CREATE TYPE JSON_VALUE_ARRAY as table of json_value;
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ACTION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ACTION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ACTIVATION_LOG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ACTIVATION_LOG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ACTIVATION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ACTIVATION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ANSWER_LIST_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ANSWER_LIST_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ANSWER_LOG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ANSWER_LOG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ANSWER_QUERY_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ANSWER_QUERY_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ATTACHMENT_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ATTACHMENT_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.A_COPYDATA_MAPPING_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE A_COPYDATA_MAPPING_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.A_LOCATION_QC_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE A_LOCATION_QC_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.BUTTON_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE BUTTON_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.CHAPTER_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE CHAPTER_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.CIRCULATION_ANSWER_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE CIRCULATION_ANSWER_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.CIRCULATION_LOG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE CIRCULATION_LOG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.CIRCULATION_REASON_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE CIRCULATION_REASON_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.CIRCULATION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE CIRCULATION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.CIRCULATION_STATE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE CIRCULATION_STATE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.CIRCULATION_TYPE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE CIRCULATION_TYPE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.FORM_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE FORM_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.GLOSSARY_CATEGORY_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE GLOSSARY_CATEGORY_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.GLOSSARY_SENTENCE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE GLOSSARY_SENTENCE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.GROUP_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE GROUP_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.INSTANCE_DEMO_LOG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE INSTANCE_DEMO_LOG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.INSTANCE_FORM_PDF_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE INSTANCE_FORM_PDF_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.INSTANCE_LOCATION_LOG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE INSTANCE_LOCATION_LOG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.INSTANCE_LOG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE INSTANCE_LOG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.INSTANCE_RESOURCE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE INSTANCE_RESOURCE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.INSTANCE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE INSTANCE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.INSTANCE_STATE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE INSTANCE_STATE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.IR_EDITCIRCULATION_SG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE IR_EDITCIRCULATION_SG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.IR_EDITLETTER_ANSWER_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE IR_EDITLETTER_ANSWER_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.LETTER_IMAGE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE LETTER_IMAGE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.LOCATION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE LOCATION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.MAPPING_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE MAPPING_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.NOTICE_IMAGE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE NOTICE_IMAGE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.NOTICE_LOG_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE NOTICE_LOG_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.NOTICE_TYPE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE NOTICE_TYPE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.PAGE_ANSWER_ACTIVATION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE PAGE_ANSWER_ACTIVATION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.PAGE_FORM_GROUP_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE PAGE_FORM_GROUP_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.PAGE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE PAGE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.PROPOSAL_ACTIVATION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE PROPOSAL_ACTIVATION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.QUESTION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE QUESTION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.RESOURCE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE RESOURCE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.ROLE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE ROLE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.R_LIST_COLUMN_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE R_LIST_COLUMN_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.R_SEARCH_COLUMN_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE R_SEARCH_COLUMN_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.R_SEARCH_FILTER_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE R_SEARCH_FILTER_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.SERVICE_ANSWER_ACTIVATION_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE SERVICE_ANSWER_ACTIVATION_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.SERVICE_GROUP_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE SERVICE_GROUP_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.SERVICE_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE SERVICE_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render SEQUENCE DDL for object CAMAC_DEV.USER_SEQ with DBMS_METADATA attempting internal generator.
CREATE SEQUENCE USER_SEQ INCREMENT BY 1 MAXVALUE 9999999999999999999999999999 MINVALUE 1 CACHE 20
-- Unable to render TABLE DDL for object CAMAC_DEV.ACTION with DBMS_METADATA attempting internal generator.
ALTER TABLE ACTION
ADD CONSTRAINT SYS_C005740 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C008068
ENABLECREATE UNIQUE INDEX SYS_C008068 ON ACTION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ACTION 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, AVAILABLE_ACTION_ID VARCHAR2(25 BYTE) NOT NULL 
, BUTTON_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
, SUCCESS_MESSAGE VARCHAR2(1000 BYTE) 
, ERROR_MESSAGE VARCHAR2(1000 BYTE) 
, EXECUTE_ALWAYS NUMBER(1, 0) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE ACTION
ADD CONSTRAINT FKACTION125375 FOREIGN KEY
(
  AVAILABLE_ACTION_ID 
)
REFERENCES AVAILABLE_ACTION
(
  AVAILABLE_ACTION_ID 
)
ENABLE
ALTER TABLE ACTION
ADD CONSTRAINT FKACTION425470 FOREIGN KEY
(
  BUTTON_ID 
)
REFERENCES BUTTON
(
  BUTTON_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.ACTIVATION with DBMS_METADATA attempting internal generator.
ALTER TABLE ACTIVATION
ADD CONSTRAINT SYS_C005747 PRIMARY KEY 
(
  ACTIVATION_ID 
)
USING INDEX SYS_C008006
ENABLECREATE UNIQUE INDEX SYS_C008006 ON ACTIVATION (ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ACTIVATION 
(
  ACTIVATION_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_PARENT_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_STATE_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) 
, CIRCULATION_ANSWER_ID NUMBER(10, 0) 
, START_DATE DATE NOT NULL 
, DEADLINE_DATE DATE NOT NULL 
, SUSPENSION_DATE DATE 
, END_DATE DATE 
, VERSION NUMBER(10, 0) NOT NULL 
, REASON VARCHAR2(50 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE ACTIVATION
ADD CONSTRAINT FKACTIVATION157025 FOREIGN KEY
(
  CIRCULATION_STATE_ID 
)
REFERENCES CIRCULATION_STATE
(
  CIRCULATION_STATE_ID 
)
ENABLE
ALTER TABLE ACTIVATION
ADD CONSTRAINT FKACTIVATION282993 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE ACTIVATION
ADD CONSTRAINT FKACTIVATION44069 FOREIGN KEY
(
  CIRCULATION_ANSWER_ID 
)
REFERENCES CIRCULATION_ANSWER
(
  CIRCULATION_ANSWER_ID 
)
ENABLE
ALTER TABLE ACTIVATION
ADD CONSTRAINT FKACTIVATION574952 FOREIGN KEY
(
  SERVICE_PARENT_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
ALTER TABLE ACTIVATION
ADD CONSTRAINT FKACTIVATION691704 FOREIGN KEY
(
  CIRCULATION_ID 
)
REFERENCES CIRCULATION
(
  CIRCULATION_ID 
)
ENABLE
ALTER TABLE ACTIVATION
ADD CONSTRAINT FKACTIVATION803860 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.ACTIVATION_LOG with DBMS_METADATA attempting internal generator.
ALTER TABLE ACTIVATION_LOG
ADD CONSTRAINT SYS_C005756 PRIMARY KEY 
(
  ACTIVATION_LOG_ID 
)
USING INDEX SYS_C007941
ENABLECREATE UNIQUE INDEX SYS_C007941 ON ACTIVATION_LOG (ACTIVATION_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ACTIVATION_LOG 
(
  ACTIVATION_LOG_ID NUMBER(10, 0) NOT NULL 
, ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTION VARCHAR2(500 BYTE) NOT NULL 
, DATA CLOB 
, MODIFICATION_DATE DATE NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (DATA) STORE AS SYS_LOB0000017541C00005$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)
-- Unable to render TABLE DDL for object CAMAC_DEV.AIR_ACTION with DBMS_METADATA attempting internal generator.
ALTER TABLE AIR_ACTION
ADD CONSTRAINT SYS_C005762 PRIMARY KEY 
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
, ACTION_NAME 
)
USING INDEX SYS_C007883
ENABLECREATE UNIQUE INDEX SYS_C007883 ON AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID ASC, ACTION_NAME ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE AIR_ACTION 
(
  AVAILABLE_INSTANCE_RESOURCE_ID VARCHAR2(25 BYTE) NOT NULL 
, ACTION_NAME VARCHAR2(50 BYTE) NOT NULL 
, HIDDEN NUMBER(1, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE AIR_ACTION
ADD CONSTRAINT FKAIR_ACTION70708 FOREIGN KEY
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
)
REFERENCES AVAILABLE_INSTANCE_RESOURCE
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.ANSWER with DBMS_METADATA attempting internal generator.
ALTER TABLE ANSWER
ADD CONSTRAINT SYS_C005766 PRIMARY KEY 
(
  INSTANCE_ID 
, QUESTION_ID 
, CHAPTER_ID 
, ITEM 
)
USING INDEX SYS_C008033
ENABLECREATE UNIQUE INDEX SYS_C008033 ON ANSWER (INSTANCE_ID ASC, QUESTION_ID ASC, CHAPTER_ID ASC, ITEM ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ANSWER 
(
  INSTANCE_ID NUMBER(10, 0) NOT NULL 
, QUESTION_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, ITEM NUMBER(10, 0) NOT NULL 
, ANSWER VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE ANSWER
ADD CONSTRAINT FKANSWER128151 FOREIGN KEY
(
  QUESTION_ID 
)
REFERENCES QUESTION
(
  QUESTION_ID 
)
ENABLE
ALTER TABLE ANSWER
ADD CONSTRAINT FKANSWER69673 FOREIGN KEY
(
  CHAPTER_ID 
)
REFERENCES CHAPTER
(
  CHAPTER_ID 
)
ENABLE
ALTER TABLE ANSWER
ADD CONSTRAINT FKANSWER732538 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.ANSWER_LIST with DBMS_METADATA attempting internal generator.
ALTER TABLE ANSWER_LIST
ADD CONSTRAINT SYS_C005772 PRIMARY KEY 
(
  ANSWER_LIST_ID 
)
USING INDEX SYS_C008275
ENABLECREATE UNIQUE INDEX SYS_C008275 ON ANSWER_LIST (ANSWER_LIST_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ANSWER_LIST 
(
  ANSWER_LIST_ID NUMBER(10, 0) NOT NULL 
, QUESTION_ID NUMBER(10, 0) NOT NULL 
, VALUE VARCHAR2(20 BYTE) NOT NULL 
, NAME VARCHAR2(300 BYTE) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE ANSWER_LIST
ADD CONSTRAINT FKANSWER_LIS836630 FOREIGN KEY
(
  QUESTION_ID 
)
REFERENCES QUESTION
(
  QUESTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.ANSWER_LOG with DBMS_METADATA attempting internal generator.
ALTER TABLE ANSWER_LOG
ADD CONSTRAINT SYS_C005789 PRIMARY KEY 
(
  ANSWER_LOG_ID 
)
USING INDEX SYS_C007955
ENABLECREATE UNIQUE INDEX SYS_C007955 ON ANSWER_LOG (ANSWER_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ANSWER_LOG 
(
  ANSWER_LOG_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTION VARCHAR2(500 BYTE) NOT NULL 
, DATA CLOB 
, ID1 NUMBER(10, 0) NOT NULL 
, FIELD1 VARCHAR2(30 BYTE) NOT NULL 
, ID2 NUMBER(10, 0) NOT NULL 
, FIELD2 VARCHAR2(30 BYTE) NOT NULL 
, ID3 NUMBER(10, 0) NOT NULL 
, FIELD3 VARCHAR2(30 BYTE) NOT NULL 
, ID4 NUMBER(10, 0) NOT NULL 
, FIELD4 VARCHAR2(30 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (DATA) STORE AS SYS_LOB0000017547C00005$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)
-- Unable to render TABLE DDL for object CAMAC_DEV.ANSWER_QUERY with DBMS_METADATA attempting internal generator.
ALTER TABLE ANSWER_QUERY
ADD CONSTRAINT SYS_C005791 PRIMARY KEY 
(
  ANSWER_QUERY_ID 
)
USING INDEX SYS_C008279
ENABLECREATE UNIQUE INDEX SYS_C008279 ON ANSWER_QUERY (ANSWER_QUERY_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ANSWER_QUERY 
(
  ANSWER_QUERY_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, QUERY VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.AR_ACTION with DBMS_METADATA attempting internal generator.
ALTER TABLE AR_ACTION
ADD CONSTRAINT SYS_C005795 PRIMARY KEY 
(
  AVAILABLE_RESOURCE_ID 
, ACTION_NAME 
)
USING INDEX SYS_C007887
ENABLECREATE UNIQUE INDEX SYS_C007887 ON AR_ACTION (AVAILABLE_RESOURCE_ID ASC, ACTION_NAME ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE AR_ACTION 
(
  AVAILABLE_RESOURCE_ID VARCHAR2(25 BYTE) NOT NULL 
, ACTION_NAME VARCHAR2(50 BYTE) NOT NULL 
, HIDDEN NUMBER(1, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE AR_ACTION
ADD CONSTRAINT FKAR_ACTION621488 FOREIGN KEY
(
  AVAILABLE_RESOURCE_ID 
)
REFERENCES AVAILABLE_RESOURCE
(
  AVAILABLE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.ATTACHMENT with DBMS_METADATA attempting internal generator.
ALTER TABLE ATTACHMENT
ADD CONSTRAINT ATTACHMENT_PK PRIMARY KEY 
(
  ATTACHMENT_ID 
)
USING INDEX ATTACHMENT_PK
ENABLECREATE UNIQUE INDEX ATTACHMENT_PK ON ATTACHMENT (ATTACHMENT_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ATTACHMENT 
(
  ATTACHMENT_ID NUMBER NOT NULL 
, NAME VARCHAR2(255 BYTE) NOT NULL 
, INSTANCE_ID NUMBER NOT NULL 
, PATH VARCHAR2(255 BYTE) NOT NULL 
, "SIZE" NUMBER NOT NULL 
, "DATE" DATE NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, IDENTIFIER VARCHAR2(255 BYTE) NOT NULL 
, MIME_TYPE VARCHAR2(255 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE ATTACHMENT
ADD CONSTRAINT ATTACHMENT_FK1 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ON DELETE CASCADE ENABLE
ALTER TABLE ATTACHMENT
ADD CONSTRAINT ATTACHMENT_USER_FK FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.AVAILABLE_ACTION with DBMS_METADATA attempting internal generator.
ALTER TABLE AVAILABLE_ACTION
ADD CONSTRAINT SYS_C005809 PRIMARY KEY 
(
  AVAILABLE_ACTION_ID 
)
USING INDEX SYS_C008071
ENABLECREATE UNIQUE INDEX SYS_C008071 ON AVAILABLE_ACTION (AVAILABLE_ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE AVAILABLE_ACTION 
(
  AVAILABLE_ACTION_ID VARCHAR2(25 BYTE) NOT NULL 
, MODULE_NAME VARCHAR2(50 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE with DBMS_METADATA attempting internal generator.
ALTER TABLE AVAILABLE_INSTANCE_RESOURCE
ADD CONSTRAINT SYS_C005812 PRIMARY KEY 
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C008109
ENABLECREATE UNIQUE INDEX SYS_C008109 ON AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE AVAILABLE_INSTANCE_RESOURCE 
(
  AVAILABLE_INSTANCE_RESOURCE_ID VARCHAR2(25 BYTE) NOT NULL 
, MODULE_NAME VARCHAR2(50 BYTE) NOT NULL 
, CONTROLLER_NAME VARCHAR2(50 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.AVAILABLE_RESOURCE with DBMS_METADATA attempting internal generator.
ALTER TABLE AVAILABLE_RESOURCE
ADD CONSTRAINT SYS_C005816 PRIMARY KEY 
(
  AVAILABLE_RESOURCE_ID 
)
USING INDEX SYS_C008207
ENABLECREATE UNIQUE INDEX SYS_C008207 ON AVAILABLE_RESOURCE (AVAILABLE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE AVAILABLE_RESOURCE 
(
  AVAILABLE_RESOURCE_ID VARCHAR2(25 BYTE) NOT NULL 
, MODULE_NAME VARCHAR2(50 BYTE) NOT NULL 
, CONTROLLER_NAME VARCHAR2(50 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.A_CHECKQUERY with DBMS_METADATA attempting internal generator.
ALTER TABLE A_CHECKQUERY
ADD CONSTRAINT SYS_C005820 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C008027
ENABLECREATE UNIQUE INDEX SYS_C008027 ON A_CHECKQUERY (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_CHECKQUERY 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, QUERY VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_CHECKQUERY
ADD CONSTRAINT FKA_CHECKQUE428973 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_CIRCULATIONTRANSITION with DBMS_METADATA attempting internal generator.
ALTER TABLE A_CIRCULATIONTRANSITION
ADD CONSTRAINT SYS_C005823 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C007838
ENABLECREATE UNIQUE INDEX SYS_C007838 ON A_CIRCULATIONTRANSITION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_CIRCULATIONTRANSITION 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, CURRENT_CIRCULATION_STATE_ID NUMBER(10, 0) 
, NEXT_CIRCULATION_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_CIRCULATIONTRANSITION
ADD CONSTRAINT FKA_CIRCULAT488256 FOREIGN KEY
(
  NEXT_CIRCULATION_STATE_ID 
)
REFERENCES CIRCULATION_STATE
(
  CIRCULATION_STATE_ID 
)
ENABLE
ALTER TABLE A_CIRCULATIONTRANSITION
ADD CONSTRAINT FKA_CIRCULAT722268 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
ALTER TABLE A_CIRCULATIONTRANSITION
ADD CONSTRAINT FKA_CIRCULAT832134 FOREIGN KEY
(
  CURRENT_CIRCULATION_STATE_ID 
)
REFERENCES CIRCULATION_STATE
(
  CIRCULATION_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_COPYDATA with DBMS_METADATA attempting internal generator.
ALTER TABLE A_COPYDATA
ADD CONSTRAINT SYS_C005826 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C007835
ENABLECREATE UNIQUE INDEX SYS_C007835 ON A_COPYDATA (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_COPYDATA 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_COPYDATA
ADD CONSTRAINT FKA_COPYDATA566396 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_COPYDATA_MAPPING with DBMS_METADATA attempting internal generator.
ALTER TABLE A_COPYDATA_MAPPING
ADD CONSTRAINT SYS_C005828 PRIMARY KEY 
(
  A_COPYDATA_MAPPING_ID 
)
USING INDEX SYS_C007833
ENABLECREATE UNIQUE INDEX SYS_C007833 ON A_COPYDATA_MAPPING (A_COPYDATA_MAPPING_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_COPYDATA_MAPPING 
(
  A_COPYDATA_MAPPING_ID NUMBER(10, 0) NOT NULL 
, ACTION_ID NUMBER(10, 0) NOT NULL 
, QUESTION_ID NUMBER(10, 0) 
, CHAPTER_ID NUMBER(10, 0) 
, TABLE_NAME VARCHAR2(30 BYTE) NOT NULL 
, COLUMN_NAME VARCHAR2(30 BYTE) NOT NULL 
, IS_DATE NUMBER(1, 0) NOT NULL 
, GET_NAME NUMBER(1, 0) DEFAULT 0 NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_COPYDATA_MAPPING
ADD CONSTRAINT FKA_COPYDATA718119 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES A_COPYDATA
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_EMAIL with DBMS_METADATA attempting internal generator.
ALTER TABLE A_EMAIL
ADD CONSTRAINT SYS_C005835 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C008061
ENABLECREATE UNIQUE INDEX SYS_C008061 ON A_EMAIL (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_EMAIL 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, SENDER_NAME VARCHAR2(50 BYTE) NOT NULL 
, SENDER_EMAIL VARCHAR2(50 BYTE) NOT NULL 
, QUERY VARCHAR2(4000 BYTE) NOT NULL 
, TITLE VARCHAR2(200 BYTE) NOT NULL 
, TEXT VARCHAR2(2000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_EMAIL
ADD CONSTRAINT FKA_EMAIL698914 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_FORMTRANSITION with DBMS_METADATA attempting internal generator.
ALTER TABLE A_FORMTRANSITION
ADD CONSTRAINT SYS_C005842 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C008021
ENABLECREATE UNIQUE INDEX SYS_C008021 ON A_FORMTRANSITION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_FORMTRANSITION 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, CURRENT_INSTANCE_STATE_ID NUMBER(10, 0) 
, NEXT_INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_FORMTRANSITION
ADD CONSTRAINT FKA_FORMTRAN115223 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
ALTER TABLE A_FORMTRANSITION
ADD CONSTRAINT FKA_FORMTRAN19209 FOREIGN KEY
(
  NEXT_INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE A_FORMTRANSITION
ADD CONSTRAINT FKA_FORMTRAN274020 FOREIGN KEY
(
  CURRENT_INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_LOCATION with DBMS_METADATA attempting internal generator.
ALTER TABLE A_LOCATION
ADD CONSTRAINT SYS_C005845 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C007855
ENABLECREATE UNIQUE INDEX SYS_C007855 ON A_LOCATION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_LOCATION 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_LOCATION
ADD CONSTRAINT FKA_LOCATION3719 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_LOCATION_QC with DBMS_METADATA attempting internal generator.
ALTER TABLE A_LOCATION_QC
ADD CONSTRAINT SYS_C005847 PRIMARY KEY 
(
  A_LOCATION_QC_ID 
)
USING INDEX SYS_C007853
ENABLECREATE UNIQUE INDEX SYS_C007853 ON A_LOCATION_QC (A_LOCATION_QC_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_LOCATION_QC 
(
  A_LOCATION_QC_ID NUMBER(10, 0) NOT NULL 
, ACTION_ID NUMBER(10, 0) NOT NULL 
, QUESTION_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_LOCATION_QC
ADD CONSTRAINT FKA_LOCATION397928 FOREIGN KEY
(
  QUESTION_ID 
, CHAPTER_ID 
)
REFERENCES QUESTION_CHAPTER
(
  QUESTION_ID 
, CHAPTER_ID 
)
ENABLE
ALTER TABLE A_LOCATION_QC
ADD CONSTRAINT FKA_LOCATION561890 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES A_LOCATION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_NOTICE with DBMS_METADATA attempting internal generator.
ALTER TABLE A_NOTICE
ADD CONSTRAINT SYS_C005852 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C007827
ENABLECREATE UNIQUE INDEX SYS_C007827 ON A_NOTICE (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_NOTICE 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, NOTICE_TYPE_ID NUMBER(10, 0) NOT NULL 
, QUERY VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_NOTICE
ADD CONSTRAINT FKA_NOTICE455188 FOREIGN KEY
(
  NOTICE_TYPE_ID 
)
REFERENCES NOTICE_TYPE
(
  NOTICE_TYPE_ID 
)
ENABLE
ALTER TABLE A_NOTICE
ADD CONSTRAINT FKA_NOTICE887484 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_PHP with DBMS_METADATA attempting internal generator.
ALTER TABLE A_PHP
ADD CONSTRAINT SYS_C005856 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C008024
ENABLECREATE UNIQUE INDEX SYS_C008024 ON A_PHP (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_PHP 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, PHP_CLASS VARCHAR2(500 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_PHP
ADD CONSTRAINT FKA_PHP809119 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_PROPOSAL with DBMS_METADATA attempting internal generator.
ALTER TABLE A_PROPOSAL
ADD CONSTRAINT SYS_C005859 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C007872
ENABLECREATE UNIQUE INDEX SYS_C007872 ON A_PROPOSAL (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_PROPOSAL 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_STATE_ID NUMBER(10, 0) NOT NULL 
, DEADLINE_DAYS NUMBER(10, 0) NOT NULL 
, REASON VARCHAR2(50 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_PROPOSAL
ADD CONSTRAINT FKA_PROPOSAL266761 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
ALTER TABLE A_PROPOSAL
ADD CONSTRAINT FKA_PROPOSAL328089 FOREIGN KEY
(
  CIRCULATION_STATE_ID 
)
REFERENCES CIRCULATION_STATE
(
  CIRCULATION_STATE_ID 
)
ENABLE
ALTER TABLE A_PROPOSAL
ADD CONSTRAINT FKA_PROPOSAL921680 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_SAVEPDF with DBMS_METADATA attempting internal generator.
ALTER TABLE A_SAVEPDF
ADD CONSTRAINT SYS_C005864 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C007803
ENABLECREATE UNIQUE INDEX SYS_C007803 ON A_SAVEPDF (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_SAVEPDF 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_GROUP_ID NUMBER(10, 0) 
, SHOW_ALL_PAGE_FORM_MODE NUMBER(1, 0) NOT NULL 
, TEMPLATE VARCHAR2(500 BYTE) NOT NULL 
, PDF_CLASS VARCHAR2(500 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_SAVEPDF
ADD CONSTRAINT FKA_SAVEPDF100324 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
ALTER TABLE A_SAVEPDF
ADD CONSTRAINT FKA_SAVEPDF418328 FOREIGN KEY
(
  PAGE_FORM_GROUP_ID 
)
REFERENCES PAGE_FORM_GROUP
(
  PAGE_FORM_GROUP_ID 
)
ENABLE
ALTER TABLE A_SAVEPDF
ADD CONSTRAINT FKA_SAVEPDF54120 FOREIGN KEY
(
  FORM_ID 
)
REFERENCES FORM
(
  FORM_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.A_VALIDATE with DBMS_METADATA attempting internal generator.
ALTER TABLE A_VALIDATE
ADD CONSTRAINT SYS_C005870 PRIMARY KEY 
(
  ACTION_ID 
)
USING INDEX SYS_C007795
ENABLECREATE UNIQUE INDEX SYS_C007795 ON A_VALIDATE (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE A_VALIDATE 
(
  ACTION_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_GROUP_ID NUMBER(10, 0) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE A_VALIDATE
ADD CONSTRAINT FKA_VALIDATE166755 FOREIGN KEY
(
  PAGE_FORM_GROUP_ID 
)
REFERENCES PAGE_FORM_GROUP
(
  PAGE_FORM_GROUP_ID 
)
ENABLE
ALTER TABLE A_VALIDATE
ADD CONSTRAINT FKA_VALIDATE351897 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.BUTTON with DBMS_METADATA attempting internal generator.
ALTER TABLE BUTTON
ADD CONSTRAINT SYS_C005875 PRIMARY KEY 
(
  BUTTON_ID 
)
USING INDEX SYS_C008188
ENABLECREATE UNIQUE INDEX SYS_C008188 ON BUTTON (BUTTON_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE BUTTON 
(
  BUTTON_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
, CLASS VARCHAR2(25 BYTE) 
, HIDDEN NUMBER(1, 0) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE BUTTON
ADD CONSTRAINT FKBUTTON310902 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.B_GROUP_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE B_GROUP_ACL
ADD CONSTRAINT SYS_C005878 PRIMARY KEY 
(
  BUTTON_ID 
, GROUP_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008121
ENABLECREATE UNIQUE INDEX SYS_C008121 ON B_GROUP_ACL (BUTTON_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE B_GROUP_ACL 
(
  BUTTON_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE B_GROUP_ACL
ADD CONSTRAINT FKB_GROUP_AC339732 FOREIGN KEY
(
  BUTTON_ID 
)
REFERENCES BUTTON
(
  BUTTON_ID 
)
ENABLE
ALTER TABLE B_GROUP_ACL
ADD CONSTRAINT FKB_GROUP_AC449448 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE B_GROUP_ACL
ADD CONSTRAINT FKB_GROUP_AC577162 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.B_ROLE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE B_ROLE_ACL
ADD CONSTRAINT SYS_C005882 PRIMARY KEY 
(
  BUTTON_ID 
, ROLE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008125
ENABLECREATE UNIQUE INDEX SYS_C008125 ON B_ROLE_ACL (BUTTON_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE B_ROLE_ACL 
(
  BUTTON_ID NUMBER(10, 0) NOT NULL 
, ROLE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE B_ROLE_ACL
ADD CONSTRAINT FKB_ROLE_ACL184480 FOREIGN KEY
(
  ROLE_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
ALTER TABLE B_ROLE_ACL
ADD CONSTRAINT FKB_ROLE_ACL23008 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE B_ROLE_ACL
ADD CONSTRAINT FKB_ROLE_ACL86708 FOREIGN KEY
(
  BUTTON_ID 
)
REFERENCES BUTTON
(
  BUTTON_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.B_SERVICE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE B_SERVICE_ACL
ADD CONSTRAINT SYS_C005886 PRIMARY KEY 
(
  BUTTON_ID 
, SERVICE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008113
ENABLECREATE UNIQUE INDEX SYS_C008113 ON B_SERVICE_ACL (BUTTON_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE B_SERVICE_ACL 
(
  BUTTON_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE B_SERVICE_ACL
ADD CONSTRAINT FKB_SERVICE_122104 FOREIGN KEY
(
  BUTTON_ID 
)
REFERENCES BUTTON
(
  BUTTON_ID 
)
ENABLE
ALTER TABLE B_SERVICE_ACL
ADD CONSTRAINT FKB_SERVICE_739770 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE B_SERVICE_ACL
ADD CONSTRAINT FKB_SERVICE_899954 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.B_USER_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE B_USER_ACL
ADD CONSTRAINT SYS_C005890 PRIMARY KEY 
(
  BUTTON_ID 
, USER_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008117
ENABLECREATE UNIQUE INDEX SYS_C008117 ON B_USER_ACL (BUTTON_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE B_USER_ACL 
(
  BUTTON_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE B_USER_ACL
ADD CONSTRAINT FKB_USER_ACL135861 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE B_USER_ACL
ADD CONSTRAINT FKB_USER_ACL324863 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE B_USER_ACL
ADD CONSTRAINT FKB_USER_ACL973854 FOREIGN KEY
(
  BUTTON_ID 
)
REFERENCES BUTTON
(
  BUTTON_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CHAPTER with DBMS_METADATA attempting internal generator.
ALTER TABLE CHAPTER
ADD CONSTRAINT SYS_C005894 PRIMARY KEY 
(
  CHAPTER_ID 
)
USING INDEX SYS_C008301
ENABLECREATE UNIQUE INDEX SYS_C008301 ON CHAPTER (CHAPTER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CHAPTER 
(
  CHAPTER_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(500 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
, JAVASCRIPT VARCHAR2(4000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.CHAPTER_PAGE with DBMS_METADATA attempting internal generator.
ALTER TABLE CHAPTER_PAGE
ADD CONSTRAINT SYS_C005897 PRIMARY KEY 
(
  CHAPTER_ID 
, PAGE_ID 
)
USING INDEX SYS_C008288
ENABLECREATE UNIQUE INDEX SYS_C008288 ON CHAPTER_PAGE (CHAPTER_ID ASC, PAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CHAPTER_PAGE 
(
  CHAPTER_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CHAPTER_PAGE
ADD CONSTRAINT FKCHAPTER_PA38290 FOREIGN KEY
(
  CHAPTER_ID 
)
REFERENCES CHAPTER
(
  CHAPTER_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE
ADD CONSTRAINT FKCHAPTER_PA758670 FOREIGN KEY
(
  PAGE_ID 
)
REFERENCES PAGE
(
  PAGE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CHAPTER_PAGE_GROUP_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE CHAPTER_PAGE_GROUP_ACL
ADD CONSTRAINT SYS_C005901 PRIMARY KEY 
(
  CHAPTER_ID 
, PAGE_ID 
, GROUP_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008167
ENABLECREATE UNIQUE INDEX SYS_C008167 ON CHAPTER_PAGE_GROUP_ACL (CHAPTER_ID ASC, PAGE_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CHAPTER_PAGE_GROUP_ACL 
(
  CHAPTER_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CHAPTER_PAGE_GROUP_ACL
ADD CONSTRAINT FKCHAPTER_PA127184 FOREIGN KEY
(
  CHAPTER_ID 
, PAGE_ID 
)
REFERENCES CHAPTER_PAGE
(
  CHAPTER_ID 
, PAGE_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_GROUP_ACL
ADD CONSTRAINT FKCHAPTER_PA452453 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_GROUP_ACL
ADD CONSTRAINT FKCHAPTER_PA574157 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE CHAPTER_PAGE_ROLE_ACL
ADD CONSTRAINT SYS_C005906 PRIMARY KEY 
(
  CHAPTER_ID 
, PAGE_ID 
, ROLE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008235
ENABLECREATE UNIQUE INDEX SYS_C008235 ON CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID ASC, PAGE_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CHAPTER_PAGE_ROLE_ACL 
(
  CHAPTER_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, ROLE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CHAPTER_PAGE_ROLE_ACL
ADD CONSTRAINT FKCHAPTER_PA741090 FOREIGN KEY
(
  CHAPTER_ID 
, PAGE_ID 
)
REFERENCES CHAPTER_PAGE
(
  CHAPTER_ID 
, PAGE_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_ROLE_ACL
ADD CONSTRAINT FKCHAPTER_PA772167 FOREIGN KEY
(
  ROLE_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_ROLE_ACL
ADD CONSTRAINT FKCHAPTER_PA933639 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE CHAPTER_PAGE_SERVICE_ACL
ADD CONSTRAINT SYS_C005911 PRIMARY KEY 
(
  CHAPTER_ID 
, PAGE_ID 
, SERVICE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008157
ENABLECREATE UNIQUE INDEX SYS_C008157 ON CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID ASC, PAGE_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CHAPTER_PAGE_SERVICE_ACL 
(
  CHAPTER_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CHAPTER_PAGE_SERVICE_ACL
ADD CONSTRAINT FKCHAPTER_PA204217 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_SERVICE_ACL
ADD CONSTRAINT FKCHAPTER_PA435508 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_SERVICE_ACL
ADD CONSTRAINT FKCHAPTER_PA529486 FOREIGN KEY
(
  CHAPTER_ID 
, PAGE_ID 
)
REFERENCES CHAPTER_PAGE
(
  CHAPTER_ID 
, PAGE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CHAPTER_PAGE_USER_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE CHAPTER_PAGE_USER_ACL
ADD CONSTRAINT SYS_C005916 PRIMARY KEY 
(
  CHAPTER_ID 
, PAGE_ID 
, USER_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008162
ENABLECREATE UNIQUE INDEX SYS_C008162 ON CHAPTER_PAGE_USER_ACL (CHAPTER_ID ASC, PAGE_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CHAPTER_PAGE_USER_ACL 
(
  CHAPTER_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CHAPTER_PAGE_USER_ACL
ADD CONSTRAINT FKCHAPTER_PA631784 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_USER_ACL
ADD CONSTRAINT FKCHAPTER_PA820786 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE CHAPTER_PAGE_USER_ACL
ADD CONSTRAINT FKCHAPTER_PA853943 FOREIGN KEY
(
  CHAPTER_ID 
, PAGE_ID 
)
REFERENCES CHAPTER_PAGE
(
  CHAPTER_ID 
, PAGE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION with DBMS_METADATA attempting internal generator.
ALTER TABLE CIRCULATION
ADD CONSTRAINT SYS_C005921 PRIMARY KEY 
(
  CIRCULATION_ID 
)
USING INDEX SYS_C007917
ENABLECREATE UNIQUE INDEX SYS_C007917 ON CIRCULATION (CIRCULATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CIRCULATION 
(
  CIRCULATION_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CIRCULATION
ADD CONSTRAINT FKCIRCULATIO786412 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES IR_EDITCIRCULATION
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE CIRCULATION
ADD CONSTRAINT FKCIRCULATIO875594 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_ANSWER with DBMS_METADATA attempting internal generator.
ALTER TABLE CIRCULATION_ANSWER
ADD CONSTRAINT SYS_C005926 PRIMARY KEY 
(
  CIRCULATION_ANSWER_ID 
)
USING INDEX SYS_C008221
ENABLECREATE UNIQUE INDEX SYS_C008221 ON CIRCULATION_ANSWER (CIRCULATION_ANSWER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CIRCULATION_ANSWER 
(
  CIRCULATION_ANSWER_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_ANSWER_TYPE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CIRCULATION_ANSWER
ADD CONSTRAINT FKCIRCULATIO36857 FOREIGN KEY
(
  CIRCULATION_ANSWER_TYPE_ID 
)
REFERENCES CIRCULATION_ANSWER_TYPE
(
  CIRCULATION_ANSWER_TYPE_ID 
)
ENABLE
ALTER TABLE CIRCULATION_ANSWER
ADD CONSTRAINT FKCIRCULATIO49857 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_ANSWER_TYPE with DBMS_METADATA attempting internal generator.
ALTER TABLE CIRCULATION_ANSWER_TYPE
ADD CONSTRAINT SYS_C005932 PRIMARY KEY 
(
  CIRCULATION_ANSWER_TYPE_ID 
)
USING INDEX SYS_C008215
ENABLECREATE UNIQUE INDEX SYS_C008215 ON CIRCULATION_ANSWER_TYPE (CIRCULATION_ANSWER_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CIRCULATION_ANSWER_TYPE 
(
  CIRCULATION_ANSWER_TYPE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_LOG with DBMS_METADATA attempting internal generator.
ALTER TABLE CIRCULATION_LOG
ADD CONSTRAINT SYS_C005935 PRIMARY KEY 
(
  CIRCULATION_LOG_ID 
)
USING INDEX SYS_C007894
ENABLECREATE UNIQUE INDEX SYS_C007894 ON CIRCULATION_LOG (CIRCULATION_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CIRCULATION_LOG 
(
  CIRCULATION_LOG_ID NUMBER(10, 0) NOT NULL 
, ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTION VARCHAR2(500 BYTE) NOT NULL 
, DATA CLOB 
, MODIFICATION_DATE DATE NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (DATA) STORE AS SYS_LOB0000017583C00005$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_REASON with DBMS_METADATA attempting internal generator.
ALTER TABLE CIRCULATION_REASON
ADD CONSTRAINT SYS_C005941 PRIMARY KEY 
(
  CIRCULATION_REASON_ID 
)
USING INDEX SYS_C008212
ENABLECREATE UNIQUE INDEX SYS_C008212 ON CIRCULATION_REASON (CIRCULATION_REASON_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CIRCULATION_REASON 
(
  CIRCULATION_REASON_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE CIRCULATION_REASON
ADD CONSTRAINT FKCIRCULATIO205277 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_STATE with DBMS_METADATA attempting internal generator.
ALTER TABLE CIRCULATION_STATE
ADD CONSTRAINT SYS_C005946 PRIMARY KEY 
(
  CIRCULATION_STATE_ID 
)
USING INDEX SYS_C008225
ENABLECREATE UNIQUE INDEX SYS_C008225 ON CIRCULATION_STATE (CIRCULATION_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CIRCULATION_STATE 
(
  CIRCULATION_STATE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(100 BYTE) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_TYPE with DBMS_METADATA attempting internal generator.
ALTER TABLE CIRCULATION_TYPE
ADD CONSTRAINT SYS_C005950 PRIMARY KEY 
(
  CIRCULATION_TYPE_ID 
)
USING INDEX SYS_C007992
ENABLECREATE UNIQUE INDEX SYS_C007992 ON CIRCULATION_TYPE (CIRCULATION_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE CIRCULATION_TYPE 
(
  CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.FORM with DBMS_METADATA attempting internal generator.
ALTER TABLE FORM
ADD CONSTRAINT SYS_C005953 PRIMARY KEY 
(
  FORM_ID 
)
USING INDEX SYS_C008308
ENABLECREATE UNIQUE INDEX SYS_C008308 ON FORM (FORM_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE FORM 
(
  FORM_ID NUMBER(10, 0) NOT NULL 
, FORM_STATE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(500 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE FORM
ADD CONSTRAINT FKFORM331615 FOREIGN KEY
(
  FORM_STATE_ID 
)
REFERENCES FORM_STATE
(
  FORM_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.FORM_STATE with DBMS_METADATA attempting internal generator.
ALTER TABLE FORM_STATE
ADD CONSTRAINT SYS_C005957 PRIMARY KEY 
(
  FORM_STATE_ID 
)
USING INDEX SYS_C008269
ENABLECREATE UNIQUE INDEX SYS_C008269 ON FORM_STATE (FORM_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE FORM_STATE 
(
  FORM_STATE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.GLOSSARY_CATEGORY with DBMS_METADATA attempting internal generator.
ALTER TABLE GLOSSARY_CATEGORY
ADD CONSTRAINT GLOSSARY_CATEGORY_PK PRIMARY KEY 
(
  GLOSSARY_CATEGORY_ID 
)
USING INDEX GLOSSARY_CATEGORY_PK
ENABLECREATE UNIQUE INDEX GLOSSARY_CATEGORY_PK ON GLOSSARY_CATEGORY (GLOSSARY_CATEGORY_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE GLOSSARY_CATEGORY 
(
  GLOSSARY_CATEGORY_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(80 BYTE) NOT NULL 
, ROLE_ID NUMBER 
, SERVICE_ID NUMBER 
, USER_ID NUMBER 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.GLOSSARY_SENTENCE with DBMS_METADATA attempting internal generator.
ALTER TABLE GLOSSARY_SENTENCE
ADD CONSTRAINT GLOSSARY_SENTENCE_PK PRIMARY KEY 
(
  GLOSSARY_SENTENCE_ID 
)
USING INDEX GLOSSARY_SENTENCE_PK
ENABLECREATE UNIQUE INDEX GLOSSARY_SENTENCE_PK ON GLOSSARY_SENTENCE (GLOSSARY_SENTENCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE GLOSSARY_SENTENCE 
(
  GLOSSARY_SENTENCE_ID NUMBER NOT NULL 
, GLOSSARY_CATEGORY_ID NUMBER NOT NULL 
, TITLE VARCHAR2(500 BYTE) NOT NULL 
, SENTENCE VARCHAR2(4000 BYTE) NOT NULL 
, ROLE_ID NUMBER 
, SERVICE_ID NUMBER 
, USER_ID NUMBER 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.GROUP with DBMS_METADATA attempting internal generator.
ALTER TABLE "GROUP"
ADD CONSTRAINT SYS_C005968 PRIMARY KEY 
(
  GROUP_ID 
)
USING INDEX SYS_C008336
ENABLECREATE UNIQUE INDEX SYS_C008336 ON "GROUP" (GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE "GROUP" 
(
  GROUP_ID NUMBER(10, 0) NOT NULL 
, ROLE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) 
, NAME VARCHAR2(100 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE "GROUP"
ADD CONSTRAINT FKGROUP559557 FOREIGN KEY
(
  ROLE_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
ALTER TABLE "GROUP"
ADD CONSTRAINT FKGROUP947104 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.GROUP_LOCATION with DBMS_METADATA attempting internal generator.
ALTER TABLE GROUP_LOCATION
ADD CONSTRAINT SYS_C005972 PRIMARY KEY 
(
  GROUP_ID 
, LOCATION_ID 
)
USING INDEX SYS_C008318
ENABLECREATE UNIQUE INDEX SYS_C008318 ON GROUP_LOCATION (GROUP_ID ASC, LOCATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE GROUP_LOCATION 
(
  GROUP_ID NUMBER(10, 0) NOT NULL 
, LOCATION_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE GROUP_LOCATION
ADD CONSTRAINT FKGROUP_LOCA209875 FOREIGN KEY
(
  LOCATION_ID 
)
REFERENCES LOCATION
(
  LOCATION_ID 
)
ENABLE
ALTER TABLE GROUP_LOCATION
ADD CONSTRAINT FKGROUP_LOCA564744 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE
ADD CONSTRAINT SYS_C005975 PRIMARY KEY 
(
  INSTANCE_ID 
)
USING INDEX SYS_C008041
ENABLECREATE UNIQUE INDEX SYS_C008041 ON INSTANCE (INSTANCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE 
(
  INSTANCE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
, CREATION_DATE DATE NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE INSTANCE
ADD CONSTRAINT FKINSTANCE54930 FOREIGN KEY
(
  FORM_ID 
)
REFERENCES FORM
(
  FORM_ID 
)
ENABLE
ALTER TABLE INSTANCE
ADD CONSTRAINT FKINSTANCE83085 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
ALTER TABLE INSTANCE
ADD CONSTRAINT FKINSTANCE839062 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE INSTANCE
ADD CONSTRAINT FKINSTANCE943525 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_DEMO with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_DEMO
ADD CONSTRAINT SYS_C005983 PRIMARY KEY 
(
  INSTANCE_DEMO_ID 
)
USING INDEX SYS_C008558
ENABLECREATE UNIQUE INDEX SYS_C008558 ON INSTANCE_DEMO (INSTANCE_DEMO_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_DEMO 
(
  INSTANCE_DEMO_ID NUMBER(10, 0) NOT NULL 
, VALUE VARCHAR2(1000 BYTE) 
, AUTOMATIC_DATE DATE 
, FORM_DATE DATE 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE INSTANCE_DEMO
ADD CONSTRAINT FKINSTANCE_DEMO1 FOREIGN KEY
(
  INSTANCE_DEMO_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_DEMO_LOG with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_DEMO_LOG
ADD CONSTRAINT SYS_C005985 PRIMARY KEY 
(
  INSTANCE_DEMO_LOG_ID 
)
USING INDEX SYS_C008566
ENABLECREATE UNIQUE INDEX SYS_C008566 ON INSTANCE_DEMO_LOG (INSTANCE_DEMO_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_DEMO_LOG 
(
  INSTANCE_DEMO_LOG_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTION VARCHAR2(500 BYTE) NOT NULL 
, DATA CLOB NOT NULL 
, ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (DATA) STORE AS SYS_LOB0000017597C00005$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_FORM_PDF with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_FORM_PDF
ADD CONSTRAINT SYS_C005992 PRIMARY KEY 
(
  INSTANCE_FORM_PDF_ID 
)
USING INDEX SYS_C007814
ENABLECREATE UNIQUE INDEX SYS_C007814 ON INSTANCE_FORM_PDF (INSTANCE_FORM_PDF_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_FORM_PDF 
(
  INSTANCE_FORM_PDF_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_ID NUMBER(10, 0) NOT NULL 
, ACTION_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, FILENAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE INSTANCE_FORM_PDF
ADD CONSTRAINT FKINSTANCE_F392374 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE INSTANCE_FORM_PDF
ADD CONSTRAINT FKINSTANCE_F731427 FOREIGN KEY
(
  ACTION_ID 
)
REFERENCES ACTION
(
  ACTION_ID 
)
ENABLE
ALTER TABLE INSTANCE_FORM_PDF
ADD CONSTRAINT FKINSTANCE_F765139 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_GUEST with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_GUEST
ADD CONSTRAINT SYS_C006000 PRIMARY KEY 
(
  INSTANCE_ID 
)
USING INDEX SYS_C007823
ENABLECREATE UNIQUE INDEX SYS_C007823 ON INSTANCE_GUEST (INSTANCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_GUEST 
(
  INSTANCE_ID NUMBER(10, 0) NOT NULL 
, SESSION_ID VARCHAR2(50 BYTE) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE INSTANCE_GUEST
ADD CONSTRAINT FKINSTANCE_G338221 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_LOCATION with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_LOCATION
ADD CONSTRAINT SYS_C006004 PRIMARY KEY 
(
  LOCATION_ID 
, INSTANCE_ID 
)
USING INDEX SYS_C007858
ENABLECREATE UNIQUE INDEX SYS_C007858 ON INSTANCE_LOCATION (LOCATION_ID ASC, INSTANCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_LOCATION 
(
  LOCATION_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE INSTANCE_LOCATION
ADD CONSTRAINT FKINSTANCE_L131203 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
ALTER TABLE INSTANCE_LOCATION
ADD CONSTRAINT FKINSTANCE_L448980 FOREIGN KEY
(
  LOCATION_ID 
)
REFERENCES LOCATION
(
  LOCATION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_LOCATION_LOG with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_LOCATION_LOG
ADD CONSTRAINT SYS_C006007 PRIMARY KEY 
(
  INSTANCE_LOCATION_LOG_ID 
)
USING INDEX SYS_C007848
ENABLECREATE UNIQUE INDEX SYS_C007848 ON INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_LOCATION_LOG 
(
  INSTANCE_LOCATION_LOG_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTION VARCHAR2(500 BYTE) NOT NULL 
, DATA CLOB 
, ID1 NUMBER(10, 0) NOT NULL 
, FIELD1 VARCHAR2(30 BYTE) NOT NULL 
, ID2 NUMBER(10, 0) NOT NULL 
, FIELD2 VARCHAR2(30 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (DATA) STORE AS SYS_LOB0000017603C00005$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_LOG with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_LOG
ADD CONSTRAINT SYS_C006016 PRIMARY KEY 
(
  INSTANCE_LOG_ID 
)
USING INDEX SYS_C007962
ENABLECREATE UNIQUE INDEX SYS_C007962 ON INSTANCE_LOG (INSTANCE_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_LOG 
(
  INSTANCE_LOG_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTION VARCHAR2(500 BYTE) NOT NULL 
, DATA CLOB 
, ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (DATA) STORE AS SYS_LOB0000017606C00005$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_RESOURCE with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_RESOURCE
ADD CONSTRAINT SYS_C006022 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C008105
ENABLECREATE UNIQUE INDEX SYS_C008105 ON INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_RESOURCE 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, AVAILABLE_INSTANCE_RESOURCE_ID VARCHAR2(25 BYTE) NOT NULL 
, RESOURCE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
, TEMPLATE VARCHAR2(500 BYTE) 
, CLASS VARCHAR2(25 BYTE) 
, HIDDEN NUMBER(1, 0) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE INSTANCE_RESOURCE
ADD CONSTRAINT FKINSTANCE_R309345 FOREIGN KEY
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
)
REFERENCES AVAILABLE_INSTANCE_RESOURCE
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE INSTANCE_RESOURCE
ADD CONSTRAINT FKINSTANCE_R636267 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
ALTER TABLE INSTANCE_RESOURCE
ADD CONSTRAINT FKINSTANCE_R720544 FOREIGN KEY
(
  FORM_ID 
)
REFERENCES FORM
(
  FORM_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_RESOURCE_ACTION with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_RESOURCE_ACTION
ADD CONSTRAINT SYS_C006030 PRIMARY KEY 
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
, AVAILABLE_ACTION_ID 
)
USING INDEX SYS_C008047
ENABLECREATE UNIQUE INDEX SYS_C008047 ON INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID ASC, AVAILABLE_ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_RESOURCE_ACTION 
(
  AVAILABLE_INSTANCE_RESOURCE_ID VARCHAR2(25 BYTE) NOT NULL 
, AVAILABLE_ACTION_ID VARCHAR2(25 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE INSTANCE_RESOURCE_ACTION
ADD CONSTRAINT FKINSTANCE_R184021 FOREIGN KEY
(
  AVAILABLE_ACTION_ID 
)
REFERENCES AVAILABLE_ACTION
(
  AVAILABLE_ACTION_ID 
)
ENABLE
ALTER TABLE INSTANCE_RESOURCE_ACTION
ADD CONSTRAINT FKINSTANCE_R236464 FOREIGN KEY
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
)
REFERENCES AVAILABLE_INSTANCE_RESOURCE
(
  AVAILABLE_INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_STATE with DBMS_METADATA attempting internal generator.
ALTER TABLE INSTANCE_STATE
ADD CONSTRAINT SYS_C006033 PRIMARY KEY 
(
  INSTANCE_STATE_ID 
)
USING INDEX SYS_C008244
ENABLECREATE UNIQUE INDEX SYS_C008244 ON INSTANCE_STATE (INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE INSTANCE_STATE 
(
  INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(100 BYTE) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_ALLFORMPAGES with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_ALLFORMPAGES
ADD CONSTRAINT SYS_C006037 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007924
ENABLECREATE UNIQUE INDEX SYS_C007924 ON IR_ALLFORMPAGES (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_ALLFORMPAGES 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_GROUP_ID NUMBER(10, 0) 
, PDF_CLASS VARCHAR2(500 BYTE) 
, SHOW_ALL_PAGE_FORM_MODE NUMBER(1, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_ALLFORMPAGES
ADD CONSTRAINT FKIR_ALLFORM254849 FOREIGN KEY
(
  PAGE_FORM_GROUP_ID 
)
REFERENCES PAGE_FORM_GROUP
(
  PAGE_FORM_GROUP_ID 
)
ENABLE
ALTER TABLE IR_ALLFORMPAGES
ADD CONSTRAINT FKIR_ALLFORM645459 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_CIRCULATION with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_CIRCULATION
ADD CONSTRAINT SYS_C006040 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007978
ENABLECREATE UNIQUE INDEX SYS_C007978 ON IR_CIRCULATION (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_CIRCULATION 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) 
, DRAFT_CIRCULATION_ANSWER_ID NUMBER(10, 0) 
, SHOW_NOTICE NUMBER(1, 0) NOT NULL 
, SHOW_HISTORY NUMBER(1, 0) NOT NULL 
, SHOW_ALL_CHILDREN NUMBER(1, 0) NOT NULL 
, READ_NOTICE_TEMPLATE VARCHAR2(500 BYTE) 
, PDF_CLASS VARCHAR2(500 BYTE) 
, SERVICE_TO_BE_INTERPRETED VARCHAR2(50 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_CIRCULATION
ADD CONSTRAINT FKIR_CIRCULA675506 FOREIGN KEY
(
  DRAFT_CIRCULATION_ANSWER_ID 
)
REFERENCES CIRCULATION_ANSWER
(
  CIRCULATION_ANSWER_ID 
)
ENABLE
ALTER TABLE IR_CIRCULATION
ADD CONSTRAINT FKIR_CIRCULA717703 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_CIRCULATION
ADD CONSTRAINT FKIR_CIRCULA74747 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
ALTER TABLE IR_CIRCULATION
ADD CONSTRAINT FKIR_CIRCULA873267 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_EDITCIRCULATION with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_EDITCIRCULATION
ADD CONSTRAINT SYS_C006046 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007997
ENABLECREATE UNIQUE INDEX SYS_C007997 ON IR_EDITCIRCULATION (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_EDITCIRCULATION 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, DRAFT_CIRCULATION_ANSWER_ID NUMBER(10, 0) 
, SHOW_NOTICE NUMBER(1, 0) NOT NULL 
, ADD_TEMPLATE VARCHAR2(500 BYTE) 
, ADD_ACTIVATION_TEMPLATE VARCHAR2(500 BYTE) 
, READ_NOTICE_TEMPLATE VARCHAR2(500 BYTE) 
, PDF_CLASS VARCHAR2(500 BYTE) 
, DEFAULT_CIRCULATION_NAME VARCHAR2(500 BYTE) 
, SINGLE_CIRCULATION NUMBER(1, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_EDITCIRCULATION
ADD CONSTRAINT FKIR_EDITCIR372215 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
ALTER TABLE IR_EDITCIRCULATION
ADD CONSTRAINT FKIR_EDITCIR579764 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_EDITCIRCULATION
ADD CONSTRAINT FKIR_EDITCIR621961 FOREIGN KEY
(
  DRAFT_CIRCULATION_ANSWER_ID 
)
REFERENCES CIRCULATION_ANSWER
(
  CIRCULATION_ANSWER_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_EDITCIRCULATION_SG with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_EDITCIRCULATION_SG
ADD CONSTRAINT SYS_C006051 PRIMARY KEY 
(
  IR_EDITCIRCULATION_SG_ID 
)
USING INDEX SYS_C007989
ENABLECREATE UNIQUE INDEX SYS_C007989 ON IR_EDITCIRCULATION_SG (IR_EDITCIRCULATION_SG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_EDITCIRCULATION_SG 
(
  IR_EDITCIRCULATION_SG_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_GROUP_ID NUMBER(10, 0) NOT NULL 
, LOCALIZED NUMBER(1, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_EDITCIRCULATION_SG
ADD CONSTRAINT FKIR_EDITCIR259074 FOREIGN KEY
(
  SERVICE_GROUP_ID 
)
REFERENCES SERVICE_GROUP
(
  SERVICE_GROUP_ID 
)
ENABLE
ALTER TABLE IR_EDITCIRCULATION_SG
ADD CONSTRAINT FKIR_EDITCIR476386 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES IR_EDITCIRCULATION
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_EDITFORMPAGE with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_EDITFORMPAGE
ADD CONSTRAINT SYS_C006056 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C008191
ENABLECREATE UNIQUE INDEX SYS_C008191 ON IR_EDITFORMPAGE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_EDITFORMPAGE 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, PDF_CLASS VARCHAR2(500 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_EDITFORMPAGE
ADD CONSTRAINT FKIR_EDITFOR420962 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_EDITFORMPAGE
ADD CONSTRAINT FKIR_EDITFOR744183 FOREIGN KEY
(
  PAGE_ID 
)
REFERENCES PAGE
(
  PAGE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_EDITFORMPAGES with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_EDITFORMPAGES
ADD CONSTRAINT SYS_C006059 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C008078
ENABLECREATE UNIQUE INDEX SYS_C008078 ON IR_EDITFORMPAGES (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_EDITFORMPAGES 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_GROUP_ID NUMBER(10, 0) 
, PDF_CLASS VARCHAR2(500 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_EDITFORMPAGES
ADD CONSTRAINT FKIR_EDITFOR305004 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_EDITFORMPAGES
ADD CONSTRAINT FKIR_EDITFOR766277 FOREIGN KEY
(
  PAGE_FORM_GROUP_ID 
)
REFERENCES PAGE_FORM_GROUP
(
  PAGE_FORM_GROUP_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_EDITLETTER with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_EDITLETTER
ADD CONSTRAINT SYS_C006061 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007984
ENABLECREATE UNIQUE INDEX SYS_C007984 ON IR_EDITLETTER (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_EDITLETTER 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PDF_CLASS VARCHAR2(500 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_EDITLETTER
ADD CONSTRAINT FKIR_EDITLET55435 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_EDITLETTER_ANSWER with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_EDITLETTER_ANSWER
ADD CONSTRAINT SYS_C006063 PRIMARY KEY 
(
  IR_EDITLETTER_ANSWER_ID 
)
USING INDEX SYS_C007982
ENABLECREATE UNIQUE INDEX SYS_C007982 ON IR_EDITLETTER_ANSWER (IR_EDITLETTER_ANSWER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_EDITLETTER_ANSWER 
(
  IR_EDITLETTER_ANSWER_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_EDITLETTER_ANSWER
ADD CONSTRAINT FKIR_EDITLET118223 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES IR_EDITLETTER
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_EDITNOTICE with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_EDITNOTICE
ADD CONSTRAINT SYS_C006067 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007908
ENABLECREATE UNIQUE INDEX SYS_C007908 ON IR_EDITNOTICE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_EDITNOTICE 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, EDITABLE_AFTER_DEADLINE NUMBER(1, 0) NOT NULL 
, PDF_CLASS VARCHAR2(500 BYTE) 
, EDIT_NOTICE_TEMPLATE VARCHAR2(500 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_EDITNOTICE
ADD CONSTRAINT FKIR_EDITNOT433223 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_EDITNOTICE
ADD CONSTRAINT FKIR_EDITNOT745916 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_FORMERROR with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_FORMERROR
ADD CONSTRAINT SYS_C006071 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007806
ENABLECREATE UNIQUE INDEX SYS_C007806 ON IR_FORMERROR (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_FORMERROR 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, IR_EDITFORMPAGES_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_FORMERROR
ADD CONSTRAINT FKIR_FORMERR383206 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_FORMERROR
ADD CONSTRAINT FKIR_FORMERR636967 FOREIGN KEY
(
  IR_EDITFORMPAGES_ID 
)
REFERENCES IR_EDITFORMPAGES
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_FORMPAGE with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_FORMPAGE
ADD CONSTRAINT SYS_C006074 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C008074
ENABLECREATE UNIQUE INDEX SYS_C008074 ON IR_FORMPAGE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_FORMPAGE 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, PDF_CLASS VARCHAR2(500 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_FORMPAGE
ADD CONSTRAINT FKIR_FORMPAG638405 FOREIGN KEY
(
  PAGE_ID 
)
REFERENCES PAGE
(
  PAGE_ID 
)
ENABLE
ALTER TABLE IR_FORMPAGE
ADD CONSTRAINT FKIR_FORMPAG684815 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_FORMPAGES with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_FORMPAGES
ADD CONSTRAINT SYS_C006077 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C008076
ENABLECREATE UNIQUE INDEX SYS_C008076 ON IR_FORMPAGES (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_FORMPAGES 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_GROUP_ID NUMBER(10, 0) 
, PDF_CLASS VARCHAR2(500 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_FORMPAGES
ADD CONSTRAINT FKIR_FORMPAG329489 FOREIGN KEY
(
  PAGE_FORM_GROUP_ID 
)
REFERENCES PAGE_FORM_GROUP
(
  PAGE_FORM_GROUP_ID 
)
ENABLE
ALTER TABLE IR_FORMPAGES
ADD CONSTRAINT FKIR_FORMPAG741792 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_FORMWIZARD with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_FORMWIZARD
ADD CONSTRAINT SYS_C006079 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007819
ENABLECREATE UNIQUE INDEX SYS_C007819 ON IR_FORMWIZARD (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_FORMWIZARD 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_GROUP_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
, SHOW_CAPTCHA NUMBER(1, 0) NOT NULL 
, SUMMARY VARCHAR2(4000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_FORMWIZARD
ADD CONSTRAINT FKIR_FORMWIZ18601 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_FORMWIZARD
ADD CONSTRAINT FKIR_FORMWIZ506030 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE IR_FORMWIZARD
ADD CONSTRAINT FKIR_FORMWIZ881707 FOREIGN KEY
(
  PAGE_FORM_GROUP_ID 
)
REFERENCES PAGE_FORM_GROUP
(
  PAGE_FORM_GROUP_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_GROUP_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_GROUP_ACL
ADD CONSTRAINT SYS_C006084 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
, GROUP_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008093
ENABLECREATE UNIQUE INDEX SYS_C008093 ON IR_GROUP_ACL (INSTANCE_RESOURCE_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_GROUP_ACL 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_GROUP_ACL
ADD CONSTRAINT FKIR_GROUP_A354202 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_GROUP_ACL
ADD CONSTRAINT FKIR_GROUP_A78207 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
ALTER TABLE IR_GROUP_ACL
ADD CONSTRAINT FKIR_GROUP_A866772 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_LETTER with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_LETTER
ADD CONSTRAINT SYS_C006088 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007934
ENABLECREATE UNIQUE INDEX SYS_C007934 ON IR_LETTER (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_LETTER 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, IR_EDITLETTER_ID NUMBER(10, 0) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_LETTER
ADD CONSTRAINT FKIR_LETTER303905 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_NEWFORM with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_NEWFORM
ADD CONSTRAINT SYS_C006090 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C008044
ENABLECREATE UNIQUE INDEX SYS_C008044 ON IR_NEWFORM (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_NEWFORM 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_NEWFORM
ADD CONSTRAINT FKIR_NEWFORM183428 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE IR_NEWFORM
ADD CONSTRAINT FKIR_NEWFORM695998 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_PAGE with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_PAGE
ADD CONSTRAINT SYS_C006093 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007797
ENABLECREATE UNIQUE INDEX SYS_C007797 ON IR_PAGE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_PAGE 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, PDF_CLASS VARCHAR2(500 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_PAGE
ADD CONSTRAINT FKIR_PAGE236639 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_ROLE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_ROLE_ACL
ADD CONSTRAINT SYS_C006095 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
, ROLE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008097
ENABLECREATE UNIQUE INDEX SYS_C008097 ON IR_ROLE_ACL (INSTANCE_RESOURCE_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_ROLE_ACL 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, ROLE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_ROLE_ACL
ADD CONSTRAINT FKIR_ROLE_AC144710 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_ROLE_ACL
ADD CONSTRAINT FKIR_ROLE_AC495808 FOREIGN KEY
(
  ROLE_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
ALTER TABLE IR_ROLE_ACL
ADD CONSTRAINT FKIR_ROLE_AC657280 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_SERVICE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_SERVICE_ACL
ADD CONSTRAINT SYS_C006099 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
, SERVICE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008085
ENABLECREATE UNIQUE INDEX SYS_C008085 ON IR_SERVICE_ACL (INSTANCE_RESOURCE_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_SERVICE_ACL 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_SERVICE_ACL
ADD CONSTRAINT FKIR_SERVICE293198 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE IR_SERVICE_ACL
ADD CONSTRAINT FKIR_SERVICE625063 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
ALTER TABLE IR_SERVICE_ACL
ADD CONSTRAINT FKIR_SERVICE780627 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_USER_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE IR_USER_ACL
ADD CONSTRAINT SYS_C006103 PRIMARY KEY 
(
  INSTANCE_RESOURCE_ID 
, USER_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008089
ENABLECREATE UNIQUE INDEX SYS_C008089 ON IR_USER_ACL (INSTANCE_RESOURCE_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE IR_USER_ACL 
(
  INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE IR_USER_ACL
ADD CONSTRAINT FKIR_USER_AC31857 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE IR_USER_ACL
ADD CONSTRAINT FKIR_USER_AC544427 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE IR_USER_ACL
ADD CONSTRAINT FKIR_USER_AC644574 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.LETTER with DBMS_METADATA attempting internal generator.
ALTER TABLE LETTER
ADD CONSTRAINT SYS_C006107 PRIMARY KEY 
(
  INSTANCE_ID 
, INSTANCE_RESOURCE_ID 
)
USING INDEX SYS_C007970
ENABLECREATE UNIQUE INDEX SYS_C007970 ON LETTER (INSTANCE_ID ASC, INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE LETTER 
(
  INSTANCE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, IR_EDITLETTER_ANSWER_ID NUMBER(10, 0) 
, "DATE" DATE NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, CONTENT CLOB NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (CONTENT) STORE AS SYS_LOB0000017632C00007$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)ALTER TABLE LETTER
ADD CONSTRAINT FKLETTER229264 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES IR_EDITLETTER
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE LETTER
ADD CONSTRAINT FKLETTER417067 FOREIGN KEY
(
  IR_EDITLETTER_ANSWER_ID 
)
REFERENCES IR_EDITLETTER_ANSWER
(
  IR_EDITLETTER_ANSWER_ID 
)
ENABLE
ALTER TABLE LETTER
ADD CONSTRAINT FKLETTER469117 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE LETTER
ADD CONSTRAINT FKLETTER96352 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.LETTER_IMAGE with DBMS_METADATA attempting internal generator.
ALTER TABLE LETTER_IMAGE
ADD CONSTRAINT SYS_C006115 PRIMARY KEY 
(
  LETTER_IMAGE_ID 
)
USING INDEX SYS_C007932
ENABLECREATE UNIQUE INDEX SYS_C007932 ON LETTER_IMAGE (LETTER_IMAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE LETTER_IMAGE 
(
  LETTER_IMAGE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, FILENAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE LETTER_IMAGE
ADD CONSTRAINT FKLETTER_IMA187846 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
ALTER TABLE LETTER_IMAGE
ADD CONSTRAINT FKLETTER_IMA815080 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE LETTER_IMAGE
ADD CONSTRAINT FKLETTER_IMA861350 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES INSTANCE_RESOURCE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.LOCATION with DBMS_METADATA attempting internal generator.
ALTER TABLE LOCATION
ADD CONSTRAINT SYS_C006123 PRIMARY KEY 
(
  LOCATION_ID 
)
USING INDEX SYS_C008320
ENABLECREATE UNIQUE INDEX SYS_C008320 ON LOCATION (LOCATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE LOCATION 
(
  LOCATION_ID NUMBER(10, 0) NOT NULL 
, COMMUNAL_CANTONAL_NUMBER NUMBER(10, 0) 
, COMMUNAL_FEDERAL_NUMBER VARCHAR2(255 BYTE) 
, DISTRICT_NUMBER NUMBER(10, 0) 
, SECTION_NUMBER NUMBER(10, 0) 
, NAME VARCHAR2(100 BYTE) 
, COMMUNE_NAME VARCHAR2(100 BYTE) 
, DISTRICT_NAME VARCHAR2(100 BYTE) 
, SECTION_NAME VARCHAR2(100 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.MAPPING with DBMS_METADATA attempting internal generator.
ALTER TABLE MAPPING
ADD CONSTRAINT SYS_C006125 PRIMARY KEY 
(
  MAPPING_ID 
)
USING INDEX SYS_C008263
ENABLECREATE UNIQUE INDEX SYS_C008263 ON MAPPING (MAPPING_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE MAPPING 
(
  MAPPING_ID NUMBER(10, 0) NOT NULL 
, TABLE_NAME VARCHAR2(30 BYTE) NOT NULL 
, COLUMN_NAME VARCHAR2(30 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.NOTICE with DBMS_METADATA attempting internal generator.
ALTER TABLE NOTICE
ADD CONSTRAINT SYS_C006129 PRIMARY KEY 
(
  NOTICE_TYPE_ID 
, ACTIVATION_ID 
)
USING INDEX SYS_C007912
ENABLECREATE UNIQUE INDEX SYS_C007912 ON NOTICE (NOTICE_TYPE_ID ASC, ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE NOTICE 
(
  NOTICE_TYPE_ID NUMBER(10, 0) NOT NULL 
, ACTIVATION_ID NUMBER(10, 0) NOT NULL 
, CONTENT CLOB 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (CONTENT) STORE AS SYS_LOB0000017638C00003$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)ALTER TABLE NOTICE
ADD CONSTRAINT FKNOTICE481069 FOREIGN KEY
(
  NOTICE_TYPE_ID 
)
REFERENCES NOTICE_TYPE
(
  NOTICE_TYPE_ID 
)
ENABLE
ALTER TABLE NOTICE
ADD CONSTRAINT FKNOTICE87000 FOREIGN KEY
(
  ACTIVATION_ID 
)
REFERENCES ACTIVATION
(
  ACTIVATION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.NOTICE_IMAGE with DBMS_METADATA attempting internal generator.
ALTER TABLE NOTICE_IMAGE
ADD CONSTRAINT SYS_C006132 PRIMARY KEY 
(
  NOTICE_IMAGE_ID 
)
USING INDEX SYS_C007867
ENABLECREATE UNIQUE INDEX SYS_C007867 ON NOTICE_IMAGE (NOTICE_IMAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE NOTICE_IMAGE 
(
  NOTICE_IMAGE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_RESOURCE_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTIVATION_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, FILENAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE NOTICE_IMAGE
ADD CONSTRAINT FKNOTICE_IMA199419 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE NOTICE_IMAGE
ADD CONSTRAINT FKNOTICE_IMA572184 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
ALTER TABLE NOTICE_IMAGE
ADD CONSTRAINT FKNOTICE_IMA590857 FOREIGN KEY
(
  INSTANCE_RESOURCE_ID 
)
REFERENCES IR_EDITNOTICE
(
  INSTANCE_RESOURCE_ID 
)
ENABLE
ALTER TABLE NOTICE_IMAGE
ADD CONSTRAINT FKNOTICE_IMA698986 FOREIGN KEY
(
  ACTIVATION_ID 
)
REFERENCES ACTIVATION
(
  ACTIVATION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.NOTICE_LOG with DBMS_METADATA attempting internal generator.
ALTER TABLE NOTICE_LOG
ADD CONSTRAINT SYS_C006141 PRIMARY KEY 
(
  NOTICE_LOG_ID 
)
USING INDEX SYS_C007904
ENABLECREATE UNIQUE INDEX SYS_C007904 ON NOTICE_LOG (NOTICE_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE NOTICE_LOG 
(
  NOTICE_LOG_ID NUMBER(10, 0) NOT NULL 
, MODIFICATION_DATE DATE NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, ACTION VARCHAR2(500 BYTE) NOT NULL 
, DATA CLOB 
, ID1 NUMBER(10, 0) NOT NULL 
, FIELD1 VARCHAR2(30 BYTE) NOT NULL 
, ID2 NUMBER(10, 0) NOT NULL 
, FIELD2 VARCHAR2(30 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS 
LOB (DATA) STORE AS SYS_LOB0000017642C00005$$ 
( 
  ENABLE STORAGE IN ROW 
  CHUNK 8192 
  RETENTION 
  NOCACHE 
  LOGGING 
  TABLESPACE SYSTEM 
  STORAGE 
  ( 
    INITIAL 65536 
    NEXT 1048576 
    MINEXTENTS 1 
    MAXEXTENTS UNLIMITED 
    FREELISTS 1 
    FREELIST GROUPS 1 
    BUFFER_POOL DEFAULT 
  )  
)
-- Unable to render TABLE DDL for object CAMAC_DEV.NOTICE_TYPE with DBMS_METADATA attempting internal generator.
ALTER TABLE NOTICE_TYPE
ADD CONSTRAINT SYS_C006150 PRIMARY KEY 
(
  NOTICE_TYPE_ID 
)
USING INDEX SYS_C007921
ENABLECREATE UNIQUE INDEX SYS_C007921 ON NOTICE_TYPE (NOTICE_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE NOTICE_TYPE 
(
  NOTICE_TYPE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE NOTICE_TYPE
ADD CONSTRAINT FKNOTICE_TYP683051 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE
ADD CONSTRAINT SYS_C006154 PRIMARY KEY 
(
  PAGE_ID 
)
USING INDEX SYS_C008304
ENABLECREATE UNIQUE INDEX SYS_C008304 ON PAGE (PAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE 
(
  PAGE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(500 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
, JAVASCRIPT VARCHAR2(4000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_ANSWER_ACTIVATION with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_ANSWER_ACTIVATION
ADD CONSTRAINT SYS_C006157 PRIMARY KEY 
(
  PAGE_ANSWER_ACTIVATION_ID 
)
USING INDEX SYS_C008054
ENABLECREATE UNIQUE INDEX SYS_C008054 ON PAGE_ANSWER_ACTIVATION (PAGE_ANSWER_ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_ANSWER_ACTIVATION 
(
  PAGE_ANSWER_ACTIVATION_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, QUESTION_ID NUMBER(10, 0) NOT NULL 
, PAGE_ID NUMBER(10, 0) NOT NULL 
, ANSWER VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE PAGE_ANSWER_ACTIVATION
ADD CONSTRAINT FKPAGE_ANSWE675907 FOREIGN KEY
(
  QUESTION_ID 
, CHAPTER_ID 
)
REFERENCES QUESTION_CHAPTER
(
  QUESTION_ID 
, CHAPTER_ID 
)
ENABLE
ALTER TABLE PAGE_ANSWER_ACTIVATION
ADD CONSTRAINT FKPAGE_ANSWE726226 FOREIGN KEY
(
  PAGE_ID 
, FORM_ID 
)
REFERENCES PAGE_FORM
(
  PAGE_ID 
, FORM_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_FORM
ADD CONSTRAINT SYS_C006164 PRIMARY KEY 
(
  PAGE_ID 
, FORM_ID 
)
USING INDEX SYS_C008284
ENABLECREATE UNIQUE INDEX SYS_C008284 ON PAGE_FORM (PAGE_ID ASC, FORM_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_FORM 
(
  PAGE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_MODE_ID NUMBER(10, 0) NOT NULL 
, PAGE_FORM_GROUP_ID NUMBER(10, 0) 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE PAGE_FORM
ADD CONSTRAINT FKPAGE_FORM164520 FOREIGN KEY
(
  PAGE_FORM_MODE_ID 
)
REFERENCES PAGE_FORM_MODE
(
  PAGE_FORM_MODE_ID 
)
ENABLE
ALTER TABLE PAGE_FORM
ADD CONSTRAINT FKPAGE_FORM418212 FOREIGN KEY
(
  PAGE_FORM_GROUP_ID 
)
REFERENCES PAGE_FORM_GROUP
(
  PAGE_FORM_GROUP_ID 
)
ENABLE
ALTER TABLE PAGE_FORM
ADD CONSTRAINT FKPAGE_FORM54236 FOREIGN KEY
(
  FORM_ID 
)
REFERENCES FORM
(
  FORM_ID 
)
ENABLE
ALTER TABLE PAGE_FORM
ADD CONSTRAINT FKPAGE_FORM976290 FOREIGN KEY
(
  PAGE_ID 
)
REFERENCES PAGE
(
  PAGE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_GROUP with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_FORM_GROUP
ADD CONSTRAINT SYS_C006169 PRIMARY KEY 
(
  PAGE_FORM_GROUP_ID 
)
USING INDEX SYS_C008246
ENABLECREATE UNIQUE INDEX SYS_C008246 ON PAGE_FORM_GROUP (PAGE_FORM_GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_FORM_GROUP 
(
  PAGE_FORM_GROUP_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_GROUP_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_FORM_GROUP_ACL
ADD CONSTRAINT SYS_C006171 PRIMARY KEY 
(
  PAGE_ID 
, FORM_ID 
, GROUP_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008182
ENABLECREATE UNIQUE INDEX SYS_C008182 ON PAGE_FORM_GROUP_ACL (PAGE_ID ASC, FORM_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_FORM_GROUP_ACL 
(
  PAGE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE PAGE_FORM_GROUP_ACL
ADD CONSTRAINT FKPAGE_FORM_481211 FOREIGN KEY
(
  PAGE_ID 
, FORM_ID 
)
REFERENCES PAGE_FORM
(
  PAGE_ID 
, FORM_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_GROUP_ACL
ADD CONSTRAINT FKPAGE_FORM_68585 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_GROUP_ACL
ADD CONSTRAINT FKPAGE_FORM_958025 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_MODE with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_FORM_MODE
ADD CONSTRAINT SYS_C006176 PRIMARY KEY 
(
  PAGE_FORM_MODE_ID 
)
USING INDEX SYS_C008249
ENABLECREATE UNIQUE INDEX SYS_C008249 ON PAGE_FORM_MODE (PAGE_FORM_MODE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_FORM_MODE 
(
  PAGE_FORM_MODE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_ROLE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_FORM_ROLE_ACL
ADD CONSTRAINT SYS_C006179 PRIMARY KEY 
(
  PAGE_ID 
, FORM_ID 
, ROLE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008240
ENABLECREATE UNIQUE INDEX SYS_C008240 ON PAGE_FORM_ROLE_ACL (PAGE_ID ASC, FORM_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_FORM_ROLE_ACL 
(
  PAGE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, ROLE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE PAGE_FORM_ROLE_ACL
ADD CONSTRAINT FKPAGE_FORM_257154 FOREIGN KEY
(
  ROLE_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_ROLE_ACL
ADD CONSTRAINT FKPAGE_FORM_618867 FOREIGN KEY
(
  PAGE_ID 
, FORM_ID 
)
REFERENCES PAGE_FORM
(
  PAGE_ID 
, FORM_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_ROLE_ACL
ADD CONSTRAINT FKPAGE_FORM_875908 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_SERVICE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_FORM_SERVICE_ACL
ADD CONSTRAINT SYS_C006184 PRIMARY KEY 
(
  PAGE_ID 
, FORM_ID 
, SERVICE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008172
ENABLECREATE UNIQUE INDEX SYS_C008172 ON PAGE_FORM_SERVICE_ACL (PAGE_ID ASC, FORM_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_FORM_SERVICE_ACL 
(
  PAGE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE PAGE_FORM_SERVICE_ACL
ADD CONSTRAINT FKPAGE_FORM_512263 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_SERVICE_ACL
ADD CONSTRAINT FKPAGE_FORM_632685 FOREIGN KEY
(
  PAGE_ID 
, FORM_ID 
)
REFERENCES PAGE_FORM
(
  PAGE_ID 
, FORM_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_SERVICE_ACL
ADD CONSTRAINT FKPAGE_FORM_844128 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_USER_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE PAGE_FORM_USER_ACL
ADD CONSTRAINT SYS_C006189 PRIMARY KEY 
(
  PAGE_ID 
, FORM_ID 
, USER_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008177
ENABLECREATE UNIQUE INDEX SYS_C008177 ON PAGE_FORM_USER_ACL (PAGE_ID ASC, FORM_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PAGE_FORM_USER_ACL 
(
  PAGE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE PAGE_FORM_USER_ACL
ADD CONSTRAINT FKPAGE_FORM_574053 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_USER_ACL
ADD CONSTRAINT FKPAGE_FORM_731720 FOREIGN KEY
(
  PAGE_ID 
, FORM_ID 
)
REFERENCES PAGE_FORM
(
  PAGE_ID 
, FORM_ID 
)
ENABLE
ALTER TABLE PAGE_FORM_USER_ACL
ADD CONSTRAINT FKPAGE_FORM_763055 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.PROPOSAL_ACTIVATION with DBMS_METADATA attempting internal generator.
ALTER TABLE PROPOSAL_ACTIVATION
ADD CONSTRAINT SYS_C006195 PRIMARY KEY 
(
  PROPOSAL_ACTIVATION_ID 
)
USING INDEX SYS_C007879
ENABLECREATE UNIQUE INDEX SYS_C007879 ON PROPOSAL_ACTIVATION (PROPOSAL_ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE PROPOSAL_ACTIVATION 
(
  PROPOSAL_ACTIVATION_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_TYPE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, CIRCULATION_STATE_ID NUMBER(10, 0) NOT NULL 
, DEADLINE_DATE DATE NOT NULL 
, REASON VARCHAR2(50 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE PROPOSAL_ACTIVATION
ADD CONSTRAINT FKPROPOSAL_A329504 FOREIGN KEY
(
  INSTANCE_ID 
)
REFERENCES INSTANCE
(
  INSTANCE_ID 
)
ENABLE
ALTER TABLE PROPOSAL_ACTIVATION
ADD CONSTRAINT FKPROPOSAL_A395289 FOREIGN KEY
(
  CIRCULATION_STATE_ID 
)
REFERENCES CIRCULATION_STATE
(
  CIRCULATION_STATE_ID 
)
ENABLE
ALTER TABLE PROPOSAL_ACTIVATION
ADD CONSTRAINT FKPROPOSAL_A748453 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
ALTER TABLE PROPOSAL_ACTIVATION
ADD CONSTRAINT FKPROPOSAL_A800438 FOREIGN KEY
(
  CIRCULATION_TYPE_ID 
)
REFERENCES CIRCULATION_TYPE
(
  CIRCULATION_TYPE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.QUESTION with DBMS_METADATA attempting internal generator.
ALTER TABLE QUESTION
ADD CONSTRAINT SYS_C006201 PRIMARY KEY 
(
  QUESTION_ID 
)
USING INDEX SYS_C008298
ENABLECREATE UNIQUE INDEX SYS_C008298 ON QUESTION (QUESTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE QUESTION 
(
  QUESTION_ID NUMBER(10, 0) NOT NULL 
, QUESTION_TYPE_ID NUMBER(10, 0) NOT NULL 
, MAPPING_ID NUMBER(10, 0) 
, ANSWER_QUERY_ID NUMBER(10, 0) 
, NAME VARCHAR2(500 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
, JAVASCRIPT VARCHAR2(4000 BYTE) 
, REGEX VARCHAR2(1000 BYTE) 
, DEFAULT_ANSWER VARCHAR2(4000 BYTE) 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE QUESTION
ADD CONSTRAINT FKQUESTION17051 FOREIGN KEY
(
  QUESTION_TYPE_ID 
)
REFERENCES QUESTION_TYPE
(
  QUESTION_TYPE_ID 
)
ENABLE
ALTER TABLE QUESTION
ADD CONSTRAINT FKQUESTION38014 FOREIGN KEY
(
  MAPPING_ID 
)
REFERENCES MAPPING
(
  MAPPING_ID 
)
ENABLE
ALTER TABLE QUESTION
ADD CONSTRAINT FKQUESTION493622 FOREIGN KEY
(
  ANSWER_QUERY_ID 
)
REFERENCES ANSWER_QUERY
(
  ANSWER_QUERY_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.QUESTION_CHAPTER with DBMS_METADATA attempting internal generator.
ALTER TABLE QUESTION_CHAPTER
ADD CONSTRAINT SYS_C006205 PRIMARY KEY 
(
  QUESTION_ID 
, CHAPTER_ID 
)
USING INDEX SYS_C008294
ENABLECREATE UNIQUE INDEX SYS_C008294 ON QUESTION_CHAPTER (QUESTION_ID ASC, CHAPTER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE QUESTION_CHAPTER 
(
  QUESTION_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, REQUIRED NUMBER(1, 0) NOT NULL 
, ITEM NUMBER(10, 0) DEFAULT 1 NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE QUESTION_CHAPTER
ADD CONSTRAINT FKQUESTION_C34531 FOREIGN KEY
(
  CHAPTER_ID 
)
REFERENCES CHAPTER
(
  CHAPTER_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER
ADD CONSTRAINT FKQUESTION_C836706 FOREIGN KEY
(
  QUESTION_ID 
)
REFERENCES QUESTION
(
  QUESTION_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.QUESTION_CHAPTER_GROUP_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE QUESTION_CHAPTER_GROUP_ACL
ADD CONSTRAINT SYS_C006211 PRIMARY KEY 
(
  QUESTION_ID 
, CHAPTER_ID 
, GROUP_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008152
ENABLECREATE UNIQUE INDEX SYS_C008152 ON QUESTION_CHAPTER_GROUP_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE QUESTION_CHAPTER_GROUP_ACL 
(
  QUESTION_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE QUESTION_CHAPTER_GROUP_ACL
ADD CONSTRAINT FKQUESTION_C301035 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_GROUP_ACL
ADD CONSTRAINT FKQUESTION_C725575 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_GROUP_ACL
ADD CONSTRAINT FKQUESTION_C801557 FOREIGN KEY
(
  QUESTION_ID 
, CHAPTER_ID 
)
REFERENCES QUESTION_CHAPTER
(
  QUESTION_ID 
, CHAPTER_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.QUESTION_CHAPTER_ROLE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE QUESTION_CHAPTER_ROLE_ACL
ADD CONSTRAINT SYS_C006216 PRIMARY KEY 
(
  QUESTION_ID 
, CHAPTER_ID 
, ROLE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008230
ENABLECREATE UNIQUE INDEX SYS_C008230 ON QUESTION_CHAPTER_ROLE_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE QUESTION_CHAPTER_ROLE_ACL 
(
  QUESTION_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, ROLE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE QUESTION_CHAPTER_ROLE_ACL
ADD CONSTRAINT FKQUESTION_C387846 FOREIGN KEY
(
  QUESTION_ID 
, CHAPTER_ID 
)
REFERENCES QUESTION_CHAPTER
(
  QUESTION_ID 
, CHAPTER_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_ROLE_ACL
ADD CONSTRAINT FKQUESTION_C56611 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_ROLE_ACL
ADD CONSTRAINT FKQUESTION_C895138 FOREIGN KEY
(
  ROLE_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.QUESTION_CHAPTER_SERVICE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE QUESTION_CHAPTER_SERVICE_ACL
ADD CONSTRAINT SYS_C006221 PRIMARY KEY 
(
  QUESTION_ID 
, CHAPTER_ID 
, SERVICE_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008142
ENABLECREATE UNIQUE INDEX SYS_C008142 ON QUESTION_CHAPTER_SERVICE_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE QUESTION_CHAPTER_SERVICE_ACL 
(
  QUESTION_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE QUESTION_CHAPTER_SERVICE_ACL
ADD CONSTRAINT FKQUESTION_C292861 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_SERVICE_ACL
ADD CONSTRAINT FKQUESTION_C483461 FOREIGN KEY
(
  QUESTION_ID 
, CHAPTER_ID 
)
REFERENCES QUESTION_CHAPTER
(
  QUESTION_ID 
, CHAPTER_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_SERVICE_ACL
ADD CONSTRAINT FKQUESTION_C960995 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.QUESTION_CHAPTER_USER_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE QUESTION_CHAPTER_USER_ACL
ADD CONSTRAINT SYS_C006226 PRIMARY KEY 
(
  QUESTION_ID 
, CHAPTER_ID 
, USER_ID 
, INSTANCE_STATE_ID 
)
USING INDEX SYS_C008147
ENABLECREATE UNIQUE INDEX SYS_C008147 ON QUESTION_CHAPTER_USER_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE QUESTION_CHAPTER_USER_ACL 
(
  QUESTION_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
, INSTANCE_STATE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE QUESTION_CHAPTER_USER_ACL
ADD CONSTRAINT FKQUESTION_C245244 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_USER_ACL
ADD CONSTRAINT FKQUESTION_C500699 FOREIGN KEY
(
  QUESTION_ID 
, CHAPTER_ID 
)
REFERENCES QUESTION_CHAPTER
(
  QUESTION_ID 
, CHAPTER_ID 
)
ENABLE
ALTER TABLE QUESTION_CHAPTER_USER_ACL
ADD CONSTRAINT FKQUESTION_C943757 FOREIGN KEY
(
  INSTANCE_STATE_ID 
)
REFERENCES INSTANCE_STATE
(
  INSTANCE_STATE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.QUESTION_TYPE with DBMS_METADATA attempting internal generator.
ALTER TABLE QUESTION_TYPE
ADD CONSTRAINT SYS_C006232 PRIMARY KEY 
(
  QUESTION_TYPE_ID 
)
USING INDEX SYS_C008266
ENABLECREATE UNIQUE INDEX SYS_C008266 ON QUESTION_TYPE (QUESTION_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE QUESTION_TYPE 
(
  QUESTION_TYPE_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(20 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.RESOURCE with DBMS_METADATA attempting internal generator.
ALTER TABLE "RESOURCE"
ADD CONSTRAINT SYS_C006234 PRIMARY KEY 
(
  RESOURCE_ID 
)
USING INDEX SYS_C008200
ENABLECREATE UNIQUE INDEX SYS_C008200 ON "RESOURCE" (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE "RESOURCE" 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, AVAILABLE_RESOURCE_ID VARCHAR2(25 BYTE) NOT NULL 
, NAME VARCHAR2(50 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(1000 BYTE) 
, TEMPLATE VARCHAR2(500 BYTE) 
, CLASS VARCHAR2(25 BYTE) 
, HIDDEN NUMBER(1, 0) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE "RESOURCE"
ADD CONSTRAINT FKRESOURCE987863 FOREIGN KEY
(
  AVAILABLE_RESOURCE_ID 
)
REFERENCES AVAILABLE_RESOURCE
(
  AVAILABLE_RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.ROLE with DBMS_METADATA attempting internal generator.
ALTER TABLE ROLE
ADD CONSTRAINT SYS_C006240 PRIMARY KEY 
(
  ROLE_ID 
)
USING INDEX SYS_C008332
ENABLECREATE UNIQUE INDEX SYS_C008332 ON ROLE (ROLE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE ROLE 
(
  ROLE_ID NUMBER(10, 0) NOT NULL 
, ROLE_PARENT_ID NUMBER(10, 0) 
, NAME VARCHAR2(100 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE ROLE
ADD CONSTRAINT FKROLE332436 FOREIGN KEY
(
  ROLE_PARENT_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_FORMLIST with DBMS_METADATA attempting internal generator.
ALTER TABLE R_FORMLIST
ADD CONSTRAINT SYS_C006243 PRIMARY KEY 
(
  RESOURCE_ID 
)
USING INDEX SYS_C008194
ENABLECREATE UNIQUE INDEX SYS_C008194 ON R_FORMLIST (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_FORMLIST 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_FORMLIST
ADD CONSTRAINT FKR_FORMLIST366375 FOREIGN KEY
(
  FORM_ID 
)
REFERENCES FORM
(
  FORM_ID 
)
ENABLE
ALTER TABLE R_FORMLIST
ADD CONSTRAINT FKR_FORMLIST990436 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_GROUP_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE R_GROUP_ACL
ADD CONSTRAINT SYS_C006246 PRIMARY KEY 
(
  RESOURCE_ID 
, GROUP_ID 
)
USING INDEX SYS_C008134
ENABLECREATE UNIQUE INDEX SYS_C008134 ON R_GROUP_ACL (RESOURCE_ID ASC, GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_GROUP_ACL 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_GROUP_ACL
ADD CONSTRAINT FKR_GROUP_AC496715 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
ALTER TABLE R_GROUP_ACL
ADD CONSTRAINT FKR_GROUP_AC973478 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_LIST with DBMS_METADATA attempting internal generator.
ALTER TABLE R_LIST
ADD CONSTRAINT SYS_C006249 PRIMARY KEY 
(
  RESOURCE_ID 
)
USING INDEX SYS_C008081
ENABLECREATE UNIQUE INDEX SYS_C008081 ON R_LIST (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_LIST 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, QUERY VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_LIST
ADD CONSTRAINT FKR_LIST348281 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_LIST_COLUMN with DBMS_METADATA attempting internal generator.
ALTER TABLE R_LIST_COLUMN
ADD CONSTRAINT SYS_C006252 PRIMARY KEY 
(
  R_LIST_COLUMN_ID 
)
USING INDEX SYS_C008018
ENABLECREATE UNIQUE INDEX SYS_C008018 ON R_LIST_COLUMN (R_LIST_COLUMN_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_LIST_COLUMN 
(
  R_LIST_COLUMN_ID NUMBER(10, 0) NOT NULL 
, RESOURCE_ID NUMBER(10, 0) NOT NULL 
, COLUMN_NAME VARCHAR2(30 BYTE) NOT NULL 
, ALIAS VARCHAR2(30 BYTE) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_LIST_COLUMN
ADD CONSTRAINT FKR_LIST_COL126145 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES R_LIST
(
  RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_ROLE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE R_ROLE_ACL
ADD CONSTRAINT SYS_C006258 PRIMARY KEY 
(
  RESOURCE_ID 
, ROLE_ID 
)
USING INDEX SYS_C008137
ENABLECREATE UNIQUE INDEX SYS_C008137 ON R_ROLE_ACL (RESOURCE_ID ASC, ROLE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_ROLE_ACL 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, ROLE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_ROLE_ACL
ADD CONSTRAINT FKR_ROLE_ACL272000 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
ALTER TABLE R_ROLE_ACL
ADD CONSTRAINT FKR_ROLE_ACL936846 FOREIGN KEY
(
  ROLE_ID 
)
REFERENCES ROLE
(
  ROLE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_SEARCH with DBMS_METADATA attempting internal generator.
ALTER TABLE R_SEARCH
ADD CONSTRAINT SYS_C006261 PRIMARY KEY 
(
  RESOURCE_ID 
)
USING INDEX SYS_C008203
ENABLECREATE UNIQUE INDEX SYS_C008203 ON R_SEARCH (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_SEARCH 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, RESULT_TEMPLATE VARCHAR2(500 BYTE) 
, QUERY VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_SEARCH
ADD CONSTRAINT FKR_SEARCH676397 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_SEARCH_COLUMN with DBMS_METADATA attempting internal generator.
ALTER TABLE R_SEARCH_COLUMN
ADD CONSTRAINT SYS_C006264 PRIMARY KEY 
(
  R_SEARCH_COLUMN_ID 
)
USING INDEX SYS_C008012
ENABLECREATE UNIQUE INDEX SYS_C008012 ON R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_SEARCH_COLUMN 
(
  R_SEARCH_COLUMN_ID NUMBER(10, 0) NOT NULL 
, RESOURCE_ID NUMBER(10, 0) NOT NULL 
, COLUMN_NAME VARCHAR2(30 BYTE) NOT NULL 
, ALIAS VARCHAR2(30 BYTE) NOT NULL 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_SEARCH_COLUMN
ADD CONSTRAINT FKR_SEARCH_C940968 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES R_SEARCH
(
  RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_SEARCH_FILTER with DBMS_METADATA attempting internal generator.
ALTER TABLE R_SEARCH_FILTER
ADD CONSTRAINT SYS_C006270 PRIMARY KEY 
(
  R_SEARCH_FILTER_ID 
)
USING INDEX SYS_C008315
ENABLECREATE UNIQUE INDEX SYS_C008315 ON R_SEARCH_FILTER (R_SEARCH_FILTER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_SEARCH_FILTER 
(
  R_SEARCH_FILTER_ID NUMBER(10, 0) NOT NULL 
, RESOURCE_ID NUMBER(10, 0) NOT NULL 
, QUESTION_ID NUMBER(10, 0) 
, FIELD_NAME VARCHAR2(50 BYTE) NOT NULL 
, LABEL VARCHAR2(1000 BYTE) NOT NULL 
, QUERY VARCHAR2(4000 BYTE) NOT NULL 
, WILDCARD NUMBER(1, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_SEARCH_FILTER
ADD CONSTRAINT " " FOREIGN KEY
(
  QUESTION_ID 
)
REFERENCES QUESTION
(
  QUESTION_ID 
)
ENABLE
ALTER TABLE R_SEARCH_FILTER
ADD CONSTRAINT FKR_SEARCH_F286171 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES R_SEARCH
(
  RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_SERVICE_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE R_SERVICE_ACL
ADD CONSTRAINT SYS_C006277 PRIMARY KEY 
(
  RESOURCE_ID 
, SERVICE_ID 
)
USING INDEX SYS_C008128
ENABLECREATE UNIQUE INDEX SYS_C008128 ON R_SERVICE_ACL (RESOURCE_ID ASC, SERVICE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_SERVICE_ACL 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_SERVICE_ACL
ADD CONSTRAINT FKR_SERVICE_418739 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
ALTER TABLE R_SERVICE_ACL
ADD CONSTRAINT FKR_SERVICE_752769 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.R_USER_ACL with DBMS_METADATA attempting internal generator.
ALTER TABLE R_USER_ACL
ADD CONSTRAINT SYS_C006280 PRIMARY KEY 
(
  RESOURCE_ID 
, USER_ID 
)
USING INDEX SYS_C008131
ENABLECREATE UNIQUE INDEX SYS_C008131 ON R_USER_ACL (RESOURCE_ID ASC, USER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE R_USER_ACL 
(
  RESOURCE_ID NUMBER(10, 0) NOT NULL 
, USER_ID NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE R_USER_ACL
ADD CONSTRAINT FKR_USER_ACL384853 FOREIGN KEY
(
  RESOURCE_ID 
)
REFERENCES "RESOURCE"
(
  RESOURCE_ID 
)
ENABLE
ALTER TABLE R_USER_ACL
ADD CONSTRAINT FKR_USER_ACL894360 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.SERVICE with DBMS_METADATA attempting internal generator.
ALTER TABLE SERVICE
ADD CONSTRAINT SYS_C006283 PRIMARY KEY 
(
  SERVICE_ID 
)
USING INDEX SYS_C008329
ENABLECREATE UNIQUE INDEX SYS_C008329 ON SERVICE (SERVICE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE SERVICE 
(
  SERVICE_ID NUMBER(10, 0) NOT NULL 
, SERVICE_GROUP_ID NUMBER(10, 0) NOT NULL 
, SERVICE_PARENT_ID NUMBER(10, 0) 
, NAME VARCHAR2(100 BYTE) NOT NULL 
, DESCRIPTION VARCHAR2(255 BYTE) 
, SORT NUMBER(10, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE SERVICE
ADD CONSTRAINT FKSERVICE360946 FOREIGN KEY
(
  SERVICE_GROUP_ID 
)
REFERENCES SERVICE_GROUP
(
  SERVICE_GROUP_ID 
)
ENABLE
ALTER TABLE SERVICE
ADD CONSTRAINT FKSERVICE570159 FOREIGN KEY
(
  SERVICE_PARENT_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.SERVICE_ANSWER_ACTIVATION with DBMS_METADATA attempting internal generator.
ALTER TABLE SERVICE_ANSWER_ACTIVATION
ADD CONSTRAINT SYS_C006288 PRIMARY KEY 
(
  SERVICE_ANSWER_ACTIVATION_ID 
)
USING INDEX SYS_C008256
ENABLECREATE UNIQUE INDEX SYS_C008256 ON SERVICE_ANSWER_ACTIVATION (SERVICE_ANSWER_ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE SERVICE_ANSWER_ACTIVATION 
(
  SERVICE_ANSWER_ACTIVATION_ID NUMBER(10, 0) NOT NULL 
, FORM_ID NUMBER(10, 0) NOT NULL 
, CHAPTER_ID NUMBER(10, 0) NOT NULL 
, QUESTION_ID NUMBER(10, 0) NOT NULL 
, SERVICE_ID NUMBER(10, 0) NOT NULL 
, ANSWER VARCHAR2(4000 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE SERVICE_ANSWER_ACTIVATION
ADD CONSTRAINT FKSERVICE_AN303296 FOREIGN KEY
(
  FORM_ID 
)
REFERENCES FORM
(
  FORM_ID 
)
ENABLE
ALTER TABLE SERVICE_ANSWER_ACTIVATION
ADD CONSTRAINT FKSERVICE_AN335241 FOREIGN KEY
(
  QUESTION_ID 
, CHAPTER_ID 
)
REFERENCES QUESTION_CHAPTER
(
  QUESTION_ID 
, CHAPTER_ID 
)
ENABLE
ALTER TABLE SERVICE_ANSWER_ACTIVATION
ADD CONSTRAINT FKSERVICE_AN860026 FOREIGN KEY
(
  SERVICE_ID 
)
REFERENCES SERVICE
(
  SERVICE_ID 
)
ENABLE
-- Unable to render TABLE DDL for object CAMAC_DEV.SERVICE_GROUP with DBMS_METADATA attempting internal generator.
ALTER TABLE SERVICE_GROUP
ADD CONSTRAINT SYS_C006295 PRIMARY KEY 
(
  SERVICE_GROUP_ID 
)
USING INDEX SYS_C008259
ENABLECREATE UNIQUE INDEX SYS_C008259 ON SERVICE_GROUP (SERVICE_GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE SERVICE_GROUP 
(
  SERVICE_GROUP_ID NUMBER(10, 0) NOT NULL 
, NAME VARCHAR2(100 BYTE) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.USER with DBMS_METADATA attempting internal generator.
ALTER TABLE "USER"
ADD CONSTRAINT SYS_C006299 PRIMARY KEY 
(
  USER_ID 
)
USING INDEX SYS_C008343
ENABLEALTER TABLE "USER"
ADD CONSTRAINT SYS_C006298 UNIQUE 
(
  USERNAME 
)
USING INDEX SYS_C008344
ENABLECREATE UNIQUE INDEX SYS_C008343 ON "USER" (USER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
CREATE UNIQUE INDEX SYS_C008344 ON "USER" (USERNAME ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE "USER" 
(
  USER_ID NUMBER(10, 0) NOT NULL 
, USERNAME VARCHAR2(250 BYTE) NOT NULL 
, PASSWORD VARCHAR2(50 BYTE) 
, NAME VARCHAR2(100 BYTE) NOT NULL 
, SURNAME VARCHAR2(100 BYTE) NOT NULL 
, EMAIL VARCHAR2(100 BYTE) 
, PHONE VARCHAR2(100 BYTE) 
, DISABLED NUMBER(1, 0) DEFAULT '0' NOT NULL 
, LANGUAGE VARCHAR2(2 BYTE) NOT NULL 
, LAST_REQUEST_DATE DATE 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESS
-- Unable to render TABLE DDL for object CAMAC_DEV.USER_GROUP with DBMS_METADATA attempting internal generator.
ALTER TABLE USER_GROUP
ADD CONSTRAINT SYS_C006306 PRIMARY KEY 
(
  USER_ID 
, GROUP_ID 
)
USING INDEX SYS_C008324
ENABLECREATE UNIQUE INDEX SYS_C008324 ON USER_GROUP (USER_ID ASC, GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLELCREATE TABLE USER_GROUP 
(
  USER_ID NUMBER(10, 0) NOT NULL 
, GROUP_ID NUMBER(10, 0) NOT NULL 
, DEFAULT_GROUP NUMBER(1, 0) NOT NULL 
) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
PCTUSED 40 
INITRANS 1 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOCOMPRESSALTER TABLE USER_GROUP
ADD CONSTRAINT FKUSER_GROUP311810 FOREIGN KEY
(
  USER_ID 
)
REFERENCES "USER"
(
  USER_ID 
)
ENABLE
ALTER TABLE USER_GROUP
ADD CONSTRAINT FKUSER_GROUP67788 FOREIGN KEY
(
  GROUP_ID 
)
REFERENCES "GROUP"
(
  GROUP_ID 
)
ENABLE
REM INSERTING into CAMAC_DEV.ACTION
SET DEFINE OFF;
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (5,'save',2,'Dossier erstellen',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (6,'location',2,'Gemeinde setzen',null,null,null,0,1);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (7,'php',2,'Dossier Nummer erstellen',null,null,null,0,2);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (8,'save',3,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (9,'formtransition',4,'Freigeben an Gemeinde COMM - EXT',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (10,'save',5,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (67,'save',64,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (68,'location',64,'Location setzen',null,null,null,0,1);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (23,'save',22,'Stellungnahme speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (24,'circulationtransition',23,'Zirkulation Status OK',null,null,null,0,1);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (25,'save',23,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (26,'php',22,'Temporar ZirkEnde',null,null,null,0,1);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (27,'php',23,'Set to redac if all done',null,null,null,0,2);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (28,'notice',24,'Retrieve NOtice',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (69,'php',64,'Dossier nummer setzen',null,null,null,0,2);
REM INSERTING into CAMAC_DEV.ACTIVATION
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.ACTIVATION_LOG
SET DEFINE OFF;
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (1,1,21,'i',to_date('23-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (2,2,21,'i',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (3,2,21,'u',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (4,2,21,'u',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (5,2,21,'u',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (6,2,21,'u',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (7,2,21,'u',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (8,3,21,'i',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (9,3,21,'u',to_date('26-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (10,3,21,'u',to_date('27-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (11,3,21,'u',to_date('27-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (12,3,21,'u',to_date('27-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (13,1,21,'u',to_date('03-JUN-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (30,1,21,'u',to_date('04-JUN-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (50,1,21,'u',to_date('10-JUN-14','DD-MON-RR'));
REM INSERTING into CAMAC_DEV.AIR_ACTION
SET DEFINE OFF;
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formwizard','wizard',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formwizard','get-file',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('newform','new',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editformpage','edit-page',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editformpage','get-file',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editformpages','edit-pages',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editformpages','get-file',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formpage','read-page',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formpage','get-file',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formpages','read-pages',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formpages','get-file',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('allformpages','index',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('allformpages','get-file',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formerror','form-error',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editcirculation','edit',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editcirculation','add',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editcirculation','add-activation',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editcirculation','get-image',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('circulation','index',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('circulation','get-image',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editnotice','list-notice',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editnotice','edit-notice',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editnotice','get-image',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editnotice','list',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editnotice','upload',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editcirculation','read-notice',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('circulation','read-notice',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('letter','index',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('letter','get-image',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editletter','edit',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editletter','get-image',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editletter','list',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('editletter','upload',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('page','index',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('history','index',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('documents','list',0);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('documents','upload',1);
REM INSERTING into CAMAC_DEV.ANSWER
SET DEFINE OFF;
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,23,1,1,'Hansi Hinterseer');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,6,2,1,'01-14-005');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,1,2,1,'Hallihallo$

eine Mehrzeilige Mitteilung

haha');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,22,21,1,'a:1:{i:0;s:0:"";}');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (32,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (32,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (32,6,2,1,'01-14-032');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (32,1,2,1,'abc');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (32,5,2,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (41,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (41,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (41,6,2,1,'01-14-033');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (42,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (42,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (65,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (65,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (65,6,2,1,'01-14-006');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,3,2,1,'0');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (43,64,1,1,'031 123 987');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (82,2,3,1,'2');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (82,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (82,6,2,1,'02-14-002');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (83,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (83,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (83,6,2,1,'01-14-007');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (102,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (102,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (102,6,2,1,'01-14-008');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,6,2,1,'01-14-009');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,2,2,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,1,2,1,'foobar');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,3,2,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,5,2,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,23,1,1,'foo bar');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,61,1,1,'foobarstr 6');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,62,1,1,'3076');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,63,1,1,'Worb');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,68,1,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,79,1,1,'0');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,80,1,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,22,21,1,'a:1:{i:0;s:2:"W4";}');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,94,21,1,'a:1:{i:0;s:4:"NSlu";}');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,95,21,1,'a:1:{i:0;s:3:"WRZ";}');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,97,21,1,'a:2:{i:0;s:2:"21";i:1;s:2:"28";}');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,99,21,1,'a:1:{i:0;s:1:"W";}');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,102,21,1,'720000');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (122,103,21,1,'aha');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (142,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (142,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (142,6,2,1,'01-14-010');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (162,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (162,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (162,6,2,1,'01-14-011');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (163,2,3,1,'5');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (163,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (164,2,3,1,'10');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (164,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (164,6,2,1,'10-14-002');
REM INSERTING into CAMAC_DEV.ANSWER_LIST
SET DEFINE OFF;
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (1,4,'abm','Brandschutz (ABM)',0);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (2,4,'afe','Energienachweis',1);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (3,4,'afemin','Minergienachweis (AfE)',2);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (4,4,'qgp','Sondernutzunsplanung (QGP / QP)',3);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (5,4,'nhsdenkmal','kommunales Kulturobjekt (NHS Denkmalpflege)',4);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (6,4,'nhsschutz','kommunales Schutzobjekt /-gebiet (NHS)',5);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (7,5,'bkbuerg','Baukomission Burglen',0);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (21,22,'W1','Wohnzonen 1',0);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (22,22,'W2','Wohnzonen 2',2);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (23,22,'W3','Wohnzonen 3',3);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (24,22,'W4','Wohnzonen 4',4);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (25,22,'WS','Sonderwohnzonen',5);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (26,22,'G','Gewerbezonen',6);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (27,22,'I','Industriezonen',7);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (28,22,'WG2','Wohn- und Gewerbezonen 2',8);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (29,22,'WG3','Wohn- und Gewerbezonen 3',9);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (30,22,'WG4','Wohn- und Gewerbezonen 4',10);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (31,22,'KS','Kernzonen - Schutz',11);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (32,22,'KZ','Kernzonen - Zentrum',12);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (33,22,'B','Bahnhofzonen',13);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (34,22,'O','Zonen fur offentliche Bauten und Anlagen',14);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (35,22,'F','Freihaltezonen',15);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (36,22,'T','Tourismuszonen',16);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (37,22,'SF','Zonen fur Sport- und Freizeitanlagen',17);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (38,22,'ViB','Verkehrsflachen innerhalb Bauzone',18);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (39,22,'AB','Zonen fur besondere Anlagen und Betriebsstatten',19);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (40,22,'LW','Landwirtschaftszonen',20);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (41,22,'SLW','Speziallandwirtschaftszonen',21);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (42,22,'RB','Rebbauzonen',22);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (43,22,'NSl','Naturschutzzonen lokal',23);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (44,22,'FaB','Freihaltezone ausserhalb Bauzonen',24);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (45,22,'GR','Gewasserraumzonen',25);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (46,22,'Ge','Gewasser',26);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (47,22,'W','Weilerzone',27);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (48,22,'VaB','Verkehrsflachen ausserhalb Bauzonen',28);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (49,22,'R','Reservezonen',29);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (50,22,'Wa','Wald',30);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (51,22,'D','Deponiezonen',31);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (52,22,'A','Abbauzonen',32);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (53,22,'AD','Abbau- und Deponiezonen',33);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (54,22,'U','ubriges Gemeindegebiet',34);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (62,94,'OS','Ortsbildschutzzonen',1);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (63,94,'SOK','Schutzobjekte in Kernzonen',2);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (64,94,'Arch','archaologische Fundstellen und Funderwartungsgebiete',3);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (65,94,'NSlu','Naturschutzzonen lokal, uberlagert',4);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (66,94,'LSl','Landschaftsschutzzonen lokal',5);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (67,94,'LpB','Gebiete mit landschaftspragenden Bauten',6);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (68,94,'TrS','Gebiete mit traditioneller Streubauweise',7);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (69,94,'GRu','Gewasserraumzonen, uberlagert',8);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (70,94,'GZr','Gefahrenzonen rot',9);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (71,94,'GZb','Gefahrenzonen blau',10);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (72,94,'GZg','Gefahrenzonen gelb',11);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (73,94,'WS','Zonen fur Wintersport',12);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (74,94,'Du','Deponiezonen, uberlagert',13);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (75,94,'Au','Abbauzonen, uberlagert',14);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (76,94,'ABu','Zonen fur besondere Anlagen und Betriebsstatten, uberlagert',15);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (77,94,'ZBG','Zone fur Bauten im Gewasser',16);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (78,94,'SFu','Zonen fur Sport- und Freizeitanlagen, uberlagert',17);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (79,94,'QPr','Bereich rechtsgultiger Quartierplan',18);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (80,94,'QGPr','Bereich rechtsgultiger Quartiergestaltungsplan',19);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (81,94,'QPp','Zonen mit Quartierplanpflicht',20);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (82,94,'QGPp','Zonen mit Quartiergestaltungsplanpflicht',21);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (83,94,'NvI','Nutzungsvorbehalt Immissionsschutz',22);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (84,94,'GvRR','Genehmigungsvorbehalt RR',23);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (85,94,'wfF','weitere flachenbezogene Festlegungen',24);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (86,94,'BLS','Baulinien Strasse',25);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (87,94,'BLG','Baulinien Gewasser',26);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (88,94,'BLI','Baulinien Immissionsschutz',27);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (89,94,'BL','weitere Baulinien',28);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (90,94,'NOll','Naturobjekte lokal, linear',29);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (91,94,'KOll','Kulturobjekte lokal, linear',30);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (92,94,'KOrnl','Kulturobjekte regional / national, linear',31);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (93,94,'NOl','Naturobjekte lokal',32);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (94,94,'KOl','Kulturobjekte lokal',33);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (95,94,'EO','Einzelobjekte in Kern- und Schutzzonen',34);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (97,95,'GSZ','Grundwasserschutzzonen',1);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (98,95,'GSZp','Grundwasserschutzzonen provisorisch',2);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (99,95,'GSA','Grundwasserschutzareale',3);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (100,95,'GSAp','Grundwasserschutzareale provisorisch',4);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (101,95,'GG','Gefahrengebiete',5);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (102,95,'WR','Waldreservate',7);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (103,95,'NSrn','Naturschutzzonen regional / national',8);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (104,95,'LSrn','Landschaftsschutzzonen regional / national',9);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (105,95,'NOrnl','Naturobjekte regional / national, linear',10);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (106,95,'NOrn','Naturobjekte regional / national, punktformig',11);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (107,95,'KOrn','Kulturobjekte regional / national, punktformig',12);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (108,95,'FFF','Fruchtfolgeflachen',13);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (109,95,'WRZ','Wildruhezonen',6);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (110,97,'21','Neubau',0);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (111,97,'22','Umbau',1);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (112,97,'23','An/Aufbau',2);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (113,97,'24','Zeckanderung',3);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (114,97,'25','Terrainveranderung',4);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (115,97,'26','Abbruch',5);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (116,97,'27','Reklame',6);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (117,97,'28','Garage',7);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (118,97,'29','Solaranlage',8);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (119,97,'30','Fassadensanierung',9);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (120,97,'31','EFH',10);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (121,97,'32','MFH',11);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (122,97,'33','Geschaftshaus',12);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (123,97,'34','Lagergebaude',13);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (124,97,'35','Antennenanlage',14);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (125,97,'36','Unterkellerung',15);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (126,99,'I','Industrie',0);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (127,99,'D','Dienstleistung',1);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (128,99,'B','Buro',2);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (129,99,'W','Wohnen',3);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (130,99,'G','Gewerbe',4);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (131,99,'La','Lager',5);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (132,99,'L','Landwirtschaft',6);
Insert into CAMAC_DEV.ANSWER_LIST (ANSWER_LIST_ID,QUESTION_ID,VALUE,NAME,SORT) values (133,99,'Pr','Produktion',7);
REM INSERTING into CAMAC_DEV.ANSWER_LOG
SET DEFINE OFF;
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (1,to_date('22-MAY-14','DD-MON-RR'),21,'i',1,'INSTANCE_ID',6,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (2,to_date('22-MAY-14','DD-MON-RR'),21,'i',1,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (3,to_date('22-MAY-14','DD-MON-RR'),21,'i',1,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (4,to_date('23-MAY-14','DD-MON-RR'),21,'i',2,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (5,to_date('23-MAY-14','DD-MON-RR'),21,'i',2,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (6,to_date('23-MAY-14','DD-MON-RR'),21,'i',3,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (7,to_date('23-MAY-14','DD-MON-RR'),21,'i',3,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (8,to_date('23-MAY-14','DD-MON-RR'),21,'i',4,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (9,to_date('23-MAY-14','DD-MON-RR'),21,'i',4,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (10,to_date('23-MAY-14','DD-MON-RR'),21,'i',5,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (11,to_date('23-MAY-14','DD-MON-RR'),21,'i',5,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (12,to_date('23-MAY-14','DD-MON-RR'),21,'i',6,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (13,to_date('23-MAY-14','DD-MON-RR'),21,'i',6,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (14,to_date('23-MAY-14','DD-MON-RR'),21,'i',7,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (15,to_date('23-MAY-14','DD-MON-RR'),21,'i',7,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (16,to_date('23-MAY-14','DD-MON-RR'),21,'i',1,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (17,to_date('23-MAY-14','DD-MON-RR'),21,'i',1,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (18,to_date('23-MAY-14','DD-MON-RR'),21,'i',2,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (19,to_date('23-MAY-14','DD-MON-RR'),21,'i',2,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (20,to_date('23-MAY-14','DD-MON-RR'),21,'i',3,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (21,to_date('23-MAY-14','DD-MON-RR'),21,'i',3,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (22,to_date('23-MAY-14','DD-MON-RR'),21,'i',4,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (23,to_date('23-MAY-14','DD-MON-RR'),21,'i',4,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (24,to_date('23-MAY-14','DD-MON-RR'),21,'i',5,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (25,to_date('23-MAY-14','DD-MON-RR'),21,'i',5,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (26,to_date('23-MAY-14','DD-MON-RR'),21,'i',6,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (27,to_date('23-MAY-14','DD-MON-RR'),21,'i',6,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (28,to_date('23-MAY-14','DD-MON-RR'),21,'i',7,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (29,to_date('23-MAY-14','DD-MON-RR'),21,'i',7,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (30,to_date('23-MAY-14','DD-MON-RR'),21,'i',8,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (31,to_date('23-MAY-14','DD-MON-RR'),21,'i',8,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (32,to_date('23-MAY-14','DD-MON-RR'),21,'i',9,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (33,to_date('23-MAY-14','DD-MON-RR'),21,'i',9,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (34,to_date('23-MAY-14','DD-MON-RR'),21,'i',10,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (35,to_date('23-MAY-14','DD-MON-RR'),21,'i',10,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (36,to_date('23-MAY-14','DD-MON-RR'),21,'i',11,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (37,to_date('23-MAY-14','DD-MON-RR'),21,'i',11,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (38,to_date('23-MAY-14','DD-MON-RR'),21,'i',12,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (39,to_date('23-MAY-14','DD-MON-RR'),21,'i',12,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (40,to_date('23-MAY-14','DD-MON-RR'),21,'i',13,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (41,to_date('23-MAY-14','DD-MON-RR'),21,'i',13,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (42,to_date('23-MAY-14','DD-MON-RR'),21,'i',14,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (43,to_date('23-MAY-14','DD-MON-RR'),21,'i',14,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (44,to_date('23-MAY-14','DD-MON-RR'),21,'i',15,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (45,to_date('23-MAY-14','DD-MON-RR'),21,'i',15,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (46,to_date('23-MAY-14','DD-MON-RR'),21,'i',16,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (47,to_date('23-MAY-14','DD-MON-RR'),21,'i',16,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (48,to_date('23-MAY-14','DD-MON-RR'),21,'i',17,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (49,to_date('23-MAY-14','DD-MON-RR'),21,'i',17,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (50,to_date('23-MAY-14','DD-MON-RR'),21,'i',18,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (51,to_date('23-MAY-14','DD-MON-RR'),21,'i',18,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (52,to_date('23-MAY-14','DD-MON-RR'),21,'i',19,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (53,to_date('23-MAY-14','DD-MON-RR'),21,'i',19,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (54,to_date('23-MAY-14','DD-MON-RR'),21,'i',20,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (55,to_date('23-MAY-14','DD-MON-RR'),21,'i',20,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (56,to_date('23-MAY-14','DD-MON-RR'),21,'i',21,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (57,to_date('23-MAY-14','DD-MON-RR'),21,'i',21,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (58,to_date('23-MAY-14','DD-MON-RR'),21,'i',22,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (59,to_date('23-MAY-14','DD-MON-RR'),21,'i',22,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (60,to_date('23-MAY-14','DD-MON-RR'),21,'i',23,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (61,to_date('23-MAY-14','DD-MON-RR'),21,'i',23,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (62,to_date('23-MAY-14','DD-MON-RR'),21,'i',24,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (63,to_date('23-MAY-14','DD-MON-RR'),21,'i',24,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (64,to_date('23-MAY-14','DD-MON-RR'),21,'i',25,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (65,to_date('23-MAY-14','DD-MON-RR'),21,'i',25,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (66,to_date('23-MAY-14','DD-MON-RR'),21,'i',26,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (67,to_date('23-MAY-14','DD-MON-RR'),21,'i',26,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (68,to_date('23-MAY-14','DD-MON-RR'),21,'i',27,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (69,to_date('23-MAY-14','DD-MON-RR'),21,'i',27,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (70,to_date('23-MAY-14','DD-MON-RR'),21,'i',28,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (71,to_date('23-MAY-14','DD-MON-RR'),21,'i',28,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (72,to_date('23-MAY-14','DD-MON-RR'),21,'i',29,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (73,to_date('23-MAY-14','DD-MON-RR'),21,'i',29,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (74,to_date('23-MAY-14','DD-MON-RR'),21,'i',30,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (75,to_date('23-MAY-14','DD-MON-RR'),21,'i',30,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (76,to_date('23-MAY-14','DD-MON-RR'),21,'i',31,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (77,to_date('23-MAY-14','DD-MON-RR'),21,'i',31,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (78,to_date('23-MAY-14','DD-MON-RR'),21,'i',32,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (79,to_date('23-MAY-14','DD-MON-RR'),21,'i',32,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (80,to_date('23-MAY-14','DD-MON-RR'),21,'i',32,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (81,to_date('23-MAY-14','DD-MON-RR'),21,'i',32,'INSTANCE_ID',1,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (82,to_date('23-MAY-14','DD-MON-RR'),21,'i',32,'INSTANCE_ID',5,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (101,to_date('26-MAY-14','DD-MON-RR'),21,'i',41,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (102,to_date('26-MAY-14','DD-MON-RR'),21,'i',41,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (103,to_date('26-MAY-14','DD-MON-RR'),21,'i',41,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (104,to_date('27-MAY-14','DD-MON-RR'),21,'i',42,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (105,to_date('27-MAY-14','DD-MON-RR'),21,'i',42,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (106,to_date('27-MAY-14','DD-MON-RR'),21,'i',42,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (107,to_date('27-MAY-14','DD-MON-RR'),21,'i',42,'INSTANCE_ID',1,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (108,to_date('27-MAY-14','DD-MON-RR'),21,'i',42,'INSTANCE_ID',21,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (109,to_date('27-MAY-14','DD-MON-RR'),21,'d',42,'INSTANCE_ID',1,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (110,to_date('27-MAY-14','DD-MON-RR'),21,'d',42,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (111,to_date('27-MAY-14','DD-MON-RR'),21,'u',42,'INSTANCE_ID',21,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (112,to_date('02-JUN-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (113,to_date('02-JUN-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (114,to_date('02-JUN-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (115,to_date('03-JUN-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',1,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (116,to_date('03-JUN-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',22,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (117,to_date('03-JUN-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',23,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (124,to_date('06-JUN-14','DD-MON-RR'),21,'u',43,'INSTANCE_ID',1,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (144,to_date('22-JUL-14','DD-MON-RR'),21,'i',65,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (145,to_date('22-JUL-14','DD-MON-RR'),21,'i',65,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (146,to_date('22-JUL-14','DD-MON-RR'),21,'i',65,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (147,to_date('22-JUL-14','DD-MON-RR'),21,'u',43,'INSTANCE_ID',1,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (148,to_date('22-JUL-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',3,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (149,to_date('22-JUL-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',64,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (150,to_date('22-JUL-14','DD-MON-RR'),21,'u',43,'INSTANCE_ID',64,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (151,to_date('22-JUL-14','DD-MON-RR'),21,'u',43,'INSTANCE_ID',64,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (164,to_date('23-JUL-14','DD-MON-RR'),21,'i',82,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (165,to_date('23-JUL-14','DD-MON-RR'),21,'i',82,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (166,to_date('23-JUL-14','DD-MON-RR'),21,'i',82,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (167,to_date('23-JUL-14','DD-MON-RR'),21,'i',83,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (168,to_date('23-JUL-14','DD-MON-RR'),21,'i',83,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (169,to_date('23-JUL-14','DD-MON-RR'),21,'i',83,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (184,to_date('24-JUL-14','DD-MON-RR'),21,'i',102,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (185,to_date('24-JUL-14','DD-MON-RR'),21,'i',102,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (186,to_date('24-JUL-14','DD-MON-RR'),21,'i',102,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (204,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (205,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (206,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (207,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',2,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (208,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',1,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (209,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',3,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (210,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',5,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (211,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',23,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (212,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',61,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (213,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',62,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (214,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',63,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (215,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',68,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (216,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',79,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (217,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',80,'QUESTION_ID',1,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (218,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',22,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (219,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',94,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (220,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',95,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (221,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',97,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (222,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',99,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (223,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',102,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (224,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',103,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (225,to_date('28-JUL-14','DD-MON-RR'),21,'u',122,'INSTANCE_ID',97,'QUESTION_ID',21,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (226,to_date('29-JUL-14','DD-MON-RR'),21,'i',142,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (227,to_date('29-JUL-14','DD-MON-RR'),21,'i',142,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (228,to_date('29-JUL-14','DD-MON-RR'),21,'i',142,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (244,to_date('30-JUL-14','DD-MON-RR'),21,'i',162,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (245,to_date('30-JUL-14','DD-MON-RR'),21,'i',162,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (246,to_date('30-JUL-14','DD-MON-RR'),21,'i',162,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (247,to_date('30-JUL-14','DD-MON-RR'),21,'i',163,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (248,to_date('30-JUL-14','DD-MON-RR'),21,'i',163,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (249,to_date('30-JUL-14','DD-MON-RR'),21,'i',164,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (250,to_date('30-JUL-14','DD-MON-RR'),21,'i',164,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (251,to_date('30-JUL-14','DD-MON-RR'),21,'i',164,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
REM INSERTING into CAMAC_DEV.ANSWER_QUERY
SET DEFINE OFF;
Insert into CAMAC_DEV.ANSWER_QUERY (ANSWER_QUERY_ID,NAME,QUERY) values (1,'Gemeinde','SELECT

	LOCATION_ID, NAME

FROM

	LOCATION

	
WHERE
	LOCATION_ID IN (
	  SELECT
	  	LOCATION_ID
	  FROM
	  	GROUP_LOCATION
	  WHERE
	  	GROUP_ID = [GROUP_ID]
	  )
	  OR
	  [ROLE_ID] = 1001');
Insert into CAMAC_DEV.ANSWER_QUERY (ANSWER_QUERY_ID,NAME,QUERY) values (21,'Zonenplan','SELECT
 ID, DESCRIPTION
FROM
 MAP_ZONE2');
REM INSERTING into CAMAC_DEV.AR_ACTION
SET DEFINE OFF;
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('page','index',0);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('formlist','list',0);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('search','index',0);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('search','result',1);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('list','index',0);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('glossary','index',0);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('glossary','add-category',1);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('glossary','edit-category',1);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('glossary','add-sentence',1);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('glossary','edit-sentence',1);
Insert into CAMAC_DEV.AR_ACTION (AVAILABLE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('glossary','list',1);
REM INSERTING into CAMAC_DEV.ATTACHMENT
SET DEFINE OFF;
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE) values (21,'Websiteupdate20050902-1104.pdf',43,'/tmp/uploads//43//tmp/uploads//43/Websiteupdate20050902-1104.pdf',29,to_date('06-JUN-14','DD-MON-RR'),21,'698ef120a5b821a24d917bc0ee6dc152','application/pdf');
REM INSERTING into CAMAC_DEV.AVAILABLE_ACTION
SET DEFINE OFF;
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('save','default','Save');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('email','default','Send e-mail');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('formtransition','default','Make a transition');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('checkquery','default','Check with a SQL query');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('php','default','Call PHP');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('circulationtransition','default','Change state of the circulation');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('proposal','default','Generate proposal activation');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('location','default','Set location of instance');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('notice','default','Retrieve notice');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('copydata','default','Copy data from question to table');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('savepdf','default','Save PDF from a form');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('validate','default','Validate the form');
Insert into CAMAC_DEV.AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('wsgeocode','wsgeocode','WS geocode');
REM INSERTING into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE
SET DEFINE OFF;
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('newform','default','form','Create the form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('editformpage','default','form','Edit one page of the form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('editformpages','default','form','Edit multiple page of the form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('formpage','default','form','Read one page of the form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('formpages','default','form','Read multiple page of the form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('allformpages','default','form','Read all pages of the form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('formerror','default','form','Page with error list of the form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('formwizard','default','form','Wizard for the creation of a form');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('editcirculation','default','circulation','Edit the circulation');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('circulation','default','circulation','Read the circulation');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('editnotice','default','circulation','Edit the notice');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('letter','default','letter','Read letter');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('editletter','default','letter','Edit letter');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('page','default','page','Page from template');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('history','history','index','History of an instance');
Insert into CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('documents','documents','list','List the Documents');
REM INSERTING into CAMAC_DEV.AVAILABLE_RESOURCE
SET DEFINE OFF;
Insert into CAMAC_DEV.AVAILABLE_RESOURCE (AVAILABLE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('page','default','index','Page from template');
Insert into CAMAC_DEV.AVAILABLE_RESOURCE (AVAILABLE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('formlist','default','form','Page with a list of forms');
Insert into CAMAC_DEV.AVAILABLE_RESOURCE (AVAILABLE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('search','default','search','Page with search function');
Insert into CAMAC_DEV.AVAILABLE_RESOURCE (AVAILABLE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('list','default','list','Page with a list of instances');
Insert into CAMAC_DEV.AVAILABLE_RESOURCE (AVAILABLE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('glossary','glossary','index','Glossary');
REM INSERTING into CAMAC_DEV.A_CHECKQUERY
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.A_CIRCULATIONTRANSITION
SET DEFINE OFF;
Insert into CAMAC_DEV.A_CIRCULATIONTRANSITION (ACTION_ID,CURRENT_CIRCULATION_STATE_ID,NEXT_CIRCULATION_STATE_ID) values (24,null,2);
REM INSERTING into CAMAC_DEV.A_COPYDATA
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.A_COPYDATA_MAPPING
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.A_EMAIL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.A_FORMTRANSITION
SET DEFINE OFF;
Insert into CAMAC_DEV.A_FORMTRANSITION (ACTION_ID,CURRENT_INSTANCE_STATE_ID,NEXT_INSTANCE_STATE_ID) values (9,21,22);
REM INSERTING into CAMAC_DEV.A_LOCATION
SET DEFINE OFF;
Insert into CAMAC_DEV.A_LOCATION (ACTION_ID) values (6);
Insert into CAMAC_DEV.A_LOCATION (ACTION_ID) values (68);
REM INSERTING into CAMAC_DEV.A_LOCATION_QC
SET DEFINE OFF;
Insert into CAMAC_DEV.A_LOCATION_QC (A_LOCATION_QC_ID,ACTION_ID,QUESTION_ID,CHAPTER_ID) values (3,6,2,3);
Insert into CAMAC_DEV.A_LOCATION_QC (A_LOCATION_QC_ID,ACTION_ID,QUESTION_ID,CHAPTER_ID) values (21,68,2,3);
REM INSERTING into CAMAC_DEV.A_NOTICE
SET DEFINE OFF;
Insert into CAMAC_DEV.A_NOTICE (ACTION_ID,NOTICE_TYPE_ID,QUERY) values (28,1,'select service.name || '': <br /><br />'' || notice.content as content from notice

join activation

on activation.activation_id = notice.activation_id

join circulation

on circulation.circulation_id = activation.circulation_id

join service

on service.service_id = activation.service_id

where circulation.instance_id = [INSTANCE_ID]

and activation.service_parent_id = [SERVICE_ID]');
REM INSERTING into CAMAC_DEV.A_PHP
SET DEFINE OFF;
Insert into CAMAC_DEV.A_PHP (ACTION_ID,PHP_CLASS) values (27,'CircEnd');
Insert into CAMAC_DEV.A_PHP (ACTION_ID,PHP_CLASS) values (7,'DossierNR');
Insert into CAMAC_DEV.A_PHP (ACTION_ID,PHP_CLASS) values (26,'CircEnd');
Insert into CAMAC_DEV.A_PHP (ACTION_ID,PHP_CLASS) values (69,'DossierNR');
REM INSERTING into CAMAC_DEV.A_PROPOSAL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.A_SAVEPDF
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.A_VALIDATE
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.BUTTON
SET DEFINE OFF;
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (4,2,'Freigeben',null,null,0,1);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (2,1,'Erstellen',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (3,2,'Speichern',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (5,4,'Speichern',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (64,106,'Erstellen',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (22,23,'Antwort speichern',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (23,23,'Antwort senden',null,null,0,1);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (24,23,'Retrieve NOtice',null,null,0,2);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (65,107,'Speichern',null,null,0,0);
REM INSERTING into CAMAC_DEV.B_GROUP_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.B_GROUP_ACL (BUTTON_ID,GROUP_ID,INSTANCE_STATE_ID) values (23,23,23);
REM INSERTING into CAMAC_DEV.B_ROLE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,6,1);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,21);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (4,6,21);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (24,4,23);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (64,1001,1);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (65,1001,22);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (65,1001,24);
REM INSERTING into CAMAC_DEV.B_SERVICE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.B_SERVICE_ACL (BUTTON_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,22);
Insert into CAMAC_DEV.B_SERVICE_ACL (BUTTON_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,24);
Insert into CAMAC_DEV.B_SERVICE_ACL (BUTTON_ID,SERVICE_ID,INSTANCE_STATE_ID) values (22,2,23);
Insert into CAMAC_DEV.B_SERVICE_ACL (BUTTON_ID,SERVICE_ID,INSTANCE_STATE_ID) values (22,21,23);
Insert into CAMAC_DEV.B_SERVICE_ACL (BUTTON_ID,SERVICE_ID,INSTANCE_STATE_ID) values (24,2,23);
REM INSERTING into CAMAC_DEV.B_USER_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.CHAPTER
SET DEFINE OFF;
Insert into CAMAC_DEV.CHAPTER (CHAPTER_ID,NAME,DESCRIPTION,JAVASCRIPT) values (1,'Personendaten','Alle Daten der beteiligten Personen',null);
Insert into CAMAC_DEV.CHAPTER (CHAPTER_ID,NAME,DESCRIPTION,JAVASCRIPT) values (2,'Generell','Alle Allgemeinen Daten wie Leitbehorde, Dossier-NR',null);
Insert into CAMAC_DEV.CHAPTER (CHAPTER_ID,NAME,DESCRIPTION,JAVASCRIPT) values (3,'Erstellung','Die Daten, die im ersten Schritt erledigt werden',null);
Insert into CAMAC_DEV.CHAPTER (CHAPTER_ID,NAME,DESCRIPTION,JAVASCRIPT) values (21,'Objektdaten',null,null);
REM INSERTING into CAMAC_DEV.CHAPTER_PAGE
SET DEFINE OFF;
Insert into CAMAC_DEV.CHAPTER_PAGE (CHAPTER_ID,PAGE_ID,SORT) values (1,1,2);
Insert into CAMAC_DEV.CHAPTER_PAGE (CHAPTER_ID,PAGE_ID,SORT) values (2,1,1);
Insert into CAMAC_DEV.CHAPTER_PAGE (CHAPTER_ID,PAGE_ID,SORT) values (3,1,0);
Insert into CAMAC_DEV.CHAPTER_PAGE (CHAPTER_ID,PAGE_ID,SORT) values (21,1,3);
REM INSERTING into CAMAC_DEV.CHAPTER_PAGE_GROUP_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,1001,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,1001,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,1001,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,1001,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,1001,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,1001,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,1001,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,1);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,4,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,6,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,6,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,6,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,6,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,6,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,6,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,6,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,1001,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,1001,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,1001,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,1001,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,1001,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,1001,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,1001,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,1,6,1);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,1,1001,1);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,4,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,4,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,4,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,4,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,4,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,4,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,4,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,6,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,6,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,6,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,6,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,6,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,6,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,6,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,1001,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,1001,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,1001,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,1001,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,1001,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,1001,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,1001,27);
REM INSERTING into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID,PAGE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (1,1,1,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID,PAGE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (1,1,1,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID,PAGE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (1,1,1,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID,PAGE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (1,1,1,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID,PAGE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (1,1,1,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID,PAGE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (1,1,1,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID,PAGE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (1,1,1,27);
REM INSERTING into CAMAC_DEV.CHAPTER_PAGE_USER_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.CIRCULATION
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.CIRCULATION_ANSWER
SET DEFINE OFF;
Insert into CAMAC_DEV.CIRCULATION_ANSWER (CIRCULATION_ANSWER_ID,CIRCULATION_TYPE_ID,CIRCULATION_ANSWER_TYPE_ID,NAME,SORT) values (1,1,1,'Nein',0);
Insert into CAMAC_DEV.CIRCULATION_ANSWER (CIRCULATION_ANSWER_ID,CIRCULATION_TYPE_ID,CIRCULATION_ANSWER_TYPE_ID,NAME,SORT) values (2,1,1,'Ja',1);
Insert into CAMAC_DEV.CIRCULATION_ANSWER (CIRCULATION_ANSWER_ID,CIRCULATION_TYPE_ID,CIRCULATION_ANSWER_TYPE_ID,NAME,SORT) values (3,1,1,'Ja mit Auflagen',2);
Insert into CAMAC_DEV.CIRCULATION_ANSWER (CIRCULATION_ANSWER_ID,CIRCULATION_TYPE_ID,CIRCULATION_ANSWER_TYPE_ID,NAME,SORT) values (4,1,1,'Fachstelle nicht betroffen',3);
REM INSERTING into CAMAC_DEV.CIRCULATION_ANSWER_TYPE
SET DEFINE OFF;
Insert into CAMAC_DEV.CIRCULATION_ANSWER_TYPE (CIRCULATION_ANSWER_TYPE_ID,NAME) values (1,'Response');
Insert into CAMAC_DEV.CIRCULATION_ANSWER_TYPE (CIRCULATION_ANSWER_TYPE_ID,NAME) values (2,'Delay');
REM INSERTING into CAMAC_DEV.CIRCULATION_LOG
SET DEFINE OFF;
Insert into CAMAC_DEV.CIRCULATION_LOG (CIRCULATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (1,1,21,'i',to_date('23-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.CIRCULATION_LOG (CIRCULATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (2,2,21,'i',to_date('26-MAY-14','DD-MON-RR'));
REM INSERTING into CAMAC_DEV.CIRCULATION_REASON
SET DEFINE OFF;
Insert into CAMAC_DEV.CIRCULATION_REASON (CIRCULATION_REASON_ID,CIRCULATION_TYPE_ID,NAME,SORT) values (1,1,'Verfugung',0);
Insert into CAMAC_DEV.CIRCULATION_REASON (CIRCULATION_REASON_ID,CIRCULATION_TYPE_ID,NAME,SORT) values (2,1,'Stellungnahme',1);
REM INSERTING into CAMAC_DEV.CIRCULATION_STATE
SET DEFINE OFF;
Insert into CAMAC_DEV.CIRCULATION_STATE (CIRCULATION_STATE_ID,NAME,SORT) values (1,'RUN',0);
Insert into CAMAC_DEV.CIRCULATION_STATE (CIRCULATION_STATE_ID,NAME,SORT) values (2,'OK',1);
REM INSERTING into CAMAC_DEV.CIRCULATION_TYPE
SET DEFINE OFF;
Insert into CAMAC_DEV.CIRCULATION_TYPE (CIRCULATION_TYPE_ID,NAME) values (1,'Main circulation');
REM INSERTING into CAMAC_DEV.FORM
SET DEFINE OFF;
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (21,1,'Voreinfrage mit kantonaler Beteiligung',null);
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (41,1,'BGBB / Apparzellierung',null);
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (42,1,'Internes Mitberichtsverfahren',null);
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (43,1,'Internes Genehmigungsverfahren',null);
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (44,1,'Baubewilligungsverfahren mit kantonaler Beteiligung',null);
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (45,1,'Plangenehmigungsverfahren nach Luftfahrtgesetz',null);
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (46,1,'Plangenehmigungsverfahren fur militarische Bauten',null);
Insert into CAMAC_DEV.FORM (FORM_ID,FORM_STATE_ID,NAME,DESCRIPTION) values (47,1,'Baubewilligungsverfahren ohne kantonale Beteiligung',null);
REM INSERTING into CAMAC_DEV.FORM_STATE
SET DEFINE OFF;
Insert into CAMAC_DEV.FORM_STATE (FORM_STATE_ID,NAME) values (1,'Published');
Insert into CAMAC_DEV.FORM_STATE (FORM_STATE_ID,NAME) values (2,'Not published');
REM INSERTING into CAMAC_DEV.GLOSSARY_CATEGORY
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.GLOSSARY_SENTENCE
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV."GROUP"
SET DEFINE OFF;
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (1,1,null,'Admin');
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (2,2,null,'Guest');
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (21,1001,null,'Koordinationsstelle Baugesuche');
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (22,6,null,'Gemeinde Altdorf');
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (23,4,2,'Amt fur Umwelt');
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (24,6,null,'Urner Oberland');
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (41,4,null,'Amter');
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (42,4,21,'Subfachstelle AFU');
REM INSERTING into CAMAC_DEV.GROUP_LOCATION
SET DEFINE OFF;
Insert into CAMAC_DEV.GROUP_LOCATION (GROUP_ID,LOCATION_ID) values (22,1);
REM INSERTING into CAMAC_DEV.INSTANCE
SET DEFINE OFF;
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (42,21,44,21,22,to_date('27-MAY-14','DD-MON-RR'),to_date('27-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (43,21,44,21,22,to_date('02-JUN-14','DD-MON-RR'),to_date('02-JUN-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (32,23,44,21,22,to_date('23-MAY-14','DD-MON-RR'),to_date('23-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (41,24,44,21,22,to_date('26-MAY-14','DD-MON-RR'),to_date('27-MAY-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (62,21,44,21,22,to_date('22-JUL-14','DD-MON-RR'),to_date('22-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (63,21,44,21,22,to_date('22-JUL-14','DD-MON-RR'),to_date('22-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (64,21,44,21,22,to_date('22-JUL-14','DD-MON-RR'),to_date('22-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (65,21,44,21,22,to_date('22-JUL-14','DD-MON-RR'),to_date('22-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (82,21,44,21,22,to_date('23-JUL-14','DD-MON-RR'),to_date('23-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (83,21,44,21,22,to_date('23-JUL-14','DD-MON-RR'),to_date('23-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (102,22,44,21,22,to_date('24-JUL-14','DD-MON-RR'),to_date('24-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (122,22,44,21,22,to_date('28-JUL-14','DD-MON-RR'),to_date('28-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (142,21,44,21,22,to_date('29-JUL-14','DD-MON-RR'),to_date('29-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (162,21,44,21,22,to_date('30-JUL-14','DD-MON-RR'),to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (163,22,43,21,21,to_date('30-JUL-14','DD-MON-RR'),to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (164,22,43,21,21,to_date('30-JUL-14','DD-MON-RR'),to_date('30-JUL-14','DD-MON-RR'));
REM INSERTING into CAMAC_DEV.INSTANCE_DEMO
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.INSTANCE_DEMO_LOG
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.INSTANCE_FORM_PDF
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.INSTANCE_GUEST
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.INSTANCE_LOCATION
SET DEFINE OFF;
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,32);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,41);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,42);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,43);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,65);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,83);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,102);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,122);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,142);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,162);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (2,82);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (10,164);
REM INSERTING into CAMAC_DEV.INSTANCE_LOCATION_LOG
SET DEFINE OFF;
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (1,to_date('23-MAY-14','DD-MON-RR'),21,'i',4,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (2,to_date('23-MAY-14','DD-MON-RR'),21,'i',5,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (3,to_date('23-MAY-14','DD-MON-RR'),21,'i',6,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (4,to_date('23-MAY-14','DD-MON-RR'),21,'i',7,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (5,to_date('23-MAY-14','DD-MON-RR'),21,'i',1,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (6,to_date('23-MAY-14','DD-MON-RR'),21,'i',2,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (7,to_date('23-MAY-14','DD-MON-RR'),21,'i',3,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (8,to_date('23-MAY-14','DD-MON-RR'),21,'i',4,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (9,to_date('23-MAY-14','DD-MON-RR'),21,'i',5,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (10,to_date('23-MAY-14','DD-MON-RR'),21,'i',6,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (11,to_date('23-MAY-14','DD-MON-RR'),21,'i',7,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (12,to_date('23-MAY-14','DD-MON-RR'),21,'i',8,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (13,to_date('23-MAY-14','DD-MON-RR'),21,'i',9,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (14,to_date('23-MAY-14','DD-MON-RR'),21,'i',10,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (15,to_date('23-MAY-14','DD-MON-RR'),21,'i',11,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (16,to_date('23-MAY-14','DD-MON-RR'),21,'i',12,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (17,to_date('23-MAY-14','DD-MON-RR'),21,'i',13,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (18,to_date('23-MAY-14','DD-MON-RR'),21,'i',14,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (19,to_date('23-MAY-14','DD-MON-RR'),21,'i',15,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (20,to_date('23-MAY-14','DD-MON-RR'),21,'i',16,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (21,to_date('23-MAY-14','DD-MON-RR'),21,'i',17,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (22,to_date('23-MAY-14','DD-MON-RR'),21,'i',18,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (23,to_date('23-MAY-14','DD-MON-RR'),21,'i',19,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (24,to_date('23-MAY-14','DD-MON-RR'),21,'i',20,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (25,to_date('23-MAY-14','DD-MON-RR'),21,'i',21,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (26,to_date('23-MAY-14','DD-MON-RR'),21,'i',22,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (27,to_date('23-MAY-14','DD-MON-RR'),21,'i',23,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (28,to_date('23-MAY-14','DD-MON-RR'),21,'i',24,'INSTANCE_ID',2,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (29,to_date('23-MAY-14','DD-MON-RR'),21,'i',25,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (30,to_date('23-MAY-14','DD-MON-RR'),21,'i',26,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (31,to_date('23-MAY-14','DD-MON-RR'),21,'i',27,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (32,to_date('23-MAY-14','DD-MON-RR'),21,'i',28,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (33,to_date('23-MAY-14','DD-MON-RR'),21,'i',29,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (34,to_date('23-MAY-14','DD-MON-RR'),21,'i',30,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (35,to_date('23-MAY-14','DD-MON-RR'),21,'i',31,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (36,to_date('23-MAY-14','DD-MON-RR'),21,'i',32,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (41,to_date('26-MAY-14','DD-MON-RR'),21,'i',41,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (42,to_date('27-MAY-14','DD-MON-RR'),21,'i',42,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (43,to_date('02-JUN-14','DD-MON-RR'),21,'i',43,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (62,to_date('22-JUL-14','DD-MON-RR'),21,'i',65,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (82,to_date('23-JUL-14','DD-MON-RR'),21,'i',82,'INSTANCE_ID',2,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (83,to_date('23-JUL-14','DD-MON-RR'),21,'i',83,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (102,to_date('24-JUL-14','DD-MON-RR'),21,'i',102,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (122,to_date('28-JUL-14','DD-MON-RR'),21,'i',122,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (142,to_date('29-JUL-14','DD-MON-RR'),21,'i',142,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (162,to_date('30-JUL-14','DD-MON-RR'),21,'i',162,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (163,to_date('30-JUL-14','DD-MON-RR'),21,'i',164,'INSTANCE_ID',10,'LOCATION_ID');
REM INSERTING into CAMAC_DEV.INSTANCE_LOG
SET DEFINE OFF;
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (1,to_date('22-MAY-14','DD-MON-RR'),21,'i',1);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (2,to_date('23-MAY-14','DD-MON-RR'),21,'i',2);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (3,to_date('23-MAY-14','DD-MON-RR'),21,'i',3);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (4,to_date('23-MAY-14','DD-MON-RR'),21,'i',4);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (5,to_date('23-MAY-14','DD-MON-RR'),21,'i',5);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (6,to_date('23-MAY-14','DD-MON-RR'),21,'i',6);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (7,to_date('23-MAY-14','DD-MON-RR'),21,'i',7);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (8,to_date('23-MAY-14','DD-MON-RR'),21,'i',1);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (9,to_date('23-MAY-14','DD-MON-RR'),21,'i',2);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (10,to_date('23-MAY-14','DD-MON-RR'),21,'i',3);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (11,to_date('23-MAY-14','DD-MON-RR'),21,'i',4);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (12,to_date('23-MAY-14','DD-MON-RR'),21,'i',5);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (13,to_date('23-MAY-14','DD-MON-RR'),21,'i',6);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (14,to_date('23-MAY-14','DD-MON-RR'),21,'i',7);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (15,to_date('23-MAY-14','DD-MON-RR'),21,'i',8);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (16,to_date('23-MAY-14','DD-MON-RR'),21,'i',9);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (17,to_date('23-MAY-14','DD-MON-RR'),21,'i',10);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (18,to_date('23-MAY-14','DD-MON-RR'),21,'i',11);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (19,to_date('23-MAY-14','DD-MON-RR'),21,'i',12);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (20,to_date('23-MAY-14','DD-MON-RR'),21,'i',13);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (21,to_date('23-MAY-14','DD-MON-RR'),21,'i',14);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (22,to_date('23-MAY-14','DD-MON-RR'),21,'i',15);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (23,to_date('23-MAY-14','DD-MON-RR'),21,'i',16);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (24,to_date('23-MAY-14','DD-MON-RR'),21,'i',17);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (25,to_date('23-MAY-14','DD-MON-RR'),21,'i',18);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (26,to_date('23-MAY-14','DD-MON-RR'),21,'i',19);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (27,to_date('23-MAY-14','DD-MON-RR'),21,'i',20);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (28,to_date('23-MAY-14','DD-MON-RR'),21,'i',21);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (29,to_date('23-MAY-14','DD-MON-RR'),21,'i',22);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (30,to_date('23-MAY-14','DD-MON-RR'),21,'i',23);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (31,to_date('23-MAY-14','DD-MON-RR'),21,'i',24);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (32,to_date('23-MAY-14','DD-MON-RR'),21,'i',25);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (33,to_date('23-MAY-14','DD-MON-RR'),21,'i',26);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (34,to_date('23-MAY-14','DD-MON-RR'),21,'i',27);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (35,to_date('23-MAY-14','DD-MON-RR'),21,'i',28);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (36,to_date('23-MAY-14','DD-MON-RR'),21,'i',29);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (37,to_date('23-MAY-14','DD-MON-RR'),21,'i',30);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (38,to_date('23-MAY-14','DD-MON-RR'),21,'i',31);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (39,to_date('23-MAY-14','DD-MON-RR'),21,'i',32);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (40,to_date('23-MAY-14','DD-MON-RR'),21,'u',32);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (41,to_date('23-MAY-14','DD-MON-RR'),21,'u',32);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (42,to_date('26-MAY-14','DD-MON-RR'),21,'i',41);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (43,to_date('26-MAY-14','DD-MON-RR'),21,'u',41);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (44,to_date('26-MAY-14','DD-MON-RR'),21,'u',41);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (45,to_date('26-MAY-14','DD-MON-RR'),21,'u',41);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (46,to_date('27-MAY-14','DD-MON-RR'),21,'u',41);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (47,to_date('27-MAY-14','DD-MON-RR'),21,'u',41);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (48,to_date('27-MAY-14','DD-MON-RR'),21,'i',42);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (49,to_date('02-JUN-14','DD-MON-RR'),21,'i',43);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (66,to_date('22-JUL-14','DD-MON-RR'),21,'i',62);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (67,to_date('22-JUL-14','DD-MON-RR'),21,'i',63);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (68,to_date('22-JUL-14','DD-MON-RR'),21,'i',64);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (69,to_date('22-JUL-14','DD-MON-RR'),21,'i',65);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (86,to_date('23-JUL-14','DD-MON-RR'),21,'i',82);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (87,to_date('23-JUL-14','DD-MON-RR'),21,'i',83);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (106,to_date('24-JUL-14','DD-MON-RR'),21,'i',102);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (107,to_date('24-JUL-14','DD-MON-RR'),21,'u',102);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (126,to_date('28-JUL-14','DD-MON-RR'),21,'i',122);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (127,to_date('28-JUL-14','DD-MON-RR'),21,'u',122);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (128,to_date('28-JUL-14','DD-MON-RR'),21,'u',122);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (129,to_date('29-JUL-14','DD-MON-RR'),21,'i',142);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (146,to_date('30-JUL-14','DD-MON-RR'),21,'i',162);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (147,to_date('30-JUL-14','DD-MON-RR'),21,'i',163);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (148,to_date('30-JUL-14','DD-MON-RR'),21,'i',164);
REM INSERTING into CAMAC_DEV.INSTANCE_RESOURCE
SET DEFINE OFF;
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (1,'newform',22,44,'Baugesuch mit kantonaler Beteiligung erstellen',null,null,null,0,0);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (2,'editformpage',23,44,'Dossier bearbeiten',null,'/form/main.phtml',null,0,0);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (3,'formpage',23,44,'Dossier anschauen',null,null,null,0,1);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (4,'editformpage',24,44,'Dossier bearbeiten','Dossier bearbeiten fur Koordinationsstelle','/form/main.phtml',null,0,0);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (5,'formpage',1,44,'Dossier anschauen','Anschauen ist immer erlaubt',null,null,0,0);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (105,'editcirculation',24,44,'Zirkulation',null,null,null,0,3);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (21,'circulation',24,44,'Zirkulation anschauen',null,null,null,0,2);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (22,'formpage',41,44,'Baugesuch ansehen',null,null,null,0,0);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (23,'editnotice',41,44,'Stellungnahme',null,null,null,0,1);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (24,'circulation',41,44,'Beteiligte Fachstellen',null,null,null,0,2);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (106,'newform',22,43,'Internes Genehmigungsverfahren erstellen',null,null,null,0,1);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (107,'editformpage',24,43,'Dossier bearbeiten','Dossier bearbeiten fur Internes Genehmigungsverfahren','/form/main.phtml',null,0,4);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (125,'editcirculation',24,43,'Zirkulation','Zirkulation fur internes Genehmigungsverfahren',null,null,0,5);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (46,'documents',23,44,'Dokumente',null,null,null,0,2);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (85,'formpage',24,44,'Dossier anschauen',null,null,null,0,1);
REM INSERTING into CAMAC_DEV.INSTANCE_RESOURCE_ACTION
SET DEFINE OFF;
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','copydata');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','location');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','save');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','copydata');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','location');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','save');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','copydata');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','location');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','save');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','save');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editletter','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','circulationtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','notice');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','save');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','copydata');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','location');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpage','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','copydata');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','location');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','copydata');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','location');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formwizard','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('history','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('history','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('history','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('history','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('letter','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('letter','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('letter','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('letter','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('letter','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('letter','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('letter','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','copydata');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','location');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','save');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','wsgeocode');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','checkquery');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','email');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','formtransition');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','php');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','proposal');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','savepdf');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','validate');
Insert into CAMAC_DEV.INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','wsgeocode');
REM INSERTING into CAMAC_DEV.INSTANCE_STATE
SET DEFINE OFF;
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (1,'new',0);
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (21,'comm',2);
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (22,'ext',3);
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (23,'circ',4);
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (24,'redac',5);
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (25,'done',6);
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (26,'arch',7);
Insert into CAMAC_DEV.INSTANCE_STATE (INSTANCE_STATE_ID,NAME,SORT) values (27,'del',8);
REM INSERTING into CAMAC_DEV.IR_ALLFORMPAGES
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_CIRCULATION
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_CIRCULATION (INSTANCE_RESOURCE_ID,CIRCULATION_TYPE_ID,SERVICE_ID,DRAFT_CIRCULATION_ANSWER_ID,SHOW_NOTICE,SHOW_HISTORY,SHOW_ALL_CHILDREN,READ_NOTICE_TEMPLATE,PDF_CLASS,SERVICE_TO_BE_INTERPRETED) values (21,1,1,null,2,1,1,null,null,null);
Insert into CAMAC_DEV.IR_CIRCULATION (INSTANCE_RESOURCE_ID,CIRCULATION_TYPE_ID,SERVICE_ID,DRAFT_CIRCULATION_ANSWER_ID,SHOW_NOTICE,SHOW_HISTORY,SHOW_ALL_CHILDREN,READ_NOTICE_TEMPLATE,PDF_CLASS,SERVICE_TO_BE_INTERPRETED) values (24,1,1,null,2,0,0,null,null,null);
REM INSERTING into CAMAC_DEV.IR_EDITCIRCULATION
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_EDITCIRCULATION (INSTANCE_RESOURCE_ID,CIRCULATION_TYPE_ID,DRAFT_CIRCULATION_ANSWER_ID,SHOW_NOTICE,ADD_TEMPLATE,ADD_ACTIVATION_TEMPLATE,READ_NOTICE_TEMPLATE,PDF_CLASS,DEFAULT_CIRCULATION_NAME,SINGLE_CIRCULATION) values (125,1,null,0,null,null,null,null,null,0);
Insert into CAMAC_DEV.IR_EDITCIRCULATION (INSTANCE_RESOURCE_ID,CIRCULATION_TYPE_ID,DRAFT_CIRCULATION_ANSWER_ID,SHOW_NOTICE,ADD_TEMPLATE,ADD_ACTIVATION_TEMPLATE,READ_NOTICE_TEMPLATE,PDF_CLASS,DEFAULT_CIRCULATION_NAME,SINGLE_CIRCULATION) values (105,1,null,0,null,null,null,null,null,0);
REM INSERTING into CAMAC_DEV.IR_EDITCIRCULATION_SG
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_EDITCIRCULATION_SG (IR_EDITCIRCULATION_SG_ID,INSTANCE_RESOURCE_ID,SERVICE_GROUP_ID,LOCALIZED) values (2,105,2,0);
Insert into CAMAC_DEV.IR_EDITCIRCULATION_SG (IR_EDITCIRCULATION_SG_ID,INSTANCE_RESOURCE_ID,SERVICE_GROUP_ID,LOCALIZED) values (22,125,2,1);
REM INSERTING into CAMAC_DEV.IR_EDITFORMPAGE
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_EDITFORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (2,1,null);
Insert into CAMAC_DEV.IR_EDITFORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (4,1,null);
Insert into CAMAC_DEV.IR_EDITFORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (107,1,null);
REM INSERTING into CAMAC_DEV.IR_EDITFORMPAGES
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_EDITLETTER
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_EDITLETTER_ANSWER
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_EDITNOTICE
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_EDITNOTICE (INSTANCE_RESOURCE_ID,CIRCULATION_TYPE_ID,EDITABLE_AFTER_DEADLINE,PDF_CLASS,EDIT_NOTICE_TEMPLATE) values (23,1,0,null,null);
REM INSERTING into CAMAC_DEV.IR_FORMERROR
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_FORMPAGE
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_FORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (3,1,null);
Insert into CAMAC_DEV.IR_FORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (5,1,null);
Insert into CAMAC_DEV.IR_FORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (22,1,null);
Insert into CAMAC_DEV.IR_FORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (85,1,null);
REM INSERTING into CAMAC_DEV.IR_FORMPAGES
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_FORMWIZARD
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_GROUP_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_GROUP_ACL (INSTANCE_RESOURCE_ID,GROUP_ID,INSTANCE_STATE_ID) values (22,41,23);
Insert into CAMAC_DEV.IR_GROUP_ACL (INSTANCE_RESOURCE_ID,GROUP_ID,INSTANCE_STATE_ID) values (23,41,23);
REM INSERTING into CAMAC_DEV.IR_LETTER
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_NEWFORM
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_NEWFORM (INSTANCE_RESOURCE_ID,INSTANCE_STATE_ID) values (1,21);
Insert into CAMAC_DEV.IR_NEWFORM (INSTANCE_RESOURCE_ID,INSTANCE_STATE_ID) values (106,22);
REM INSERTING into CAMAC_DEV.IR_PAGE
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.IR_ROLE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,6,1);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,6,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,1);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (4,1001,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (4,1001,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,1001,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,1001,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,1001,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,1001,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,1001,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,1001,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,1001,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1001,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1001,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1001,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1001,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1001,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1001,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (22,4,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (22,4,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (23,4,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (23,4,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,4,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,4,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,4,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,4,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,4,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,4,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,4,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,6,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,6,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,6,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,6,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,6,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,6,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (46,6,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,1001,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,1001,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,1001,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,1001,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,1001,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,1001,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,1001,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,1001,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,1001,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,1001,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,1001,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,1001,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (106,1001,1);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (107,1001,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (107,1001,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (125,1001,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (125,1001,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (125,1001,24);
REM INSERTING into CAMAC_DEV.IR_SERVICE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,21);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,23);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,24);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,25);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,26);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (5,1,27);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (24,2,23);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (24,2,24);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (85,1,21);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (85,1,22);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (85,1,23);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (85,1,24);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (85,1,25);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (85,1,26);
Insert into CAMAC_DEV.IR_SERVICE_ACL (INSTANCE_RESOURCE_ID,SERVICE_ID,INSTANCE_STATE_ID) values (85,1,27);
REM INSERTING into CAMAC_DEV.IR_USER_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.LETTER
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.LETTER_IMAGE
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.LOCATION
SET DEFINE OFF;
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (1,1,'1201',null,null,'Altdorf','Altdorf (UR)',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (2,2,'1202',null,null,'Andermatt','Andermatt',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (5,5,'1205',null,null,'Burglen','Burglen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (6,6,'1206',null,null,'Erstfeld','Erstfeld',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (7,7,'1207',null,null,'Fluelen','Fluelen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (8,8,'1208',null,null,'Goschenen','Goschenen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (9,9,'1209',null,null,'Gurtnellen','Gurtnellen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (10,10,'1210',null,null,'Hospental','Hospental',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (11,11,'1211',null,null,'Isenthal','Isenthal',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (12,12,'1212',null,null,'Realp','Realp',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (13,13,'1213',null,null,'Schattdorf','Schattdorf',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (14,14,'1214',null,null,'Seedorf','Seedorf (UR)',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (15,15,'1215',null,null,'Seelisberg','Seelisberg',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (16,16,'1216',null,null,'Silenen','Silenen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (19,19,'1219',null,null,'Unterschachen','Unterschachen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (20,20,'1220',null,null,'Wassen','Wassen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (3,3,'1203',null,null,'Attinghausen','Attinghausen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (4,4,'1204',null,null,'Bauen','Bauen',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (17,17,'1217',null,null,'Sisikon','Sisikon',null,null);
Insert into CAMAC_DEV.LOCATION (LOCATION_ID,COMMUNAL_CANTONAL_NUMBER,COMMUNAL_FEDERAL_NUMBER,DISTRICT_NUMBER,SECTION_NUMBER,NAME,COMMUNE_NAME,DISTRICT_NAME,SECTION_NAME) values (18,18,'1218',null,null,'Spiringen','Spiringen',null,null);
REM INSERTING into CAMAC_DEV.MAPPING
SET DEFINE OFF;
Insert into CAMAC_DEV.MAPPING (MAPPING_ID,TABLE_NAME,COLUMN_NAME) values (1,'ANSWER','ANSWER');
Insert into CAMAC_DEV.MAPPING (MAPPING_ID,TABLE_NAME,COLUMN_NAME) values (21,'INSTANCE_LOCATION','LOCATION_ID');
REM INSERTING into CAMAC_DEV.NOTICE
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.NOTICE_IMAGE
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.NOTICE_LOG
SET DEFINE OFF;
Insert into CAMAC_DEV.NOTICE_LOG (NOTICE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (1,to_date('26-MAY-14','DD-MON-RR'),21,'i',1,'NOTICE_TYPE_ID',2,'ACTIVATION_ID');
Insert into CAMAC_DEV.NOTICE_LOG (NOTICE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (2,to_date('26-MAY-14','DD-MON-RR'),21,'i',2,'NOTICE_TYPE_ID',2,'ACTIVATION_ID');
Insert into CAMAC_DEV.NOTICE_LOG (NOTICE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (3,to_date('04-JUN-14','DD-MON-RR'),21,'i',1,'NOTICE_TYPE_ID',1,'ACTIVATION_ID');
Insert into CAMAC_DEV.NOTICE_LOG (NOTICE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (4,to_date('04-JUN-14','DD-MON-RR'),21,'u',1,'NOTICE_TYPE_ID',1,'ACTIVATION_ID');
REM INSERTING into CAMAC_DEV.NOTICE_TYPE
SET DEFINE OFF;
Insert into CAMAC_DEV.NOTICE_TYPE (NOTICE_TYPE_ID,CIRCULATION_TYPE_ID,NAME) values (1,1,'Mitteilungen an die Gemeindebaubehorde');
Insert into CAMAC_DEV.NOTICE_TYPE (NOTICE_TYPE_ID,CIRCULATION_TYPE_ID,NAME) values (2,1,'Mitteilungen an die Koordinationsstelle');
REM INSERTING into CAMAC_DEV.PAGE
SET DEFINE OFF;
Insert into CAMAC_DEV.PAGE (PAGE_ID,NAME,DESCRIPTION,JAVASCRIPT) values (1,'Hauptformular',null,null);
REM INSERTING into CAMAC_DEV.PAGE_ANSWER_ACTIVATION
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.PAGE_FORM
SET DEFINE OFF;
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,21,1,1,0);
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,41,1,1,0);
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,42,1,1,0);
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,43,3,1,0);
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,44,3,1,0);
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,45,1,1,0);
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,46,1,1,0);
Insert into CAMAC_DEV.PAGE_FORM (PAGE_ID,FORM_ID,PAGE_FORM_MODE_ID,PAGE_FORM_GROUP_ID,SORT) values (1,47,1,1,0);
REM INSERTING into CAMAC_DEV.PAGE_FORM_GROUP
SET DEFINE OFF;
Insert into CAMAC_DEV.PAGE_FORM_GROUP (PAGE_FORM_GROUP_ID,NAME) values (1,'Group 1');
Insert into CAMAC_DEV.PAGE_FORM_GROUP (PAGE_FORM_GROUP_ID,NAME) values (21,'test');
REM INSERTING into CAMAC_DEV.PAGE_FORM_GROUP_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.PAGE_FORM_MODE
SET DEFINE OFF;
Insert into CAMAC_DEV.PAGE_FORM_MODE (PAGE_FORM_MODE_ID,NAME) values (1,'Additional');
Insert into CAMAC_DEV.PAGE_FORM_MODE (PAGE_FORM_MODE_ID,NAME) values (2,'Activable');
Insert into CAMAC_DEV.PAGE_FORM_MODE (PAGE_FORM_MODE_ID,NAME) values (3,'Required');
REM INSERTING into CAMAC_DEV.PAGE_FORM_ROLE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,1);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,21);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,22);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,23);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,24);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,25);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,26);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,1001,27);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,1);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,21);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,22);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,23);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,24);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,25);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,26);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,27);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,1001,21);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,1001,22);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,1001,23);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,1001,24);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,1001,25);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,1001,26);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,1001,27);
REM INSERTING into CAMAC_DEV.PAGE_FORM_SERVICE_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.PAGE_FORM_USER_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.PROPOSAL_ACTIVATION
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.QUESTION
SET DEFINE OFF;
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (1,2,1,null,'Mitteilungen',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (2,3,1,1,'Gemeinde','Die Auswahl der Gemeinde... muss wohl noch eingeschrankt werden!',null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (3,6,1,null,'Es werden keine physischen Unterlagen zugestellt',null,null,null,'0');
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (4,7,1,null,'Die Gemeindebaubehorde wunscht, dass das vorliegende Gesuch hinsichtlich folgender Fachbereiche durch die zustandigen kantonalen Fachstellen gepruft wird',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (5,3,1,null,'Leitbehorde','hier einschranken fur die entsprechenden User',null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (6,2,1,null,'Dossiernummer',null,'$(''[QUESTION]'').attr(''readonly'', ''readonly'')',null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (7,9,null,null,'test',null,null,null,'select * from dual;');
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (21,8,1,null,'Datei-Test',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (22,4,1,null,'Grundnutzungen gemass rechtsgultigem Nutzungsplan',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (23,1,1,null,'Name / Vorname',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (41,9,null,null,'Gesuchsteller',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (61,1,1,null,'Adresse',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (62,1,1,null,'PLZ','Postleitzahl',null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (63,1,1,null,'Ort',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (64,1,1,null,'Telefon Festnetz',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (65,1,1,null,'Telefon Mobile',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (66,1,1,null,'Email',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (67,1,1,null,'Fax',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (68,6,1,null,'Rechnungsadresse identisch GesuchstellerIn',null,null,null,'0');
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (69,1,1,null,'Rechnungsadresse',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (70,9,null,null,'ProjektverfasserIn',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (71,1,1,null,'Name / Vorname',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (72,1,1,null,'Adresse',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (73,1,1,null,'PLZ','Postleitzahl',null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (74,1,1,null,'Ort',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (75,1,1,null,'Telefon Festnetz',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (76,1,1,null,'Telefon Mobile',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (77,1,1,null,'Email',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (78,1,1,null,'Fax',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (79,6,1,null,'ProjektverfasserIn identisch GesuchstellerIn',null,null,null,'0');
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (80,6,1,null,'GrundeigentumerIn identisch GesuchstellerIn',null,null,null,'0');
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (81,9,null,null,'GrundeigentumerIn',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (82,1,1,null,'Name / Vorname',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (83,1,1,null,'Adresse',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (84,1,1,null,'PLZ','Postleitzahl',null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (85,1,1,null,'Ort',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (86,1,1,null,'Telefon Festnetz',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (87,1,1,null,'Telefon Mobile',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (88,1,1,null,'Email',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (89,1,1,null,'Fax',null,null,'/^\+?[\d ]+$/',null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (90,9,null,null,'Bauplatz',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (91,1,1,null,'Parzellennummer',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (92,1,1,null,'Baurechtsnummer','(z.B. bei Bauten und Anlagen auf Gebiet der Korporationen Uri und Ursern)',null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (93,1,1,null,'Strasse/Flurname',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (94,4,1,null,'Uberlagerte Nutzungsplaninhalte gemass rechtsgutigem Zonenplan',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (95,4,1,null,'Orientierende Nutzungsplaninhalte',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (96,9,null,null,'Vorhaben',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (97,4,1,null,'Vorhaben',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (98,1,1,null,'Andere Vorhaben',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (99,4,1,null,'Nutzung',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (100,1,1,null,'Andere Nutzung',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (101,1,1,null,'Umbauter Raum nach SIA 416',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (102,1,1,null,'Baukosten (Gebaudekosten)',null,null,null,null);
Insert into CAMAC_DEV.QUESTION (QUESTION_ID,QUESTION_TYPE_ID,MAPPING_ID,ANSWER_QUERY_ID,NAME,DESCRIPTION,JAVASCRIPT,REGEX,DEFAULT_ANSWER) values (103,1,1,null,'Bemerkungen',null,null,null,null);
REM INSERTING into CAMAC_DEV.QUESTION_CHAPTER
SET DEFINE OFF;
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (1,2,0,1,1);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (2,2,0,1,0);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (3,2,0,1,2);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (4,2,0,1,3);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (5,2,0,1,4);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (6,2,0,1,5);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (41,1,0,1,0);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (2,3,1,1,1);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (5,3,1,1,2);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (22,21,0,1,4);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (23,1,1,1,1);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (61,1,1,1,2);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (62,1,1,1,3);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (63,1,1,1,4);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (64,1,0,1,5);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (65,1,0,1,6);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (66,1,0,1,7);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (67,1,0,1,8);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (68,1,0,1,9);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (69,1,0,1,10);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (70,1,0,1,11);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (71,1,0,1,13);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (72,1,0,1,14);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (73,1,0,1,15);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (74,1,0,1,16);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (75,1,0,1,17);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (76,1,0,1,18);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (77,1,0,1,19);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (78,1,0,1,20);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (79,1,0,1,12);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (80,1,0,1,22);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (81,1,0,1,21);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (82,1,0,1,23);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (83,1,0,1,24);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (84,1,0,1,25);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (85,1,0,1,26);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (86,1,0,1,27);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (87,1,0,1,28);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (88,1,0,1,29);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (89,1,0,1,30);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (90,21,0,1,0);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (91,21,0,1,1);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (92,21,0,1,2);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (93,21,0,1,3);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (94,21,0,1,5);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (95,21,0,1,6);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (96,21,0,1,7);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (97,21,0,1,8);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (98,21,0,1,9);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (99,21,0,1,10);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (100,21,0,1,11);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (101,21,0,1,12);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (102,21,0,1,13);
Insert into CAMAC_DEV.QUESTION_CHAPTER (QUESTION_ID,CHAPTER_ID,REQUIRED,ITEM,SORT) values (103,21,0,1,14);
REM INSERTING into CAMAC_DEV.QUESTION_CHAPTER_GROUP_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.QUESTION_CHAPTER_ROLE_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.QUESTION_CHAPTER_SERVICE_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.QUESTION_CHAPTER_USER_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.QUESTION_TYPE
SET DEFINE OFF;
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (1,'Text');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (2,'Textarea');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (3,'Select');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (4,'Multi select');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (5,'Radiobox');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (6,'Checkbox');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (7,'Multi checkbox');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (8,'File');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (9,'Note');
Insert into CAMAC_DEV.QUESTION_TYPE (QUESTION_TYPE_ID,NAME) values (10,'SQLNote');
REM INSERTING into CAMAC_DEV."RESOURCE"
SET DEFINE OFF;
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (1,'list','Dossierliste',null,null,null,0,5);
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (62,'list','Pendenzenliste Ende','Liste fur Koordinationsstellen',null,null,0,3);
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (22,'page','Dossier erstellen','Landepage fur Gemeinden, links zum Dossiers erstellen','/global/home.phtml',null,0,7);
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (23,'list','Pendenzenliste start','Start Pendenzenliste fur Gemeinden',null,null,0,1);
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (24,'list','Pendenzenliste start','Pendenzenliste start fur Koord',null,null,0,2);
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (41,'list','Pendenzenliste','Pendenzenliste fur Amter',null,null,0,0);
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (42,'search','Dossiersuche',null,'/global/search.phtml',null,0,6);
Insert into CAMAC_DEV."RESOURCE" (RESOURCE_ID,AVAILABLE_RESOURCE_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (63,'list','Pendenzenliste Ende','Liste fur Gemeinden',null,null,0,4);
REM INSERTING into CAMAC_DEV.ROLE
SET DEFINE OFF;
Insert into CAMAC_DEV.ROLE (ROLE_ID,ROLE_PARENT_ID,NAME) values (1,null,'Admin');
Insert into CAMAC_DEV.ROLE (ROLE_ID,ROLE_PARENT_ID,NAME) values (2,null,'Guest');
Insert into CAMAC_DEV.ROLE (ROLE_ID,ROLE_PARENT_ID,NAME) values (3,null,'Pilot');
Insert into CAMAC_DEV.ROLE (ROLE_ID,ROLE_PARENT_ID,NAME) values (4,null,'Service');
Insert into CAMAC_DEV.ROLE (ROLE_ID,ROLE_PARENT_ID,NAME) values (5,null,'Architect');
Insert into CAMAC_DEV.ROLE (ROLE_ID,ROLE_PARENT_ID,NAME) values (6,null,'Gemeinde');
Insert into CAMAC_DEV.ROLE (ROLE_ID,ROLE_PARENT_ID,NAME) values (1001,null,'Koordinationsstelle');
REM INSERTING into CAMAC_DEV.R_FORMLIST
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.R_GROUP_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.R_GROUP_ACL (RESOURCE_ID,GROUP_ID) values (41,23);
REM INSERTING into CAMAC_DEV.R_LIST
SET DEFINE OFF;
Insert into CAMAC_DEV.R_LIST (RESOURCE_ID,QUERY) values (1,'select 

	"INSTANCE_ID",

	"DOSSIERNR"."ANSWER" as "DOSSIER_NR",

	"FORM"."NAME"        as "FORM",

	"LOCATION"."NAME"    as "COMMUNITY",

	"USER"."USERNAME"        AS "USER",

	GET_STATE_NAME_BY_ID("INSTANCE"."INSTANCE_STATE_ID") AS "STATUS"

FROM "INSTANCE"

JOIN "INSTANCE_LOCATION" ON (

		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"

)

JOIN "LOCATION" ON (

		"INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"

)

join "ANSWER"  "DOSSIERNR" ON (

		"DOSSIERNR"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"

		AND

		"DOSSIERNR"."QUESTION_ID" = 6

		AND

		"DOSSIERNR"."CHAPTER_ID" = 2

		AND

		"DOSSIERNR"."ITEM" = 1

	)

join "FORM" ON (

	"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"

)

JOIN "USER" ON (

		"INSTANCE"."USER_ID" = "USER"."USER_ID"

)');
Insert into CAMAC_DEV.R_LIST (RESOURCE_ID,QUERY) values (23,'SELECT

	"INSTANCE"."INSTANCE_ID"   AS "INSTANCE_ID",

	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",

	"FORM"."NAME"              AS "FORM",

	"LOCATION"."NAME"          AS "COMMUNITY",

	"USER"."USERNAME"          AS "USER",

	"ANSWER_PETITION"."ANSWER" AS "PETITION",

	"ANSWER_INTENT"."ANSWER"   AS "INTENT",

	"ANSWER_CITY"."ANSWER"     AS "CITY",

	"INSTANCE_STATE"."NAME"    AS "STATE"

FROM

	"INSTANCE"

JOIN

	"INSTANCE_LOCATION" ON (

		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"

	)

JOIN 

	"LOCATION" ON (

	 "INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"

	)

JOIN

	FORM ON (

		"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"

)

JOIN

	"USER" ON (

		"INSTANCE"."USER_ID" = "USER"."USER_ID"

)

JOIN

	"ANSWER" "ANSWER_DOK_NR" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"

		AND

		"ANSWER_DOK_NR"."QUESTION_ID" = 6

		AND

		"ANSWER_DOK_NR"."CHAPTER_ID" = 2

		AND

		"ANSWER_DOK_NR"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_PETITION" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_PETITION"."INSTANCE_ID"

		AND

		"ANSWER_PETITION"."QUESTION_ID" = 23

		AND

		"ANSWER_PETITION"."CHAPTER_ID" = 1

		AND

		"ANSWER_PETITION"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_INTENT" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_INTENT"."INSTANCE_ID"

		AND

		"ANSWER_INTENT"."QUESTION_ID" = 97

		AND

		"ANSWER_INTENT"."CHAPTER_ID" = 21

		AND

		"ANSWER_INTENT"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_CITY" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_CITY"."INSTANCE_ID"

		AND

		"ANSWER_CITY"."QUESTION_ID" = 63

		AND

		"ANSWER_CITY"."CHAPTER_ID" = 1

		AND

		"ANSWER_CITY"."ITEM" = 1

	)

JOIN 

	"INSTANCE_STATE" ON (

	"INSTANCE_STATE"."NAME" = ''comm''

)

JOIN

	"GROUP_LOCATION" ON (

	 	"GROUP_LOCATION"."GROUP_ID" = [GROUP_ID]

	)

WHERE

	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"

	AND

	"GROUP_LOCATION"."LOCATION_ID" = "INSTANCE_LOCATION"."LOCATION_ID"');
Insert into CAMAC_DEV.R_LIST (RESOURCE_ID,QUERY) values (24,'SELECT

	"INSTANCE"."INSTANCE_ID"   AS "INSTANCE_ID",

	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",

	"FORM"."NAME"              AS "FORM",

	"LOCATION"."NAME"          AS "COMMUNITY",

	"USER"."USERNAME"          AS "USER",

	"ANSWER_PETITION"."ANSWER" AS "PETITION",

	"ANSWER_INTENT"."ANSWER"   AS "INTENT",

	"ANSWER_CITY"."ANSWER"     AS "CITY",

	"INSTANCE_STATE"."NAME"    AS "STATE"

FROM

	"INSTANCE"

JOIN

	"INSTANCE_LOCATION" ON (

		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"

	)

JOIN 

	"LOCATION" ON (

	 "INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"

	)

JOIN

	FORM ON (

		"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"

)

JOIN

	"USER" ON (

		"INSTANCE"."USER_ID" = "USER"."USER_ID"

)

JOIN

	"ANSWER" "ANSWER_DOK_NR" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"

		AND

		"ANSWER_DOK_NR"."QUESTION_ID" = 6

		AND

		"ANSWER_DOK_NR"."CHAPTER_ID" = 2

		AND

		"ANSWER_DOK_NR"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_PETITION" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_PETITION"."INSTANCE_ID"

		AND

		"ANSWER_PETITION"."QUESTION_ID" = 23

		AND

		"ANSWER_PETITION"."CHAPTER_ID" = 1

		AND

		"ANSWER_PETITION"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_INTENT" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_INTENT"."INSTANCE_ID"

		AND

		"ANSWER_INTENT"."QUESTION_ID" = 97

		AND

		"ANSWER_INTENT"."CHAPTER_ID" = 21

		AND

		"ANSWER_INTENT"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_CITY" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_CITY"."INSTANCE_ID"

		AND

		"ANSWER_CITY"."QUESTION_ID" = 63

		AND

		"ANSWER_CITY"."CHAPTER_ID" = 1

		AND

		"ANSWER_CITY"."ITEM" = 1

	)

JOIN 

	"INSTANCE_STATE" ON (

	"INSTANCE_STATE"."NAME" = ''ext''

)

WHERE

	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"');
Insert into CAMAC_DEV.R_LIST (RESOURCE_ID,QUERY) values (41,'SELECT

	"INSTANCE"."INSTANCE_ID"   AS "INSTANCE_ID",

	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",

	"FORM"."NAME"              AS "FORM",

	"LOCATION"."NAME"          AS "COMMUNITY",

	"USER"."USERNAME"          AS "USER",

	"ANSWER_PETITION"."ANSWER" AS "PETITION",

	"ANSWER_INTENT"."ANSWER"   AS "INTENT",

	"ANSWER_CITY"."ANSWER"     AS "CITY",

	"INSTANCE_STATE"."NAME"    AS "STATE"

FROM

	"INSTANCE"

JOIN

	"INSTANCE_LOCATION" ON (

		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"

	)

JOIN 

	"LOCATION" ON (

	 "INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"

	)

JOIN

	FORM ON (

		"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"

)

JOIN

	"USER" ON (

		"INSTANCE"."USER_ID" = "USER"."USER_ID"

)

JOIN

	"ANSWER" "ANSWER_DOK_NR" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"

		AND

		"ANSWER_DOK_NR"."QUESTION_ID" = 6

		AND

		"ANSWER_DOK_NR"."CHAPTER_ID" = 2

		AND

		"ANSWER_DOK_NR"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_PETITION" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_PETITION"."INSTANCE_ID"

		AND

		"ANSWER_PETITION"."QUESTION_ID" = 23

		AND

		"ANSWER_PETITION"."CHAPTER_ID" = 1

		AND

		"ANSWER_PETITION"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_INTENT" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_INTENT"."INSTANCE_ID"

		AND

		"ANSWER_INTENT"."QUESTION_ID" = 97

		AND

		"ANSWER_INTENT"."CHAPTER_ID" = 21

		AND

		"ANSWER_INTENT"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_CITY" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_CITY"."INSTANCE_ID"

		AND

		"ANSWER_CITY"."QUESTION_ID" = 63

		AND

		"ANSWER_CITY"."CHAPTER_ID" = 1

		AND

		"ANSWER_CITY"."ITEM" = 1

	)

JOIN 

	"INSTANCE_STATE" ON (

	"INSTANCE_STATE"."NAME" = ''circ''

)

JOIN

	"GROUP_LOCATION" ON (

	 	"GROUP_LOCATION"."GROUP_ID" = [GROUP_ID]

	)

WHERE

	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"

	AND

	"GROUP_LOCATION"."LOCATION_ID" = "INSTANCE_LOCATION"."LOCATION_ID"');
Insert into CAMAC_DEV.R_LIST (RESOURCE_ID,QUERY) values (62,'SELECT

	"INSTANCE"."INSTANCE_ID"   AS "INSTANCE_ID",

	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",

	"FORM"."NAME"              AS "FORM",

	"LOCATION"."NAME"          AS "COMMUNITY",

	"USER"."USERNAME"          AS "USER",

	"ANSWER_PETITION"."ANSWER" AS "PETITION",

	"ANSWER_INTENT"."ANSWER"   AS "INTENT",

	"ANSWER_CITY"."ANSWER"     AS "CITY",

	"INSTANCE_STATE"."NAME"    AS "STATE"

FROM

	"INSTANCE"

JOIN

	"INSTANCE_LOCATION" ON (

		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"

	)

JOIN 

	"LOCATION" ON (

	 "INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"

	)

JOIN

	FORM ON (

		"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"

)

JOIN

	"USER" ON (

		"INSTANCE"."USER_ID" = "USER"."USER_ID"

)

JOIN

	"ANSWER" "ANSWER_DOK_NR" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"

		AND

		"ANSWER_DOK_NR"."QUESTION_ID" = 6

		AND

		"ANSWER_DOK_NR"."CHAPTER_ID" = 2

		AND

		"ANSWER_DOK_NR"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_PETITION" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_PETITION"."INSTANCE_ID"

		AND

		"ANSWER_PETITION"."QUESTION_ID" = 23

		AND

		"ANSWER_PETITION"."CHAPTER_ID" = 1

		AND

		"ANSWER_PETITION"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_INTENT" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_INTENT"."INSTANCE_ID"

		AND

		"ANSWER_INTENT"."QUESTION_ID" = 97

		AND

		"ANSWER_INTENT"."CHAPTER_ID" = 21

		AND

		"ANSWER_INTENT"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_CITY" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_CITY"."INSTANCE_ID"

		AND

		"ANSWER_CITY"."QUESTION_ID" = 63

		AND

		"ANSWER_CITY"."CHAPTER_ID" = 1

		AND

		"ANSWER_CITY"."ITEM" = 1

	)

JOIN 

	"INSTANCE_STATE" ON (

	"INSTANCE_STATE"."NAME" = ''redac''

)

WHERE

	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"');
Insert into CAMAC_DEV.R_LIST (RESOURCE_ID,QUERY) values (63,'SELECT

	"INSTANCE"."INSTANCE_ID"   AS "INSTANCE_ID",

	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",

	"FORM"."NAME"              AS "FORM",

	"LOCATION"."NAME"          AS "COMMUNITY",

	"USER"."USERNAME"          AS "USER",

	"ANSWER_PETITION"."ANSWER" AS "PETITION",

	"ANSWER_INTENT"."ANSWER"   AS "INTENT",

	"ANSWER_CITY"."ANSWER"     AS "CITY",

	"INSTANCE_STATE"."NAME"    AS "STATE"

FROM

	"INSTANCE"

JOIN

	"INSTANCE_LOCATION" ON (

		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"

	)

JOIN 

	"LOCATION" ON (

	 "INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"

	)

JOIN

	FORM ON (

		"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"

)

JOIN

	"USER" ON (

		"INSTANCE"."USER_ID" = "USER"."USER_ID"

)

JOIN

	"ANSWER" "ANSWER_DOK_NR" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"

		AND

		"ANSWER_DOK_NR"."QUESTION_ID" = 6

		AND

		"ANSWER_DOK_NR"."CHAPTER_ID" = 2

		AND

		"ANSWER_DOK_NR"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_PETITION" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_PETITION"."INSTANCE_ID"

		AND

		"ANSWER_PETITION"."QUESTION_ID" = 23

		AND

		"ANSWER_PETITION"."CHAPTER_ID" = 1

		AND

		"ANSWER_PETITION"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_INTENT" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_INTENT"."INSTANCE_ID"

		AND

		"ANSWER_INTENT"."QUESTION_ID" = 97

		AND

		"ANSWER_INTENT"."CHAPTER_ID" = 21

		AND

		"ANSWER_INTENT"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_CITY" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_CITY"."INSTANCE_ID"

		AND

		"ANSWER_CITY"."QUESTION_ID" = 63

		AND

		"ANSWER_CITY"."CHAPTER_ID" = 1

		AND

		"ANSWER_CITY"."ITEM" = 1

	)

JOIN 

	"INSTANCE_STATE" ON (

	"INSTANCE_STATE"."NAME" = ''done''

)

JOIN

	"GROUP_LOCATION" ON (

	 	"GROUP_LOCATION"."GROUP_ID" = [GROUP_ID]

	)

WHERE

	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"

	AND

	"GROUP_LOCATION"."LOCATION_ID" = "INSTANCE_LOCATION"."LOCATION_ID"');
REM INSERTING into CAMAC_DEV.R_LIST_COLUMN
SET DEFINE OFF;
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (1,1,'INSTANCE_ID','INSTANCE_ID',0);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (21,23,'INSTANCE_ID','ID',0);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (34,24,'INSTANCE_ID','ID',0);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (35,24,'DOSSIER_NR','Dossier-Nr.',1);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (36,24,'FORM','Verfahren',2);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (37,24,'COMMUNITY','Gemeinde',3);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (38,24,'USER','Ersteller',4);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (41,41,'INSTANCE_ID','INSTANCE_ID',0);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (42,41,'STATE','STATE',8);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (79,62,'INSTANCE_ID','ID',0);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (30,23,'DOSSIER_NR','Dossier-Nr.',1);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (31,23,'FORM','Verfahren',2);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (32,23,'COMMUNITY','Gemeinde',3);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (33,23,'USER','Ersteller',4);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (44,1,'DOSSIER_NR','DOSSIER_NR',1);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (45,1,'FORM','FORM',2);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (46,1,'COMMUNITY','COMMUNITY',3);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (47,1,'USER','USER',4);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (49,1,'STATUS','STATUS',5);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (64,24,'INTENT','Vorhaben',6);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (65,24,'PETITION','Gesuchsteller',5);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (66,24,'CITY','Ort',7);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (67,24,'STATE','Status',8);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (68,23,'PETITION','Gesuchsteller',5);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (69,23,'INTENT','Vorhaben',6);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (70,23,'CITY','Ort',7);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (71,23,'STATE','Status',8);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (72,41,'DOSSIER_NR','DOSSIER_NR',1);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (73,41,'FORM','FORM',2);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (74,41,'COMMUNITY','COMMUNITY',3);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (75,41,'USER','USER',4);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (76,41,'PETITION','PETITION',5);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (77,41,'INTENT','INTENT',6);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (78,41,'CITY','CITY',7);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (80,62,'DOSSIER_NR','Dossier-Nr.',1);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (81,62,'FORM','Verfahren',2);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (82,62,'COMMUNITY','Gemeinde',3);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (83,62,'USER','Ersteller',4);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (84,62,'PETITION','Gesuchsteller',5);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (85,62,'INTENT','Vorhaben',6);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (86,62,'CITY','Ort',7);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (87,62,'STATE','Status',8);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (88,63,'INSTANCE_ID','ID',0);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (89,63,'DOSSIER_NR','Dossier-Nr.',1);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (90,63,'FORM','Verfahren',2);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (91,63,'COMMUNITY','Gemeinde',3);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (92,63,'USER','Ersteller',4);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (93,63,'PETITION','Gesuchsteller',5);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (94,63,'INTENT','Vorhaben',6);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (95,63,'CITY','Ort',7);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (96,63,'STATE','Status',8);
REM INSERTING into CAMAC_DEV.R_ROLE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (1,4);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (1,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (1,1001);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (22,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (22,1001);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (23,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (24,1001);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (42,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (42,1001);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (62,1001);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (63,6);
REM INSERTING into CAMAC_DEV.R_SEARCH
SET DEFINE OFF;
Insert into CAMAC_DEV.R_SEARCH (RESOURCE_ID,RESULT_TEMPLATE,QUERY) values (42,null,'select 

	"INSTANCE_ID",

	"DOSSIERNR"."ANSWER" as "DOSSIER_NR",

	"FORM"."NAME"        as "FORM",

	"LOCATION"."NAME"    as "COMMUNITY",

	"USER"."USERNAME"        AS "USER",

	GET_STATE_NAME_BY_ID("INSTANCE"."INSTANCE_STATE_ID") AS "STATUS"

FROM "INSTANCE"

JOIN "INSTANCE_LOCATION" ON (

		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"

)

JOIN "LOCATION" ON (

		"INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"

)

join "ANSWER"  "DOSSIERNR" ON (

		"DOSSIERNR"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"

		AND

		"DOSSIERNR"."QUESTION_ID" = 6

		AND

		"DOSSIERNR"."CHAPTER_ID" = 2

		AND

		"DOSSIERNR"."ITEM" = 1

	)

join "FORM" ON (

	"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"

)

JOIN "USER" ON (

		"INSTANCE"."USER_ID" = "USER"."USER_ID"

)');
REM INSERTING into CAMAC_DEV.R_SEARCH_COLUMN
SET DEFINE OFF;
Insert into CAMAC_DEV.R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (1,42,'INSTANCE_ID','INSTANCE_ID',0);
Insert into CAMAC_DEV.R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (2,42,'DOSSIER_NR','DOSSIER_NR',1);
Insert into CAMAC_DEV.R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (3,42,'FORM','FORM',2);
Insert into CAMAC_DEV.R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (4,42,'COMMUNITY','COMMUNITY',3);
Insert into CAMAC_DEV.R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (5,42,'USER','USER',4);
Insert into CAMAC_DEV.R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (6,42,'STATUS','STATUS',5);
REM INSERTING into CAMAC_DEV.R_SEARCH_FILTER
SET DEFINE OFF;
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (1,42,6,'dossiernumber','Dossiernummer','"DOSSIERNR"."ANSWER" = ?',0);
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (2,42,2,'community','Gemeinde','instance.instance_id in (select instance_location.instance_id from instance_location where instance_location.location_id = ?)',0);
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (3,42,null,'parcelnr','Parzellennummber','1 = 1',0);
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (4,42,null,'status','Status','"INSTANCE"."INSTANCE_STATE_ID" = get_state_id_by_name(?)',0);
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (5,42,null,'fulltext','Volltext','"INSTANCE"."INSTANCE_ID" IN (

 	SELECT

  		INSTANCE_ID

  	FROM

  		ANSWER

  	WHERE

  		lower(ANSWER) LIKE lower(?)

 )',3);
REM INSERTING into CAMAC_DEV.R_SERVICE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.R_SERVICE_ACL (RESOURCE_ID,SERVICE_ID) values (24,1);
Insert into CAMAC_DEV.R_SERVICE_ACL (RESOURCE_ID,SERVICE_ID) values (41,2);
Insert into CAMAC_DEV.R_SERVICE_ACL (RESOURCE_ID,SERVICE_ID) values (41,21);
Insert into CAMAC_DEV.R_SERVICE_ACL (RESOURCE_ID,SERVICE_ID) values (62,1);
REM INSERTING into CAMAC_DEV.R_USER_ACL
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.SERVICE
SET DEFINE OFF;
Insert into CAMAC_DEV.SERVICE (SERVICE_ID,SERVICE_GROUP_ID,SERVICE_PARENT_ID,NAME,DESCRIPTION,SORT) values (1,1,null,'Koordination Baugesuche','Ein Mitglied der kantonaler Koordinationsstelle fur Baugesuche',2);
Insert into CAMAC_DEV.SERVICE (SERVICE_ID,SERVICE_GROUP_ID,SERVICE_PARENT_ID,NAME,DESCRIPTION,SORT) values (2,2,null,'AfU','Amt fur Umwelt',0);
Insert into CAMAC_DEV.SERVICE (SERVICE_ID,SERVICE_GROUP_ID,SERVICE_PARENT_ID,NAME,DESCRIPTION,SORT) values (3,2,null,'AfG','AfG (Gewasserschutz?)',1);
Insert into CAMAC_DEV.SERVICE (SERVICE_ID,SERVICE_GROUP_ID,SERVICE_PARENT_ID,NAME,DESCRIPTION,SORT) values (21,2,2,'Subfachstelle AFU','Subfachstelle AFU',1);
REM INSERTING into CAMAC_DEV.SERVICE_ANSWER_ACTIVATION
SET DEFINE OFF;
REM INSERTING into CAMAC_DEV.SERVICE_GROUP
SET DEFINE OFF;
Insert into CAMAC_DEV.SERVICE_GROUP (SERVICE_GROUP_ID,NAME) values (1,'Koordinationsstelle');
Insert into CAMAC_DEV.SERVICE_GROUP (SERVICE_GROUP_ID,NAME) values (2,'Kantonale Amter');
REM INSERTING into CAMAC_DEV."USER"
SET DEFINE OFF;
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (1,'admin','10602b62c0f171f626e3d64046c27567','Administrator','Static',null,null,0,'en',to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (2,'guest',null,'Guest','Static',null,null,0,'en',to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (21,'pwa','c1784faf0e31b8d206c503a861906278','Walker','Paul',null,null,0,'de',to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (41,'altdorf1','2cac92f07ee422172c0c8dde938ec5e1','Jemand','Altdorf',null,null,0,'de',null);
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (42,'afu1','51b6006db9e292fb1acb270af8dc48af','jemand','Amt fur Umwelt',null,null,0,'de',null);
REM INSERTING into CAMAC_DEV.USER_GROUP
SET DEFINE OFF;
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (1,1,1);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (2,2,1);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (21,21,1);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (41,22,1);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (21,22,0);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (42,23,1);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (21,24,0);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (21,23,0);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (21,41,0);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (42,41,0);
Insert into CAMAC_DEV.USER_GROUP (USER_ID,GROUP_ID,DEFAULT_GROUP) values (21,42,0);
-- Unable to render INDEX DDL for object CAMAC_DEV.ATTACHMENT_PK with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX ATTACHMENT_PK ON ATTACHMENT (ATTACHMENT_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.GLOSSARY_CATEGORY_PK with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX GLOSSARY_CATEGORY_PK ON GLOSSARY_CATEGORY (GLOSSARY_CATEGORY_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.GLOSSARY_SENTENCE_PK with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX GLOSSARY_SENTENCE_PK ON GLOSSARY_SENTENCE (GLOSSARY_SENTENCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007795 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007795 ON A_VALIDATE (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007797 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007797 ON IR_PAGE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007803 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007803 ON A_SAVEPDF (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007806 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007806 ON IR_FORMERROR (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007814 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007814 ON INSTANCE_FORM_PDF (INSTANCE_FORM_PDF_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007819 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007819 ON IR_FORMWIZARD (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007823 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007823 ON INSTANCE_GUEST (INSTANCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007827 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007827 ON A_NOTICE (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007833 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007833 ON A_COPYDATA_MAPPING (A_COPYDATA_MAPPING_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007835 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007835 ON A_COPYDATA (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007838 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007838 ON A_CIRCULATIONTRANSITION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007848 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007848 ON INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007853 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007853 ON A_LOCATION_QC (A_LOCATION_QC_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007855 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007855 ON A_LOCATION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007858 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007858 ON INSTANCE_LOCATION (LOCATION_ID ASC, INSTANCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007867 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007867 ON NOTICE_IMAGE (NOTICE_IMAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007872 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007872 ON A_PROPOSAL (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007879 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007879 ON PROPOSAL_ACTIVATION (PROPOSAL_ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007883 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007883 ON AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID ASC, ACTION_NAME ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007887 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007887 ON AR_ACTION (AVAILABLE_RESOURCE_ID ASC, ACTION_NAME ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007894 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007894 ON CIRCULATION_LOG (CIRCULATION_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007904 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007904 ON NOTICE_LOG (NOTICE_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007908 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007908 ON IR_EDITNOTICE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007912 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007912 ON NOTICE (NOTICE_TYPE_ID ASC, ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007917 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007917 ON CIRCULATION (CIRCULATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007921 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007921 ON NOTICE_TYPE (NOTICE_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007924 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007924 ON IR_ALLFORMPAGES (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007932 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007932 ON LETTER_IMAGE (LETTER_IMAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007934 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007934 ON IR_LETTER (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007941 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007941 ON ACTIVATION_LOG (ACTIVATION_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007955 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007955 ON ANSWER_LOG (ANSWER_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007962 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007962 ON INSTANCE_LOG (INSTANCE_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007970 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007970 ON LETTER (INSTANCE_ID ASC, INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007978 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007978 ON IR_CIRCULATION (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007982 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007982 ON IR_EDITLETTER_ANSWER (IR_EDITLETTER_ANSWER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007984 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007984 ON IR_EDITLETTER (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007989 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007989 ON IR_EDITCIRCULATION_SG (IR_EDITCIRCULATION_SG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007992 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007992 ON CIRCULATION_TYPE (CIRCULATION_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C007997 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C007997 ON IR_EDITCIRCULATION (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008006 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008006 ON ACTIVATION (ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008012 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008012 ON R_SEARCH_COLUMN (R_SEARCH_COLUMN_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008018 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008018 ON R_LIST_COLUMN (R_LIST_COLUMN_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008021 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008021 ON A_FORMTRANSITION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008024 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008024 ON A_PHP (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008027 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008027 ON A_CHECKQUERY (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008033 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008033 ON ANSWER (INSTANCE_ID ASC, QUESTION_ID ASC, CHAPTER_ID ASC, ITEM ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008041 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008041 ON INSTANCE (INSTANCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008044 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008044 ON IR_NEWFORM (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008047 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008047 ON INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID ASC, AVAILABLE_ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008054 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008054 ON PAGE_ANSWER_ACTIVATION (PAGE_ANSWER_ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008061 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008061 ON A_EMAIL (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008068 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008068 ON ACTION (ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008071 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008071 ON AVAILABLE_ACTION (AVAILABLE_ACTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008074 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008074 ON IR_FORMPAGE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008076 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008076 ON IR_FORMPAGES (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008078 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008078 ON IR_EDITFORMPAGES (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008081 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008081 ON R_LIST (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008085 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008085 ON IR_SERVICE_ACL (INSTANCE_RESOURCE_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008089 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008089 ON IR_USER_ACL (INSTANCE_RESOURCE_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008093 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008093 ON IR_GROUP_ACL (INSTANCE_RESOURCE_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008097 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008097 ON IR_ROLE_ACL (INSTANCE_RESOURCE_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008105 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008105 ON INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008109 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008109 ON AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008113 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008113 ON B_SERVICE_ACL (BUTTON_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008117 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008117 ON B_USER_ACL (BUTTON_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008121 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008121 ON B_GROUP_ACL (BUTTON_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008125 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008125 ON B_ROLE_ACL (BUTTON_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008128 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008128 ON R_SERVICE_ACL (RESOURCE_ID ASC, SERVICE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008131 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008131 ON R_USER_ACL (RESOURCE_ID ASC, USER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008134 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008134 ON R_GROUP_ACL (RESOURCE_ID ASC, GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008137 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008137 ON R_ROLE_ACL (RESOURCE_ID ASC, ROLE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008142 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008142 ON QUESTION_CHAPTER_SERVICE_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008147 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008147 ON QUESTION_CHAPTER_USER_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008152 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008152 ON QUESTION_CHAPTER_GROUP_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008157 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008157 ON CHAPTER_PAGE_SERVICE_ACL (CHAPTER_ID ASC, PAGE_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008162 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008162 ON CHAPTER_PAGE_USER_ACL (CHAPTER_ID ASC, PAGE_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008167 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008167 ON CHAPTER_PAGE_GROUP_ACL (CHAPTER_ID ASC, PAGE_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008172 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008172 ON PAGE_FORM_SERVICE_ACL (PAGE_ID ASC, FORM_ID ASC, SERVICE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008177 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008177 ON PAGE_FORM_USER_ACL (PAGE_ID ASC, FORM_ID ASC, USER_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008182 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008182 ON PAGE_FORM_GROUP_ACL (PAGE_ID ASC, FORM_ID ASC, GROUP_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008188 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008188 ON BUTTON (BUTTON_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008191 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008191 ON IR_EDITFORMPAGE (INSTANCE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008194 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008194 ON R_FORMLIST (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008200 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008200 ON "RESOURCE" (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008203 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008203 ON R_SEARCH (RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008207 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008207 ON AVAILABLE_RESOURCE (AVAILABLE_RESOURCE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008212 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008212 ON CIRCULATION_REASON (CIRCULATION_REASON_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008215 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008215 ON CIRCULATION_ANSWER_TYPE (CIRCULATION_ANSWER_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008221 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008221 ON CIRCULATION_ANSWER (CIRCULATION_ANSWER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008225 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008225 ON CIRCULATION_STATE (CIRCULATION_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008230 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008230 ON QUESTION_CHAPTER_ROLE_ACL (QUESTION_ID ASC, CHAPTER_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008235 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008235 ON CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID ASC, PAGE_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008240 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008240 ON PAGE_FORM_ROLE_ACL (PAGE_ID ASC, FORM_ID ASC, ROLE_ID ASC, INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008244 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008244 ON INSTANCE_STATE (INSTANCE_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008246 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008246 ON PAGE_FORM_GROUP (PAGE_FORM_GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008249 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008249 ON PAGE_FORM_MODE (PAGE_FORM_MODE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008256 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008256 ON SERVICE_ANSWER_ACTIVATION (SERVICE_ANSWER_ACTIVATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008259 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008259 ON SERVICE_GROUP (SERVICE_GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008263 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008263 ON MAPPING (MAPPING_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008266 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008266 ON QUESTION_TYPE (QUESTION_TYPE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008269 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008269 ON FORM_STATE (FORM_STATE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008275 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008275 ON ANSWER_LIST (ANSWER_LIST_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008279 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008279 ON ANSWER_QUERY (ANSWER_QUERY_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008284 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008284 ON PAGE_FORM (PAGE_ID ASC, FORM_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008288 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008288 ON CHAPTER_PAGE (CHAPTER_ID ASC, PAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008294 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008294 ON QUESTION_CHAPTER (QUESTION_ID ASC, CHAPTER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008298 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008298 ON QUESTION (QUESTION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008301 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008301 ON CHAPTER (CHAPTER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008304 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008304 ON PAGE (PAGE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008308 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008308 ON FORM (FORM_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008315 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008315 ON R_SEARCH_FILTER (R_SEARCH_FILTER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008318 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008318 ON GROUP_LOCATION (GROUP_ID ASC, LOCATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008320 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008320 ON LOCATION (LOCATION_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008324 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008324 ON USER_GROUP (USER_ID ASC, GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008329 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008329 ON SERVICE (SERVICE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008332 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008332 ON ROLE (ROLE_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008336 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008336 ON "GROUP" (GROUP_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008343 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008343 ON "USER" (USER_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008344 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008344 ON "USER" (USERNAME ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008558 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008558 ON INSTANCE_DEMO (INSTANCE_DEMO_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
-- Unable to render INDEX DDL for object CAMAC_DEV.SYS_C008566 with DBMS_METADATA attempting internal generator.
CREATE UNIQUE INDEX SYS_C008566 ON INSTANCE_DEMO_LOG (INSTANCE_DEMO_LOG_ID ASC) 
LOGGING 
TABLESPACE SYSTEM 
PCTFREE 10 
INITRANS 2 
STORAGE 
( 
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1 
  MAXEXTENTS UNLIMITED 
  FREELISTS 1 
  FREELIST GROUPS 1 
  BUFFER_POOL DEFAULT 
) 
NOPARALLEL
