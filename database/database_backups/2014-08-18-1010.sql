--------------------------------------------------------
--  File created - Monday-August-18-2014   
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
CREATE TABLE ACTION 
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
NOPARALLELALTER TABLE ACTION
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
CREATE TABLE ACTIVATION 
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
NOPARALLELALTER TABLE ACTIVATION
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
CREATE TABLE ACTIVATION_LOG 
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
)ALTER TABLE ACTIVATION_LOG
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.AIR_ACTION with DBMS_METADATA attempting internal generator.
CREATE TABLE AIR_ACTION 
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
NOPARALLELALTER TABLE AIR_ACTION
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
CREATE TABLE ANSWER 
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
NOPARALLELALTER TABLE ANSWER
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
CREATE TABLE ANSWER_LIST 
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
NOPARALLELALTER TABLE ANSWER_LIST
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
CREATE TABLE ANSWER_LOG 
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
)ALTER TABLE ANSWER_LOG
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.ANSWER_QUERY with DBMS_METADATA attempting internal generator.
CREATE TABLE ANSWER_QUERY 
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
NOCOMPRESSALTER TABLE ANSWER_QUERY
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.AR_ACTION with DBMS_METADATA attempting internal generator.
CREATE TABLE AR_ACTION 
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
NOPARALLELALTER TABLE AR_ACTION
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
CREATE TABLE ATTACHMENT 
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
, TYPE NUMBER NOT NULL 
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
NOPARALLELALTER TABLE ATTACHMENT
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
CREATE TABLE AVAILABLE_ACTION 
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
NOCOMPRESSALTER TABLE AVAILABLE_ACTION
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.AVAILABLE_INSTANCE_RESOURCE with DBMS_METADATA attempting internal generator.
CREATE TABLE AVAILABLE_INSTANCE_RESOURCE 
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
NOCOMPRESSALTER TABLE AVAILABLE_INSTANCE_RESOURCE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.AVAILABLE_RESOURCE with DBMS_METADATA attempting internal generator.
CREATE TABLE AVAILABLE_RESOURCE 
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
NOCOMPRESSALTER TABLE AVAILABLE_RESOURCE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.A_CHECKQUERY with DBMS_METADATA attempting internal generator.
CREATE TABLE A_CHECKQUERY 
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
NOPARALLELALTER TABLE A_CHECKQUERY
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
CREATE TABLE A_CIRCULATIONTRANSITION 
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
NOPARALLELALTER TABLE A_CIRCULATIONTRANSITION
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
CREATE TABLE A_COPYDATA 
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
NOPARALLELALTER TABLE A_COPYDATA
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
CREATE TABLE A_COPYDATA_MAPPING 
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
NOPARALLELALTER TABLE A_COPYDATA_MAPPING
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
CREATE TABLE A_EMAIL 
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
NOPARALLELALTER TABLE A_EMAIL
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
CREATE TABLE A_FORMTRANSITION 
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
NOPARALLELALTER TABLE A_FORMTRANSITION
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
CREATE TABLE A_LOCATION 
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
NOPARALLELALTER TABLE A_LOCATION
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
CREATE TABLE A_LOCATION_QC 
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
NOPARALLELALTER TABLE A_LOCATION_QC
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
CREATE TABLE A_NOTICE 
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
NOPARALLELALTER TABLE A_NOTICE
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
CREATE TABLE A_PHP 
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
NOPARALLELALTER TABLE A_PHP
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
CREATE TABLE A_PROPOSAL 
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
NOPARALLELALTER TABLE A_PROPOSAL
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
CREATE TABLE A_SAVEPDF 
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
NOPARALLELALTER TABLE A_SAVEPDF
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
CREATE TABLE A_VALIDATE 
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
NOPARALLELALTER TABLE A_VALIDATE
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
CREATE TABLE BUTTON 
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
NOPARALLELALTER TABLE BUTTON
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
CREATE TABLE B_GROUP_ACL 
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
NOPARALLELALTER TABLE B_GROUP_ACL
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
CREATE TABLE B_ROLE_ACL 
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
NOPARALLELALTER TABLE B_ROLE_ACL
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
CREATE TABLE B_SERVICE_ACL 
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
NOPARALLELALTER TABLE B_SERVICE_ACL
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
CREATE TABLE B_USER_ACL 
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
NOPARALLELALTER TABLE B_USER_ACL
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
CREATE TABLE CHAPTER 
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
NOCOMPRESSALTER TABLE CHAPTER
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.CHAPTER_PAGE with DBMS_METADATA attempting internal generator.
CREATE TABLE CHAPTER_PAGE 
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
NOPARALLELALTER TABLE CHAPTER_PAGE
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
CREATE TABLE CHAPTER_PAGE_GROUP_ACL 
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
NOPARALLELALTER TABLE CHAPTER_PAGE_GROUP_ACL
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
CREATE TABLE CHAPTER_PAGE_ROLE_ACL 
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
NOPARALLELALTER TABLE CHAPTER_PAGE_ROLE_ACL
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
CREATE TABLE CHAPTER_PAGE_SERVICE_ACL 
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
NOPARALLELALTER TABLE CHAPTER_PAGE_SERVICE_ACL
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
CREATE TABLE CHAPTER_PAGE_USER_ACL 
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
NOPARALLELALTER TABLE CHAPTER_PAGE_USER_ACL
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
CREATE TABLE CIRCULATION 
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
NOPARALLELALTER TABLE CIRCULATION
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
CREATE TABLE CIRCULATION_ANSWER 
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
NOPARALLELALTER TABLE CIRCULATION_ANSWER
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
CREATE TABLE CIRCULATION_ANSWER_TYPE 
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
NOCOMPRESSALTER TABLE CIRCULATION_ANSWER_TYPE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_LOG with DBMS_METADATA attempting internal generator.
CREATE TABLE CIRCULATION_LOG 
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
)ALTER TABLE CIRCULATION_LOG
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_REASON with DBMS_METADATA attempting internal generator.
CREATE TABLE CIRCULATION_REASON 
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
NOPARALLELALTER TABLE CIRCULATION_REASON
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
CREATE TABLE CIRCULATION_STATE 
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
NOCOMPRESSALTER TABLE CIRCULATION_STATE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.CIRCULATION_TYPE with DBMS_METADATA attempting internal generator.
CREATE TABLE CIRCULATION_TYPE 
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
NOCOMPRESSALTER TABLE CIRCULATION_TYPE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.FORM with DBMS_METADATA attempting internal generator.
CREATE TABLE FORM 
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
NOPARALLELALTER TABLE FORM
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
CREATE TABLE FORM_STATE 
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
NOCOMPRESSALTER TABLE FORM_STATE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.GLOSSARY_CATEGORY with DBMS_METADATA attempting internal generator.
CREATE TABLE GLOSSARY_CATEGORY 
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
NOCOMPRESSALTER TABLE GLOSSARY_CATEGORY
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.GLOSSARY_SENTENCE with DBMS_METADATA attempting internal generator.
CREATE TABLE GLOSSARY_SENTENCE 
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
NOCOMPRESSALTER TABLE GLOSSARY_SENTENCE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.GROUP with DBMS_METADATA attempting internal generator.
CREATE TABLE "GROUP" 
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
NOPARALLELALTER TABLE "GROUP"
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
CREATE TABLE GROUP_LOCATION 
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
NOPARALLELALTER TABLE GROUP_LOCATION
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
CREATE TABLE INSTANCE 
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
NOPARALLELALTER TABLE INSTANCE
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
CREATE TABLE INSTANCE_DEMO 
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
NOPARALLELALTER TABLE INSTANCE_DEMO
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
CREATE TABLE INSTANCE_DEMO_LOG 
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
)ALTER TABLE INSTANCE_DEMO_LOG
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_FORM_PDF with DBMS_METADATA attempting internal generator.
CREATE TABLE INSTANCE_FORM_PDF 
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
NOPARALLELALTER TABLE INSTANCE_FORM_PDF
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
CREATE TABLE INSTANCE_GUEST 
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
NOPARALLELALTER TABLE INSTANCE_GUEST
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
CREATE TABLE INSTANCE_LOCATION 
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
NOPARALLELALTER TABLE INSTANCE_LOCATION
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
CREATE TABLE INSTANCE_LOCATION_LOG 
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
)ALTER TABLE INSTANCE_LOCATION_LOG
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_LOG with DBMS_METADATA attempting internal generator.
CREATE TABLE INSTANCE_LOG 
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
)ALTER TABLE INSTANCE_LOG
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.INSTANCE_RESOURCE with DBMS_METADATA attempting internal generator.
CREATE TABLE INSTANCE_RESOURCE 
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
NOPARALLELALTER TABLE INSTANCE_RESOURCE
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
CREATE TABLE INSTANCE_RESOURCE_ACTION 
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
NOPARALLELALTER TABLE INSTANCE_RESOURCE_ACTION
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
CREATE TABLE INSTANCE_STATE 
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
NOCOMPRESSALTER TABLE INSTANCE_STATE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.IR_ALLFORMPAGES with DBMS_METADATA attempting internal generator.
CREATE TABLE IR_ALLFORMPAGES 
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
NOPARALLELALTER TABLE IR_ALLFORMPAGES
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
CREATE TABLE IR_CIRCULATION 
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
NOPARALLELALTER TABLE IR_CIRCULATION
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
CREATE TABLE IR_EDITCIRCULATION 
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
NOPARALLELALTER TABLE IR_EDITCIRCULATION
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
CREATE TABLE IR_EDITCIRCULATION_SG 
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
NOPARALLELALTER TABLE IR_EDITCIRCULATION_SG
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
CREATE TABLE IR_EDITFORMPAGE 
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
NOPARALLELALTER TABLE IR_EDITFORMPAGE
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
CREATE TABLE IR_EDITFORMPAGES 
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
NOPARALLELALTER TABLE IR_EDITFORMPAGES
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
CREATE TABLE IR_EDITLETTER 
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
NOPARALLELALTER TABLE IR_EDITLETTER
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
CREATE TABLE IR_EDITLETTER_ANSWER 
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
NOPARALLELALTER TABLE IR_EDITLETTER_ANSWER
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
CREATE TABLE IR_EDITNOTICE 
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
NOPARALLELALTER TABLE IR_EDITNOTICE
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
CREATE TABLE IR_FORMERROR 
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
NOPARALLELALTER TABLE IR_FORMERROR
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
CREATE TABLE IR_FORMPAGE 
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
NOPARALLELALTER TABLE IR_FORMPAGE
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
CREATE TABLE IR_FORMPAGES 
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
NOPARALLELALTER TABLE IR_FORMPAGES
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
CREATE TABLE IR_FORMWIZARD 
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
NOPARALLELALTER TABLE IR_FORMWIZARD
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
CREATE TABLE IR_GROUP_ACL 
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
NOPARALLELALTER TABLE IR_GROUP_ACL
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
CREATE TABLE IR_LETTER 
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
NOPARALLELALTER TABLE IR_LETTER
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
CREATE TABLE IR_NEWFORM 
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
NOPARALLELALTER TABLE IR_NEWFORM
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
CREATE TABLE IR_PAGE 
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
NOPARALLELALTER TABLE IR_PAGE
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
CREATE TABLE IR_ROLE_ACL 
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
NOPARALLELALTER TABLE IR_ROLE_ACL
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
CREATE TABLE IR_SERVICE_ACL 
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
NOPARALLELALTER TABLE IR_SERVICE_ACL
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
CREATE TABLE IR_USER_ACL 
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
NOPARALLELALTER TABLE IR_USER_ACL
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
CREATE TABLE LETTER 
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
NOPARALLELALTER TABLE LETTER
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
CREATE TABLE LETTER_IMAGE 
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
NOPARALLELALTER TABLE LETTER_IMAGE
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
CREATE TABLE LOCATION 
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
NOCOMPRESSALTER TABLE LOCATION
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.MAPPING with DBMS_METADATA attempting internal generator.
CREATE TABLE MAPPING 
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
NOCOMPRESSALTER TABLE MAPPING
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.NOTICE with DBMS_METADATA attempting internal generator.
CREATE TABLE NOTICE 
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
NOPARALLELALTER TABLE NOTICE
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
CREATE TABLE NOTICE_IMAGE 
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
NOPARALLELALTER TABLE NOTICE_IMAGE
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
CREATE TABLE NOTICE_LOG 
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
)ALTER TABLE NOTICE_LOG
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.NOTICE_TYPE with DBMS_METADATA attempting internal generator.
CREATE TABLE NOTICE_TYPE 
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
NOPARALLELALTER TABLE NOTICE_TYPE
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
CREATE TABLE PAGE 
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
NOCOMPRESSALTER TABLE PAGE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_ANSWER_ACTIVATION with DBMS_METADATA attempting internal generator.
CREATE TABLE PAGE_ANSWER_ACTIVATION 
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
NOPARALLELALTER TABLE PAGE_ANSWER_ACTIVATION
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
CREATE TABLE PAGE_FORM 
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
NOPARALLELALTER TABLE PAGE_FORM
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
CREATE TABLE PAGE_FORM_GROUP 
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
NOCOMPRESSALTER TABLE PAGE_FORM_GROUP
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_GROUP_ACL with DBMS_METADATA attempting internal generator.
CREATE TABLE PAGE_FORM_GROUP_ACL 
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
NOPARALLELALTER TABLE PAGE_FORM_GROUP_ACL
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
CREATE TABLE PAGE_FORM_MODE 
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
NOCOMPRESSALTER TABLE PAGE_FORM_MODE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.PAGE_FORM_ROLE_ACL with DBMS_METADATA attempting internal generator.
CREATE TABLE PAGE_FORM_ROLE_ACL 
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
NOPARALLELALTER TABLE PAGE_FORM_ROLE_ACL
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
CREATE TABLE PAGE_FORM_SERVICE_ACL 
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
NOPARALLELALTER TABLE PAGE_FORM_SERVICE_ACL
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
CREATE TABLE PAGE_FORM_USER_ACL 
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
NOPARALLELALTER TABLE PAGE_FORM_USER_ACL
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
CREATE TABLE PROPOSAL_ACTIVATION 
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
NOPARALLELALTER TABLE PROPOSAL_ACTIVATION
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
CREATE TABLE QUESTION 
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
NOPARALLELALTER TABLE QUESTION
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
CREATE TABLE QUESTION_CHAPTER 
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
NOPARALLELALTER TABLE QUESTION_CHAPTER
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
CREATE TABLE QUESTION_CHAPTER_GROUP_ACL 
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
NOPARALLELALTER TABLE QUESTION_CHAPTER_GROUP_ACL
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
CREATE TABLE QUESTION_CHAPTER_ROLE_ACL 
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
NOPARALLELALTER TABLE QUESTION_CHAPTER_ROLE_ACL
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
CREATE TABLE QUESTION_CHAPTER_SERVICE_ACL 
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
NOPARALLELALTER TABLE QUESTION_CHAPTER_SERVICE_ACL
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
CREATE TABLE QUESTION_CHAPTER_USER_ACL 
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
NOPARALLELALTER TABLE QUESTION_CHAPTER_USER_ACL
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
CREATE TABLE QUESTION_TYPE 
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
NOCOMPRESSALTER TABLE QUESTION_TYPE
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.RESOURCE with DBMS_METADATA attempting internal generator.
CREATE TABLE "RESOURCE" 
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
NOPARALLELALTER TABLE "RESOURCE"
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
CREATE TABLE ROLE 
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
NOPARALLELALTER TABLE ROLE
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
CREATE TABLE R_FORMLIST 
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
NOPARALLELALTER TABLE R_FORMLIST
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
CREATE TABLE R_GROUP_ACL 
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
NOPARALLELALTER TABLE R_GROUP_ACL
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
CREATE TABLE R_LIST 
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
NOPARALLELALTER TABLE R_LIST
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
CREATE TABLE R_LIST_COLUMN 
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
NOPARALLELALTER TABLE R_LIST_COLUMN
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
CREATE TABLE R_ROLE_ACL 
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
NOPARALLELALTER TABLE R_ROLE_ACL
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
CREATE TABLE R_SEARCH 
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
NOPARALLELALTER TABLE R_SEARCH
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
CREATE TABLE R_SEARCH_COLUMN 
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
NOPARALLELALTER TABLE R_SEARCH_COLUMN
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
CREATE TABLE R_SEARCH_FILTER 
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
NOPARALLELALTER TABLE R_SEARCH_FILTER
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
CREATE TABLE R_SERVICE_ACL 
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
NOPARALLELALTER TABLE R_SERVICE_ACL
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
CREATE TABLE R_USER_ACL 
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
NOPARALLELALTER TABLE R_USER_ACL
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
CREATE TABLE SERVICE 
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
NOPARALLELALTER TABLE SERVICE
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
CREATE TABLE SERVICE_ANSWER_ACTIVATION 
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
NOPARALLELALTER TABLE SERVICE_ANSWER_ACTIVATION
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
CREATE TABLE SERVICE_GROUP 
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
NOCOMPRESSALTER TABLE SERVICE_GROUP
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.USER with DBMS_METADATA attempting internal generator.
CREATE TABLE "USER" 
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
NOCOMPRESSALTER TABLE "USER"
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
NOPARALLEL
-- Unable to render TABLE DDL for object CAMAC_DEV.USER_GROUP with DBMS_METADATA attempting internal generator.
CREATE TABLE USER_GROUP 
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
NOPARALLELALTER TABLE USER_GROUP
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
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (10,'save',5,'Speichern',null,'Erfolgreich gespeichert',null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (67,'save',64,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (68,'location',64,'Location setzen',null,null,null,0,1);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (23,'save',22,'Stellungnahme speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (24,'circulationtransition',23,'Zirkulation Status OK',null,null,null,0,1);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (25,'save',23,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (26,'php',22,'Temporar ZirkEnde',null,null,null,0,1);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (27,'php',23,'Set to redac if all done',null,null,null,0,2);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (28,'notice',24,'Retrieve NOtice',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (69,'php',64,'Dossier nummer setzen',null,null,null,0,2);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (87,'save',65,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (107,'save',84,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (108,'save',86,'Speichern',null,null,null,0,0);
Insert into CAMAC_DEV.ACTION (ACTION_ID,AVAILABLE_ACTION_ID,BUTTON_ID,NAME,DESCRIPTION,SUCCESS_MESSAGE,ERROR_MESSAGE,EXECUTE_ALWAYS,SORT) values (109,'formtransition',87,'Zirkulation starten',null,null,null,0,0);
REM INSERTING into CAMAC_DEV.ACTIVATION
SET DEFINE OFF;
Insert into CAMAC_DEV.ACTIVATION (ACTIVATION_ID,CIRCULATION_ID,SERVICE_ID,SERVICE_PARENT_ID,CIRCULATION_STATE_ID,USER_ID,CIRCULATION_ANSWER_ID,START_DATE,DEADLINE_DATE,SUSPENSION_DATE,END_DATE,VERSION,REASON) values (5,4,2,1,1,null,null,to_date('30-JUL-14','DD-MON-RR'),to_date('01-AUG-14','DD-MON-RR'),null,null,1,'Stellungnahme');
Insert into CAMAC_DEV.ACTIVATION (ACTIVATION_ID,CIRCULATION_ID,SERVICE_ID,SERVICE_PARENT_ID,CIRCULATION_STATE_ID,USER_ID,CIRCULATION_ANSWER_ID,START_DATE,DEADLINE_DATE,SUSPENSION_DATE,END_DATE,VERSION,REASON) values (4,3,2,1,1,null,null,to_date('30-JUL-14','DD-MON-RR'),to_date('06-JUL-14','DD-MON-RR'),null,null,1,'Verfugung');
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
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (70,4,21,'i',to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.ACTIVATION_LOG (ACTIVATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (71,5,21,'i',to_date('30-JUL-14','DD-MON-RR'));
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
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('documents','download',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('documents','preview',1);
Insert into CAMAC_DEV.AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('documents','delete',1);
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
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (182,2,3,1,'1');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (182,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (182,6,2,1,'01-14-012');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (202,2,3,1,'5');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (202,5,3,1,'bkbuerg');
Insert into CAMAC_DEV.ANSWER (INSTANCE_ID,QUESTION_ID,CHAPTER_ID,ITEM,ANSWER) values (202,6,2,1,'05-14-002');
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
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (264,to_date('30-JUL-14','DD-MON-RR'),21,'i',182,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (265,to_date('30-JUL-14','DD-MON-RR'),21,'i',182,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (266,to_date('30-JUL-14','DD-MON-RR'),21,'i',182,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (284,to_date('11-AUG-14','DD-MON-RR'),21,'i',202,'INSTANCE_ID',2,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (285,to_date('11-AUG-14','DD-MON-RR'),21,'i',202,'INSTANCE_ID',5,'QUESTION_ID',3,'CHAPTER_ID',1,'ITEM');
Insert into CAMAC_DEV.ANSWER_LOG (ANSWER_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2,ID3,FIELD3,ID4,FIELD4) values (286,to_date('11-AUG-14','DD-MON-RR'),21,'i',202,'INSTANCE_ID',6,'QUESTION_ID',2,'CHAPTER_ID',1,'ITEM');
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
	  [ROLE_ID] = 3');
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
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (54,'offerte-blw-040607_2014-08-13-1111.pdf',202,'/tmp/uploads//202/offerte-blw-040607_2014-08-13-1111.pdf',83,to_date('13-AUG-14','DD-MON-RR'),21,'c7369d2ab34388e8bbead7044d074387','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (55,'offerte-blw-040607_2014-08-13-1112.pdf',202,'/tmp/uploads//202/offerte-blw-040607_2014-08-13-1112.pdf',83,to_date('13-AUG-14','DD-MON-RR'),21,'36647a03edc15c60afeaea8fa1d64fbd','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (83,'camacDossierliste_Zonen_Status.pdf',102,'/vagrant/camac/application/../data/records/102/camacDossierliste_Zonen_Status.pdf',178,to_date('15-AUG-14','DD-MON-RR'),21,'52f622072b21fb69055a95db28c20ecc','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (57,'offerte-blw-040607.pdf',202,'/vagrant/camac/application/../data/records/202/offerte-blw-040607.pdf',83,to_date('13-AUG-14','DD-MON-RR'),21,'55d9cff1be4616a6c4a27183fdf44dcc','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (58,'offerte-blw-040607_2014-08-13-1342.pdf',202,'/vagrant/camac/application/../data/records/202/offerte-blw-040607_2014-08-13-1342.pdf',83,to_date('13-AUG-14','DD-MON-RR'),21,'36df5e82f0c252397dd690447a5a6bf3','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (59,'Hosting1209051500PlusBusiness.pdf',202,'/vagrant/camac/application/../data/records/202/Hosting1209051500PlusBusiness.pdf',178,to_date('13-AUG-14','DD-MON-RR'),21,'29f2d0e72b7ffa9404e3b57bb22bd7cc','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (60,'datenblatt_sefar_140101.pdf',202,'/vagrant/camac/application/../data/records/202/datenblatt_sefar_140101.pdf',57,to_date('13-AUG-14','DD-MON-RR'),21,'a2f789c435a8829cafd5dc43eee02710','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (61,'offerte-titoni-010708.pdf',202,'/vagrant/camac/application/../data/records/202/offerte-titoni-010708.pdf',78,to_date('13-AUG-14','DD-MON-RR'),21,'efa39ad495b8f99acc57c129c58f586a','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (62,'camacDossierliste_Screen.pdf',202,'/vagrant/camac/application/../data/records/202/camacDossierliste_Screen.pdf',190,to_date('13-AUG-14','DD-MON-RR'),21,'2442e0e5ce3bcd1cb9c9bd1cdc309633','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (52,'offerte-blw-040607_2014-08-12-1657.pdf',202,'/tmp/uploads//202/offerte-blw-040607_2014-08-12-1657.pdf',83,to_date('12-AUG-14','DD-MON-RR'),21,'c4832ea817c88d5fd63e8ad448da63ba','application/pdf',1);
Insert into CAMAC_DEV.ATTACHMENT (ATTACHMENT_ID,NAME,INSTANCE_ID,PATH,"SIZE","DATE",USER_ID,IDENTIFIER,MIME_TYPE,TYPE) values (53,'offerte-blw-040607_2014-08-13-1107.pdf',202,'/tmp/uploads//202/offerte-blw-040607_2014-08-13-1107.pdf',83,to_date('13-AUG-14','DD-MON-RR'),21,'7cedeaf785f994fe6e1295b84b91a78b','application/pdf',1);
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
Insert into CAMAC_DEV.A_FORMTRANSITION (ACTION_ID,CURRENT_INSTANCE_STATE_ID,NEXT_INSTANCE_STATE_ID) values (109,null,23);
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
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (84,125,'Speichern',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (22,23,'Antwort speichern',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (23,23,'Antwort senden',null,null,0,1);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (24,23,'Retrieve NOtice',null,null,0,2);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (65,107,'Speichern',null,null,0,0);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (87,125,'Zirkulation starten',null,null,0,1);
Insert into CAMAC_DEV.BUTTON (BUTTON_ID,INSTANCE_RESOURCE_ID,NAME,DESCRIPTION,CLASS,HIDDEN,SORT) values (86,105,'Speichern',null,null,0,0);
REM INSERTING into CAMAC_DEV.B_GROUP_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.B_GROUP_ACL (BUTTON_ID,GROUP_ID,INSTANCE_STATE_ID) values (23,23,23);
REM INSERTING into CAMAC_DEV.B_ROLE_ACL
SET DEFINE OFF;
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,6,1);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,6,21);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (4,6,21);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (24,4,23);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (64,3,1);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (65,3,22);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (65,3,24);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (84,3,22);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (84,3,23);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (84,3,24);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (87,3,22);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (87,3,23);
Insert into CAMAC_DEV.B_ROLE_ACL (BUTTON_ID,ROLE_ID,INSTANCE_STATE_ID) values (87,3,24);
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
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,3,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,3,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,3,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,3,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,3,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,3,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,3,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,1,6,27);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,3,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,3,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,3,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,3,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,3,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,3,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (2,1,3,27);
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
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,1,3,1);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (3,1,6,1);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,3,21);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,3,22);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,3,23);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,3,24);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,3,25);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,3,26);
Insert into CAMAC_DEV.CHAPTER_PAGE_ROLE_ACL (CHAPTER_ID,PAGE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,1,3,27);
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
Insert into CAMAC_DEV.CIRCULATION (CIRCULATION_ID,INSTANCE_RESOURCE_ID,INSTANCE_ID,NAME) values (5,105,122,'zirk2');
Insert into CAMAC_DEV.CIRCULATION (CIRCULATION_ID,INSTANCE_RESOURCE_ID,INSTANCE_ID,NAME) values (23,125,202,'Erste Zirkulation');
Insert into CAMAC_DEV.CIRCULATION (CIRCULATION_ID,INSTANCE_RESOURCE_ID,INSTANCE_ID,NAME) values (3,125,164,'Erste Zirkulation');
Insert into CAMAC_DEV.CIRCULATION (CIRCULATION_ID,INSTANCE_RESOURCE_ID,INSTANCE_ID,NAME) values (4,125,182,'zirk1');
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
Insert into CAMAC_DEV.CIRCULATION_LOG (CIRCULATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (3,3,21,'i',to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.CIRCULATION_LOG (CIRCULATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (4,4,21,'i',to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.CIRCULATION_LOG (CIRCULATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (5,5,21,'i',to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.CIRCULATION_LOG (CIRCULATION_LOG_ID,ID,USER_ID,ACTION,MODIFICATION_DATE) values (23,23,21,'i',to_date('11-AUG-14','DD-MON-RR'));
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
Insert into CAMAC_DEV."GROUP" (GROUP_ID,ROLE_ID,SERVICE_ID,NAME) values (21,3,1,'Koordinationsstelle Baugesuche');
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
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (164,23,43,21,21,to_date('30-JUL-14','DD-MON-RR'),to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (182,23,43,21,21,to_date('30-JUL-14','DD-MON-RR'),to_date('30-JUL-14','DD-MON-RR'));
Insert into CAMAC_DEV.INSTANCE (INSTANCE_ID,INSTANCE_STATE_ID,FORM_ID,USER_ID,GROUP_ID,CREATION_DATE,MODIFICATION_DATE) values (202,22,43,21,21,to_date('11-AUG-14','DD-MON-RR'),to_date('11-AUG-14','DD-MON-RR'));
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
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,164);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (1,182);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (2,82);
Insert into CAMAC_DEV.INSTANCE_LOCATION (LOCATION_ID,INSTANCE_ID) values (5,202);
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
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (182,to_date('30-JUL-14','DD-MON-RR'),21,'i',182,'INSTANCE_ID',1,'LOCATION_ID');
Insert into CAMAC_DEV.INSTANCE_LOCATION_LOG (INSTANCE_LOCATION_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID1,FIELD1,ID2,FIELD2) values (202,to_date('11-AUG-14','DD-MON-RR'),21,'i',202,'INSTANCE_ID',5,'LOCATION_ID');
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
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (166,to_date('30-JUL-14','DD-MON-RR'),21,'u',164);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (167,to_date('30-JUL-14','DD-MON-RR'),21,'i',182);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (168,to_date('30-JUL-14','DD-MON-RR'),21,'u',182);
Insert into CAMAC_DEV.INSTANCE_LOG (INSTANCE_LOG_ID,MODIFICATION_DATE,USER_ID,ACTION,ID) values (186,to_date('11-AUG-14','DD-MON-RR'),21,'i',202);
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
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (125,'editcirculation',24,43,'Zirkulation','Zirkulation fur internes Genehmigungsverfahren',null,null,0,6);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (46,'documents',23,44,'Dokumente',null,null,null,0,2);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (85,'formpage',24,44,'Dossier anschauen',null,null,null,0,1);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (126,'formpage',24,43,'Dossier anschauen',null,null,null,0,5);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (145,'documents',24,44,'Dokumente','Dokumente fur Baubewilligungsverfahren mit kantonaler Beteiligung',null,null,0,7);
Insert into CAMAC_DEV.INSTANCE_RESOURCE (INSTANCE_RESOURCE_ID,AVAILABLE_INSTANCE_RESOURCE_ID,RESOURCE_ID,FORM_ID,NAME,DESCRIPTION,TEMPLATE,CLASS,HIDDEN,SORT) values (146,'documents',24,43,'Dokumente','Dokumente fur internes Genehmigungsverfahren',null,null,0,8);
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
Insert into CAMAC_DEV.IR_EDITCIRCULATION_SG (IR_EDITCIRCULATION_SG_ID,INSTANCE_RESOURCE_ID,SERVICE_GROUP_ID,LOCALIZED) values (22,125,2,0);
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
Insert into CAMAC_DEV.IR_FORMPAGE (INSTANCE_RESOURCE_ID,PAGE_ID,PDF_CLASS) values (126,1,null);
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
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (4,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (4,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,3,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,3,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,3,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,3,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (5,6,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,3,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,3,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (21,3,27);
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
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,3,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,3,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,3,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (85,3,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,3,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,3,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,3,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (105,3,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (106,3,1);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (107,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (107,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (125,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (125,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (125,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (126,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (126,3,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (126,3,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (126,3,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,3,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,3,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,3,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,3,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,6,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,6,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,6,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,6,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,6,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,6,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (145,6,27);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (146,3,21);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (146,3,22);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (146,3,23);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (146,3,24);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (146,3,25);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (146,3,26);
Insert into CAMAC_DEV.IR_ROLE_ACL (INSTANCE_RESOURCE_ID,ROLE_ID,INSTANCE_STATE_ID) values (146,3,27);
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
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,1);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,21);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,22);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,23);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,24);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,25);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,26);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,43,3,27);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,3,21);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,3,22);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,3,23);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,3,24);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,3,25);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,3,26);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,3,27);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,1);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,21);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,22);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,23);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,24);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,25);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,26);
Insert into CAMAC_DEV.PAGE_FORM_ROLE_ACL (PAGE_ID,FORM_ID,ROLE_ID,INSTANCE_STATE_ID) values (1,44,6,27);
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

	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",

	"FORM"."NAME"              AS "FORM",

	"ACTIVATION"."DEADLINE_DATE" AS "DEADLINE",

	"LOCATION"."NAME"          AS "COMMUNITY",

	"ANSWER_PETITION"."ANSWER" AS "PETITION",

	"ANSWER_INTENT"."ANSWER"   AS "INTENT",

	"ANSWER_CITY"."ANSWER"     AS "CITY",

	"INSTANCE_STATE"."NAME"    AS "STATE",

	"ACTIVATION"."REASON"      AS "REASON"

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

	"CIRCULATION" ON (

		"CIRCULATION"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"

	)
 
JOIN

	"ACTIVATION" ON (

		"ACTIVATION"."CIRCULATION_ID" = "CIRCULATION"."CIRCULATION_ID"

		AND

		"ACTIVATION"."SERVICE_ID" = [SERVICE_ID]

	)

WHERE

	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"');
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
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (104,41,'DEADLINE','Frist',2);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (42,41,'STATE','Status',7);
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
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (72,41,'DOSSIER_NR','Dossier-Nr.',0);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (73,41,'FORM','Verfahren',1);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (74,41,'COMMUNITY','Gemeinde',3);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (105,41,'REASON','Grund',8);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (76,41,'PETITION','Gesuchsteller',4);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (77,41,'INTENT','Vorhaben',5);
Insert into CAMAC_DEV.R_LIST_COLUMN (R_LIST_COLUMN_ID,RESOURCE_ID,COLUMN_NAME,ALIAS,SORT) values (78,41,'CITY','Ort',6);
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
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (1,3);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (1,4);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (1,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (22,3);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (22,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (23,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (24,3);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (42,3);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (42,6);
Insert into CAMAC_DEV.R_ROLE_ACL (RESOURCE_ID,ROLE_ID) values (62,3);
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
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (21,42,null,'form','Verfahren','"INSTANCE"."FORM_ID" IN ( ?)',0);
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (22,42,null,'creationfrom','Erstellung von','"INSTANCE"."CREATION_DATE" >= (TO_DATE(?, ''DD-MM-YY''))',0);
Insert into CAMAC_DEV.R_SEARCH_FILTER (R_SEARCH_FILTER_ID,RESOURCE_ID,QUESTION_ID,FIELD_NAME,LABEL,QUERY,WILDCARD) values (23,42,null,'creationtil','Erstellung bis','"INSTANCE"."CREATION_DATE" <= (TO_DATE(?, ''dd-mm-yy''))',0);
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
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (1,'admin','10602b62c0f171f626e3d64046c27567','Administrator','Static',null,null,0,'en',to_date('15-AUG-14','DD-MON-RR'));
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (2,'guest',null,'Guest','Static',null,null,0,'en',to_date('18-AUG-14','DD-MON-RR'));
Insert into CAMAC_DEV."USER" (USER_ID,USERNAME,PASSWORD,NAME,SURNAME,EMAIL,PHONE,DISABLED,LANGUAGE,LAST_REQUEST_DATE) values (21,'pwa','c1784faf0e31b8d206c503a861906278','Walker','Paul',null,null,0,'de',to_date('15-AUG-14','DD-MON-RR'));
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
-- Unable to render TRIGGER DDL for object CAMAC_DEV.ATTACHMENT_TRG with DBMS_METADATA attempting internal generator.
CREATE TRIGGER ATTACHMENT_TRG ON . 
BEGIN
  NULL;
END;
-- Unable to render FUNCTION DDL for object CAMAC_DEV.GET_STATE_ID_BY_NAME with DBMS_METADATA attempting internal generator.
CREATE FUNCTION             "GET_STATE_ID_BY_NAME" (STATE_NAME IN VARCHAR2)

	RETURN number

IS

	stateID number;

BEGIN

	SELECT

		INSTANCE_STATE_ID into stateID

	FROM

		INSTANCE_STATE

	WHERE

		LOWER(NAME) = LOWER(STATE_NAME);

	RETURN stateID;

END;
-- Unable to render FUNCTION DDL for object CAMAC_DEV.GET_STATE_NAME_BY_ID with DBMS_METADATA attempting internal generator.
CREATE FUNCTION             "GET_STATE_NAME_BY_ID" (STATE_ID IN NUMBER)

	RETURN VARCHAR2

IS

	STATE_NAME VARCHAR2(255);

BEGIN

	SELECT

		NAME into STATE_NAME

	FROM

		INSTANCE_STATE

	WHERE

		INSTANCE_STATE_ID = STATE_ID;

	RETURN STATE_NAME;

END;
-- Unable to render FUNCTION DDL for object CAMAC_DEV.MD5 with DBMS_METADATA attempting internal generator.
CREATE FUNCTION             "MD5" (str IN VARCHAR2) RETURN VARCHAR2 AS

BEGIN

  RETURN sys.dbms_obfuscation_toolkit.md5(input => utl_raw.cast_to_raw(str));

END MD5;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_AC with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_AC as
  --json type methods

  procedure object_remove(p_self in out nocopy json, pair_name varchar2);
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value json_value, position pls_integer default null);
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value varchar2, position pls_integer default null);
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value number, position pls_integer default null);
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value boolean, position pls_integer default null);
  procedure object_check_duplicate(p_self in out nocopy json, v_set boolean);
  procedure object_remove_duplicates(p_self in out nocopy json);

  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value json, position pls_integer default null);
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value json_list, position pls_integer default null);

  function object_count(p_self in json) return number;
  function object_get(p_self in json, pair_name varchar2) return json_value;
  function object_get(p_self in json, position pls_integer) return json_value;
  function object_index_of(p_self in json, pair_name varchar2) return number;
  function object_exist(p_self in json, pair_name varchar2) return boolean;

  function object_to_char(p_self in json, spaces boolean default true, chars_per_line number default 0) return varchar2;
  procedure object_to_clob(p_self in json, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true);
  procedure object_print(p_self in json, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null); 
  procedure object_htp(p_self in json, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null);
  
  function object_to_json_value(p_self in json) return json_value;
  function object_path(p_self in json, json_path varchar2, base number default 1) return json_value;
  
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem json_value, base number default 1);
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem varchar2  , base number default 1);
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem number    , base number default 1);
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem boolean   , base number default 1);
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem json_list , base number default 1);
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem json      , base number default 1);
  
  procedure object_path_remove(p_self in out nocopy json, json_path varchar2, base number default 1);

  function object_get_values(p_self in json) return json_list;
  function object_get_keys(p_self in json) return json_list;
  
  --json_list type methods  
  procedure array_append(p_self in out nocopy json_list, elem json_value, position pls_integer default null);
  procedure array_append(p_self in out nocopy json_list, elem varchar2, position pls_integer default null);
  procedure array_append(p_self in out nocopy json_list, elem number, position pls_integer default null);
  procedure array_append(p_self in out nocopy json_list, elem boolean, position pls_integer default null);
  procedure array_append(p_self in out nocopy json_list, elem json_list, position pls_integer default null);

  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem json_value);
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem varchar2);
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem number);
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem boolean);
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem json_list);

  function array_count(p_self in json_list) return number;
  procedure array_remove(p_self in out nocopy json_list, position pls_integer);
  procedure array_remove_first(p_self in out nocopy json_list);
  procedure array_remove_last(p_self in out nocopy json_list);
  function array_get(p_self in json_list, position pls_integer) return json_value;
  function array_head(p_self in json_list) return json_value;
  function array_last(p_self in json_list) return json_value;
  function array_tail(p_self in json_list) return json_list;

  function array_to_char(p_self in json_list, spaces boolean default true, chars_per_line number default 0) return varchar2;
  procedure array_to_clob(p_self in json_list, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true);
  procedure array_print(p_self in json_list, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null); 
  procedure array_htp(p_self in json_list, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null);

  function array_path(p_self in json_list, json_path varchar2, base number default 1) return json_value;
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem json_value, base number default 1);
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem varchar2  , base number default 1);
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem number    , base number default 1);
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem boolean   , base number default 1);
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem json_list , base number default 1);

  procedure array_path_remove(p_self in out nocopy json_list, json_path varchar2, base number default 1);

  function array_to_json_value(p_self in json_list) return json_value;

  --json_value
  

  function jv_get_type(p_self in json_value) return varchar2;
  function jv_get_string(p_self in json_value, max_byte_size number default null, max_char_size number default null) return varchar2;
  procedure jv_get_string(p_self in json_value, buf in out nocopy clob);
  function jv_get_number(p_self in json_value) return number;
  function jv_get_bool(p_self in json_value) return boolean;
  function jv_get_null(p_self in json_value) return varchar2;
  
  function jv_is_object(p_self in json_value) return boolean;
  function jv_is_array(p_self in json_value) return boolean;
  function jv_is_string(p_self in json_value) return boolean;
  function jv_is_number(p_self in json_value) return boolean;
  function jv_is_bool(p_self in json_value) return boolean;
  function jv_is_null(p_self in json_value) return boolean;
  
  function jv_to_char(p_self in json_value, spaces boolean default true, chars_per_line number default 0) return varchar2;
  procedure jv_to_clob(p_self in json_value, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true);
  procedure jv_print(p_self in json_value, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null);
  procedure jv_htp(p_self in json_value, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null);
  
  function jv_value_of(p_self in json_value, max_byte_size number default null, max_char_size number default null) return varchar2;


end json_ac;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_DYN with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_DYN authid current_user as
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

  null_as_empty_string   boolean not null := true;  --varchar2
  include_dates          boolean not null := true;  --date
  include_clobs          boolean not null := true;
  include_blobs          boolean not null := false;
  
  /* list with objects */
  function executeList(stmt varchar2, bindvar json default null, cur_num number default null) return json_list;
  
  /* object with lists */
  function executeObject(stmt varchar2, bindvar json default null, cur_num number default null) return json;


  /* usage example:
   * declare
   *   res json_list;
   * begin
   *   res := json_dyn.executeList(
   *            'select :bindme as one, :lala as two from dual where dummy in :arraybind',
   *            json('{bindme:"4", lala:123, arraybind:[1,2,3,"X"]}')
   *          );
   *   res.print;
   * end;
   */

/* --11g functions
  function executeList(stmt in out sys_refcursor) return json_list;
  function executeObject(stmt in out sys_refcursor) return json;
*/
end json_dyn;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_EXT with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_EXT as
  /*
  Copyright (c) 2009 Jonas Krogsboell

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
  
  /* This package contains extra methods to lookup types and
     an easy way of adding date values in json - without changing the structure */
  function parsePath(json_path varchar2, base number default 1) return json_list;
  
  --JSON Path getters
  function get_json_value(obj json, v_path varchar2, base number default 1) return json_value;
  function get_string(obj json, path varchar2,       base number default 1) return varchar2;
  function get_number(obj json, path varchar2,       base number default 1) return number;
  function get_json(obj json, path varchar2,         base number default 1) return json;
  function get_json_list(obj json, path varchar2,    base number default 1) return json_list;
  function get_bool(obj json, path varchar2,         base number default 1) return boolean;

  --JSON Path putters
  procedure put(obj in out nocopy json, path varchar2, elem varchar2,   base number default 1);
  procedure put(obj in out nocopy json, path varchar2, elem number,     base number default 1);
  procedure put(obj in out nocopy json, path varchar2, elem json,       base number default 1);
  procedure put(obj in out nocopy json, path varchar2, elem json_list,  base number default 1);
  procedure put(obj in out nocopy json, path varchar2, elem boolean,    base number default 1);
  procedure put(obj in out nocopy json, path varchar2, elem json_value, base number default 1);

  procedure remove(obj in out nocopy json, path varchar2, base number default 1);
  
  --Pretty print with JSON Path - obsolete in 0.9.4 - obj.path(v_path).(to_char,print,htp)
  function pp(obj json, v_path varchar2) return varchar2; 
  procedure pp(obj json, v_path varchar2); --using dbms_output.put_line
  procedure pp_htp(obj json, v_path varchar2); --using htp.print

  --extra function checks if number has no fraction
  function is_integer(v json_value) return boolean;
  
  format_string varchar2(30 char) := 'yyyy-mm-dd hh24:mi:ss';
  --extension enables json to store dates without comprimising the implementation
  function to_json_value(d date) return json_value;
  --notice that a date type in json is also a varchar2
  function is_date(v json_value) return boolean;
  --convertion is needed to extract dates 
  --(json_ext.to_date will not work along with the normal to_date function - any fix will be appreciated)
  function to_date2(v json_value) return date;
  --JSON Path with date
  function get_date(obj json, path varchar2, base number default 1) return date;
  procedure put(obj in out nocopy json, path varchar2, elem date, base number default 1);
  
  --experimental support of binary data with base64
  function base64(binarydata blob) return json_list;
  function base64(l json_list) return blob;

  function encode(binarydata blob) return json_value;
  function decode(v json_value) return blob;
  
end json_ext;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_HELPER with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_HELPER as
  /* Example:
  set serveroutput on;
  declare
    v_a json;
    v_b json;
  begin
    v_a := json('{a:1, b:{a:null}, e:false}');
    v_b := json('{c:3, e:{}, b:{b:2}}');
    json_helper.merge(v_a, v_b).print(false);
  end;
  --
  {"a":1,"b":{"a":null,"b":2},"e":{},"c":3}
  */
  -- Recursive merge
  -- Courtesy of Matt Nolan - edited by Jonas Krogsbï¿½ll
  function merge( p_a_json json, p_b_json json) return json;

  -- Join two lists
  -- json_helper.join(json_list('[1,2,3]'),json_list('[4,5,6]')) -> [1,2,3,4,5,6] 
  function join( p_a_list json_list, p_b_list json_list) return json_list;

  -- keep only specific keys in json object
  -- json_helper.keep(json('{a:1,b:2,c:3,d:4,e:5,f:6}'),json_list('["a","f","c"]')) -> {"a":1,"f":6,"c":3}
  function keep( p_json json, p_keys json_list) return json;
  
  -- remove specific keys in json object
  -- json_helper.remove(json('{a:1,b:2,c:3,d:4,e:5,f:6}'),json_list('["a","f","c"]')) -> {"b":2,"d":4,"e":5}
  function remove( p_json json, p_keys json_list) return json;
  
  --equals
  function equals(p_v1 json_value, p_v2 json_value, exact boolean default true) return boolean;
  function equals(p_v1 json_value, p_v2 json, exact boolean default true) return boolean;
  function equals(p_v1 json_value, p_v2 json_list, exact boolean default true) return boolean;
  function equals(p_v1 json_value, p_v2 number) return boolean;
  function equals(p_v1 json_value, p_v2 varchar2) return boolean;
  function equals(p_v1 json_value, p_v2 boolean) return boolean; 
  function equals(p_v1 json_value, p_v2 clob) return boolean;
  function equals(p_v1 json, p_v2 json, exact boolean default true) return boolean;
  function equals(p_v1 json_list, p_v2 json_list, exact boolean default true) return boolean;
  
  --contains json, json_value
  --contains json_list, json_value
  function contains(p_v1 json, p_v2 json_value, exact boolean default false) return boolean;
  function contains(p_v1 json, p_v2 json, exact boolean default false) return boolean;
  function contains(p_v1 json, p_v2 json_list, exact boolean default false) return boolean;
  function contains(p_v1 json, p_v2 number, exact boolean default false) return boolean;
  function contains(p_v1 json, p_v2 varchar2, exact boolean default false) return boolean;
  function contains(p_v1 json, p_v2 boolean, exact boolean default false) return boolean;
  function contains(p_v1 json, p_v2 clob, exact boolean default false) return boolean;
  
  function contains(p_v1 json_list, p_v2 json_value, exact boolean default false) return boolean;
  function contains(p_v1 json_list, p_v2 json, exact boolean default false) return boolean;
  function contains(p_v1 json_list, p_v2 json_list, exact boolean default false) return boolean;
  function contains(p_v1 json_list, p_v2 number, exact boolean default false) return boolean;
  function contains(p_v1 json_list, p_v2 varchar2, exact boolean default false) return boolean;
  function contains(p_v1 json_list, p_v2 boolean, exact boolean default false) return boolean;
  function contains(p_v1 json_list, p_v2 clob, exact boolean default false) return boolean;

end json_helper;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_ML with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_ML as
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
  
  /* This package contains extra methods to lookup types and
     an easy way of adding date values in json - without changing the structure */

  jsonml_stylesheet xmltype := null;
  
  function xml2json(xml in xmltype) return json_list;
  function xmlstr2json(xmlstr in varchar2) return json_list;

end json_ml;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_PARSER with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_PARSER as
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
  /* scanner tokens:
    '{', '}', ',', ':', '[', ']', STRING, NUMBER, TRUE, FALSE, NULL 
  */
  type rToken IS RECORD (
    type_name VARCHAR2(7),
    line PLS_INTEGER,
    col PLS_INTEGER,
    data VARCHAR2(32767),
    data_overflow clob); -- max_string_size

  type lTokens is table of rToken index by pls_integer;
  type json_src is record (len number, offset number, src varchar2(32767), s_clob clob); 

  json_strict boolean not null := false;

  function next_char(indx number, s in out nocopy json_src) return varchar2;
  function next_char2(indx number, s in out nocopy json_src, amount number default 1) return varchar2;
  
  function prepareClob(buf in clob) return json_parser.json_src;
  function prepareVarchar2(buf in varchar2) return json_parser.json_src;
  function lexer(jsrc in out nocopy json_src) return lTokens;
  procedure print_token(t rToken);

  function parser(str varchar2) return json;
  function parse_list(str varchar2) return json_list;
  function parse_any(str varchar2) return json_value;
  function parser(str clob) return json;
  function parse_list(str clob) return json_list;
  function parse_any(str clob) return json_value;
  procedure remove_duplicates(obj in out nocopy json);
  function get_version return varchar2;
  
end json_parser;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_PRINTER with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_PRINTER as
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
  indent_string varchar2(10 char) := '  '; --chr(9); for tab
  newline_char varchar2(2 char)   := chr(13)||chr(10); -- Windows style
  --newline_char varchar2(2) := chr(10); -- Mac style
  --newline_char varchar2(2) := chr(13); -- Linux style
  ascii_output boolean    not null := true;
  escape_solidus boolean  not null := false;

  function pretty_print(obj json, spaces boolean default true, line_length number default 0) return varchar2;
  function pretty_print_list(obj json_list, spaces boolean default true, line_length number default 0) return varchar2;
  function pretty_print_any(json_part json_value, spaces boolean default true, line_length number default 0) return varchar2;
  procedure pretty_print(obj json, spaces boolean default true, buf in out nocopy clob, line_length number default 0, erase_clob boolean default true);
  procedure pretty_print_list(obj json_list, spaces boolean default true, buf in out nocopy clob, line_length number default 0, erase_clob boolean default true);
  procedure pretty_print_any(json_part json_value, spaces boolean default true, buf in out nocopy clob, line_length number default 0, erase_clob boolean default true);
  
  procedure dbms_output_clob(my_clob clob, delim varchar2, jsonp varchar2 default null);
  procedure htp_output_clob(my_clob clob, jsonp varchar2 default null);
end json_printer;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_UTIL_PKG with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_UTIL_PKG authid current_user as

  /*

  Purpose:    JSON utilities for PL/SQL
  see http://ora-00001.blogspot.com/
  
  Remarks:    

  Who     Date        Description
  ------  ----------  -------------------------------------
  MBR     30.01.2010  Created
  JKR     01.05.2010  Edited to fit in PL/JSON
  JKR     19.01.2011  Newest stylesheet + bugfix handling
  
  */

  -- generate JSON from REF Cursor
  function ref_cursor_to_json (p_ref_cursor in sys_refcursor,
                               p_max_rows in number := null,
                               p_skip_rows in number := null) return json_list;

  -- generate JSON from SQL statement
  function sql_to_json (p_sql in varchar2,
                        p_max_rows in number := null,
                        p_skip_rows in number := null) return json_list;


end json_util_pkg;
-- Unable to render PACKAGE DDL for object CAMAC_DEV.JSON_XML with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE JSON_XML as 
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
  
  /*
  declare
    obj json := json('{a:1,b:[2,3,4],c:true}');
    x xmltype;
  begin
    obj.print;
    x := json_xml.json_to_xml(obj);
    dbms_output.put_line(x.getclobval());
  end;  
  */

  function json_to_xml(obj json, tagname varchar2 default 'root') return xmltype;

end json_xml;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_AC with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY JSON_AC as
  procedure object_remove(p_self in out nocopy json, pair_name varchar2) as
  begin p_self.remove(pair_name); end;
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value json_value, position pls_integer default null) as
  begin p_self.put(pair_name, pair_value, position); end;
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value varchar2, position pls_integer default null) as
  begin p_self.put(pair_name, pair_value, position); end;
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value number, position pls_integer default null) as
  begin p_self.put(pair_name, pair_value, position); end;
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value boolean, position pls_integer default null) as
  begin p_self.put(pair_name, pair_value, position); end;
  procedure object_check_duplicate(p_self in out nocopy json, v_set boolean) as
  begin p_self.check_duplicate(v_set); end;
  procedure object_remove_duplicates(p_self in out nocopy json) as
  begin p_self.remove_duplicates; end;

  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value json, position pls_integer default null) as
  begin p_self.put(pair_name, pair_value, position); end;
  procedure object_put(p_self in out nocopy json, pair_name varchar2, pair_value json_list, position pls_integer default null) as
  begin p_self.put(pair_name, pair_value, position); end;

  function object_count(p_self in json) return number as
  begin return p_self.count; end;
  function object_get(p_self in json, pair_name varchar2) return json_value as
  begin return p_self.get(pair_name); end;
  function object_get(p_self in json, position pls_integer) return json_value as
  begin return p_self.get(position); end;
  function object_index_of(p_self in json, pair_name varchar2) return number as
  begin return p_self.index_of(pair_name); end;
  function object_exist(p_self in json, pair_name varchar2) return boolean as
  begin return p_self.exist(pair_name); end;

  function object_to_char(p_self in json, spaces boolean default true, chars_per_line number default 0) return varchar2 as
  begin return p_self.to_char(spaces, chars_per_line); end;
  procedure object_to_clob(p_self in json, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true) as
  begin p_self.to_clob(buf, spaces, chars_per_line, erase_clob); end;
  procedure object_print(p_self in json, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null) as
  begin p_self.print(spaces, chars_per_line, jsonp); end;
  procedure object_htp(p_self in json, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null) as
  begin p_self.htp(spaces, chars_per_line, jsonp); end;
  
  function object_to_json_value(p_self in json) return json_value as
  begin return p_self.to_json_value; end;
  function object_path(p_self in json, json_path varchar2, base number default 1) return json_value as
  begin return p_self.path(json_path, base); end;

  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem json_value, base number default 1) as
  begin p_self.path_put(json_path, elem, base); end;
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem varchar2  , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end;
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem number    , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end;
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem boolean   , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end;
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem json_list , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end;
  procedure object_path_put(p_self in out nocopy json, json_path varchar2, elem json      , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end;

  procedure object_path_remove(p_self in out nocopy json, json_path varchar2, base number default 1) as
  begin p_self.path_remove(json_path, base); end;

  function object_get_values(p_self in json) return json_list as
  begin return p_self.get_values; end;
  function object_get_keys(p_self in json) return json_list as
  begin return p_self.get_keys; end;
  
  --json_list type
  procedure array_append(p_self in out nocopy json_list, elem json_value, position pls_integer default null) as
  begin p_self.append(elem, position); end;
  procedure array_append(p_self in out nocopy json_list, elem varchar2, position pls_integer default null) as
  begin p_self.append(elem, position); end;
  procedure array_append(p_self in out nocopy json_list, elem number, position pls_integer default null) as
  begin p_self.append(elem, position); end;
  procedure array_append(p_self in out nocopy json_list, elem boolean, position pls_integer default null) as
  begin p_self.append(elem, position); end;
  procedure array_append(p_self in out nocopy json_list, elem json_list, position pls_integer default null) as
  begin p_self.append(elem, position); end;

  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem json_value) as
  begin p_self.replace(position, elem); end;
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem varchar2) as
  begin p_self.replace(position, elem); end;
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem number) as
  begin p_self.replace(position, elem); end;
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem boolean) as
  begin p_self.replace(position, elem); end;
  procedure array_replace(p_self in out nocopy json_list, position pls_integer, elem json_list) as
  begin p_self.replace(position, elem); end;

  function array_count(p_self in json_list) return number as
  begin return p_self.count; end;
  procedure array_remove(p_self in out nocopy json_list, position pls_integer) as
  begin p_self.remove(position); end;
  procedure array_remove_first(p_self in out nocopy json_list) as
  begin p_self.remove_first; end;
  procedure array_remove_last(p_self in out nocopy json_list) as
  begin p_self.remove_last; end;
  function array_get(p_self in json_list, position pls_integer) return json_value as
  begin return p_self.get(position); end;
  function array_head(p_self in json_list) return json_value as
  begin return p_self.head; end;
  function array_last(p_self in json_list) return json_value as
  begin return p_self.last; end;
  function array_tail(p_self in json_list) return json_list as
  begin return p_self.tail; end;

  function array_to_char(p_self in json_list, spaces boolean default true, chars_per_line number default 0) return varchar2 as
  begin return p_self.to_char(spaces, chars_per_line); end;
  procedure array_to_clob(p_self in json_list, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true) as
  begin p_self.to_clob(buf, spaces, chars_per_line, erase_clob); end;
  procedure array_print(p_self in json_list, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null) as 
  begin p_self.print(spaces, chars_per_line, jsonp); end;
  procedure array_htp(p_self in json_list, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null) as
  begin p_self.htp(spaces, chars_per_line, jsonp); end;

  function array_path(p_self in json_list, json_path varchar2, base number default 1) return json_value as
  begin return p_self.path(json_path, base); end;
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem json_value, base number default 1) as
  begin p_self.path_put(json_path, elem, base); end; 
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem varchar2  , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end; 
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem number    , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end; 
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem boolean   , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end; 
  procedure array_path_put(p_self in out nocopy json_list, json_path varchar2, elem json_list , base number default 1) as
  begin p_self.path_put(json_path, elem, base); end; 

  procedure array_path_remove(p_self in out nocopy json_list, json_path varchar2, base number default 1) as
  begin p_self.path_remove(json_path, base); end; 

  function array_to_json_value(p_self in json_list) return json_value as
  begin return p_self.to_json_value; end;
  
  --json_value
  
    
  function jv_get_type(p_self in json_value) return varchar2 as
  begin return p_self.get_type; end;
  function jv_get_string(p_self in json_value, max_byte_size number default null, max_char_size number default null) return varchar2 as
  begin return p_self.get_string(max_byte_size, max_char_size); end;
  procedure jv_get_string(p_self in json_value, buf in out nocopy clob) as
  begin p_self.get_string(buf); end;
  function jv_get_number(p_self in json_value) return number as
  begin return p_self.get_number; end;
  function jv_get_bool(p_self in json_value) return boolean as
  begin return p_self.get_bool; end;
  function jv_get_null(p_self in json_value) return varchar2 as
  begin return p_self.get_null; end;
  
  function jv_is_object(p_self in json_value) return boolean as
  begin return p_self.is_object; end;
  function jv_is_array(p_self in json_value) return boolean as
  begin return p_self.is_array; end;
  function jv_is_string(p_self in json_value) return boolean as
  begin return p_self.is_string; end;
  function jv_is_number(p_self in json_value) return boolean as
  begin return p_self.is_number; end;
  function jv_is_bool(p_self in json_value) return boolean as
  begin return p_self.is_bool; end;
  function jv_is_null(p_self in json_value) return boolean as
  begin return p_self.is_null; end;
  
  function jv_to_char(p_self in json_value, spaces boolean default true, chars_per_line number default 0) return varchar2 as
  begin return p_self.to_char(spaces, chars_per_line); end;
  procedure jv_to_clob(p_self in json_value, buf in out nocopy clob, spaces boolean default false, chars_per_line number default 0, erase_clob boolean default true) as
  begin p_self.to_clob(buf, spaces, chars_per_line, erase_clob); end; 
  procedure jv_print(p_self in json_value, spaces boolean default true, chars_per_line number default 8192, jsonp varchar2 default null) as
  begin p_self.print(spaces, chars_per_line, jsonp); end;
  procedure jv_htp(p_self in json_value, spaces boolean default false, chars_per_line number default 0, jsonp varchar2 default null) as
  begin p_self.htp(spaces, chars_per_line, jsonp); end;
  
  function jv_value_of(p_self in json_value, max_byte_size number default null, max_char_size number default null) return varchar2 as
  begin return p_self.value_of(max_byte_size, max_char_size); end;

end json_ac;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_DYN with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY JSON_DYN as
/*
  -- 11gR2 
  function executeList(stmt in out sys_refcursor) return json_list as
    l_cur number;
  begin
    l_cur := dbms_sql.to_cursor_number(stmt);
    return json_dyn.executeList(null, null, l_cur);
  end;

  -- 11gR2 
  function executeObject(stmt in out sys_refcursor) return json as
    l_cur number;
  begin
    l_cur := dbms_sql.to_cursor_number(stmt);
    return json_dyn.executeObject(null, null, l_cur);
  end;
*/

  procedure bind_json(l_cur number, bindvar json) as
    keylist json_list := bindvar.get_keys();
  begin
    for i in 1 .. keylist.count loop
      if(bindvar.get(i).get_type = 'number') then
        dbms_sql.bind_variable(l_cur, ':'||keylist.get(i).get_string, bindvar.get(i).get_number);
      elsif(bindvar.get(i).get_type = 'array') then
        declare
          v_bind dbms_sql.varchar2_table;
          v_arr  json_list := json_list(bindvar.get(i));
        begin
          for j in 1 .. v_arr.count loop
            v_bind(j) := v_arr.get(j).value_of;
          end loop;
          dbms_sql.bind_array(l_cur, ':'||keylist.get(i).get_string, v_bind);
        end;
      else
        dbms_sql.bind_variable(l_cur, ':'||keylist.get(i).get_string, bindvar.get(i).value_of());
      end if;
    end loop;
  end bind_json;

  /* list with objects */
  function executeList(stmt varchar2, bindvar json, cur_num number) return json_list as
    l_cur number;
    l_dtbl dbms_sql.desc_tab;
    l_cnt number;
    l_status number;
    l_val varchar2(4000);
    outer_list json_list := json_list();
    inner_obj json;
    conv number;
    read_date date;
    read_clob clob;
    read_blob blob;
    col_type number;
  begin
    if(cur_num is not null) then 
      l_cur := cur_num; 
    else
      l_cur := dbms_sql.open_cursor;
      dbms_sql.parse(l_cur, stmt, dbms_sql.native);
      if(bindvar is not null) then bind_json(l_cur, bindvar); end if;
    end if;
    dbms_sql.describe_columns(l_cur, l_cnt, l_dtbl);
    for i in 1..l_cnt loop
      col_type := l_dtbl(i).col_type;
      --dbms_output.put_line(col_type);
      if(col_type = 12) then
        dbms_sql.define_column(l_cur,i,read_date);
      elsif(col_type = 112) then
        dbms_sql.define_column(l_cur,i,read_clob);
      elsif(col_type = 113) then
        dbms_sql.define_column(l_cur,i,read_blob);
      elsif(col_type in (1,2,96)) then
        dbms_sql.define_column(l_cur,i,l_val,4000);
      end if;
    end loop;
    
    if(cur_num is null) then l_status := dbms_sql.execute(l_cur); end if;
    
    --loop through rows 
    while ( dbms_sql.fetch_rows(l_cur) > 0 ) loop
      inner_obj := json(); --init for each row
      --loop through columns
      for i in 1..l_cnt loop
        case true
        --handling string types
        when l_dtbl(i).col_type in (1,96) then -- varchar2
          dbms_sql.column_value(l_cur,i,l_val);
          if(l_val is null) then
            if(null_as_empty_string) then 
              inner_obj.put(l_dtbl(i).col_name, ''); --treatet as emptystring?
            else 
              inner_obj.put(l_dtbl(i).col_name, json_value.makenull); --null
            end if;
          else
            inner_obj.put(l_dtbl(i).col_name, json_value(l_val)); --null
          end if;
          --dbms_output.put_line(l_dtbl(i).col_name||' --> '||l_val||'varchar2' ||l_dtbl(i).col_type);
        --handling number types
        when l_dtbl(i).col_type = 2 then -- number
          dbms_sql.column_value(l_cur,i,l_val);
          conv := l_val;
          inner_obj.put(l_dtbl(i).col_name, conv);
          -- dbms_output.put_line(l_dtbl(i).col_name||' --> '||l_val||'number ' ||l_dtbl(i).col_type);
        when l_dtbl(i).col_type = 12 then -- date
          if(include_dates) then
            dbms_sql.column_value(l_cur,i,read_date);
            inner_obj.put(l_dtbl(i).col_name, json_ext.to_json_value(read_date));
          end if;
          --dbms_output.put_line(l_dtbl(i).col_name||' --> '||l_val||'date ' ||l_dtbl(i).col_type);
        when l_dtbl(i).col_type = 112 then --clob
          if(include_clobs) then
            dbms_sql.column_value(l_cur,i,read_clob);
            inner_obj.put(l_dtbl(i).col_name, json_value(read_clob));
          end if;
        when l_dtbl(i).col_type = 113 then --blob
          if(include_blobs) then
            dbms_sql.column_value(l_cur,i,read_blob);
            if(dbms_lob.getlength(read_blob) > 0) then
              inner_obj.put(l_dtbl(i).col_name, json_ext.encode(read_blob));
            else
              inner_obj.put(l_dtbl(i).col_name, json_value.makenull);
            end if;
          end if;
        
        else null; --discard other types
        end case;
      end loop;
      outer_list.append(inner_obj.to_json_value);
    end loop;
    dbms_sql.close_cursor(l_cur);
    return outer_list;
  end executeList;

  /* object with lists */
  function executeObject(stmt varchar2, bindvar json, cur_num number) return json as
    l_cur number;
    l_dtbl dbms_sql.desc_tab;
    l_cnt number;
    l_status number;
    l_val varchar2(4000);
    inner_list_names json_list := json_list();
    inner_list_data json_list := json_list();
    data_list json_list;
    outer_obj json := json();
    conv number;
    read_date date;
    read_clob clob;
    read_blob blob;
    col_type number;
  begin
    if(cur_num is not null) then 
      l_cur := cur_num; 
    else
      l_cur := dbms_sql.open_cursor;
      dbms_sql.parse(l_cur, stmt, dbms_sql.native);
      if(bindvar is not null) then bind_json(l_cur, bindvar); end if;
    end if;
    dbms_sql.describe_columns(l_cur, l_cnt, l_dtbl);
    for i in 1..l_cnt loop
      col_type := l_dtbl(i).col_type;
      if(col_type = 12) then
        dbms_sql.define_column(l_cur,i,read_date);
      elsif(col_type = 112) then
        dbms_sql.define_column(l_cur,i,read_clob);
      elsif(col_type = 113) then
        dbms_sql.define_column(l_cur,i,read_blob);
      elsif(col_type in (1,2,96)) then
        dbms_sql.define_column(l_cur,i,l_val,4000);
      end if;
    end loop;
    if(cur_num is null) then l_status := dbms_sql.execute(l_cur); end if;
    
    --build up name_list
    for i in 1..l_cnt loop
      case l_dtbl(i).col_type
        when 1 then inner_list_names.append(l_dtbl(i).col_name);
        when 96 then inner_list_names.append(l_dtbl(i).col_name);
        when 2 then inner_list_names.append(l_dtbl(i).col_name);
        when 12 then if(include_dates) then inner_list_names.append(l_dtbl(i).col_name); end if;
        when 112 then if(include_clobs) then inner_list_names.append(l_dtbl(i).col_name); end if;
        when 113 then if(include_blobs) then inner_list_names.append(l_dtbl(i).col_name); end if;
        else null;
      end case;
    end loop;

    --loop through rows 
    while ( dbms_sql.fetch_rows(l_cur) > 0 ) loop
      data_list := json_list();
      --loop through columns
      for i in 1..l_cnt loop
        case true 
        --handling string types
        when l_dtbl(i).col_type in (1,96) then -- varchar2
          dbms_sql.column_value(l_cur,i,l_val);
          if(l_val is null) then
            if(null_as_empty_string) then 
              data_list.append(''); --treatet as emptystring?
            else 
              data_list.append(json_value.makenull); --null
            end if;
          else
            data_list.append(json_value(l_val)); --null
          end if;
          --dbms_output.put_line(l_dtbl(i).col_name||' --> '||l_val||'varchar2' ||l_dtbl(i).col_type);
        --handling number types
        when l_dtbl(i).col_type = 2 then -- number
          dbms_sql.column_value(l_cur,i,l_val);
          conv := l_val;
          data_list.append(conv);
          -- dbms_output.put_line(l_dtbl(i).col_name||' --> '||l_val||'number ' ||l_dtbl(i).col_type);
        when l_dtbl(i).col_type = 12 then -- date
          if(include_dates) then
            dbms_sql.column_value(l_cur,i,read_date);
            data_list.append(json_ext.to_json_value(read_date));
          end if;
          --dbms_output.put_line(l_dtbl(i).col_name||' --> '||l_val||'date ' ||l_dtbl(i).col_type);
        when l_dtbl(i).col_type = 112 then --clob
          if(include_clobs) then
            dbms_sql.column_value(l_cur,i,read_clob);
            data_list.append(json_value(read_clob));
          end if;
        when l_dtbl(i).col_type = 113 then --blob
          if(include_blobs) then
            dbms_sql.column_value(l_cur,i,read_blob);
            if(dbms_lob.getlength(read_blob) > 0) then
              data_list.append(json_ext.encode(read_blob));
            else 
              data_list.append(json_value.makenull);
            end if; 
          end if;
        else null; --discard other types
        end case;
      end loop;
      inner_list_data.append(data_list);
    end loop;
    
    outer_obj.put('names', inner_list_names.to_json_value);
    outer_obj.put('data', inner_list_data.to_json_value);
    dbms_sql.close_cursor(l_cur);
    return outer_obj;
  end executeObject;

end json_dyn;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_EXT with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY JSON_EXT as
  scanner_exception exception;
  pragma exception_init(scanner_exception, -20100);
  parser_exception exception;
  pragma exception_init(parser_exception, -20101);
  jext_exception exception;
  pragma exception_init(jext_exception, -20110);
  
  --extra function checks if number has no fraction
  function is_integer(v json_value) return boolean as
    myint number(38); --the oracle way to specify an integer
  begin
    if(v.is_number) then
      myint := v.get_number;
      return (myint = v.get_number); --no rounding errors?
    else
      return false;
    end if;
  end;
  
  --extension enables json to store dates without comprimising the implementation
  function to_json_value(d date) return json_value as
  begin
    return json_value(to_char(d, format_string));
  end;
  
  --notice that a date type in json is also a varchar2
  function is_date(v json_value) return boolean as
    temp date;
  begin
    temp := json_ext.to_date2(v);
    return true;
  exception
    when others then 
      return false;
  end;
  
  --convertion is needed to extract dates
  function to_date2(v json_value) return date as
  begin
    if(v.is_string) then
      return to_date(v.get_string, format_string);
    else
      raise_application_error(-20110, 'Anydata did not contain a date-value');
    end if;
  exception
    when others then
      raise_application_error(-20110, 'Anydata did not contain a date on the format: '||format_string);
  end;
  
  --Json Path parser
  function parsePath(json_path varchar2, base number default 1) return json_list as
    build_path varchar2(32767) := '[';
    buf varchar2(4);
    endstring varchar2(1);
    indx number := 1;
    ret json_list;
    
    procedure next_char as
    begin
      if(indx <= length(json_path)) then
        buf := substr(json_path, indx, 1);
        indx := indx + 1;
      else 
        buf := null;
      end if;
    end;  
    --skip ws
    procedure skipws as begin while(buf in (chr(9),chr(10),chr(13),' ')) loop next_char; end loop; end;
  
  begin
    next_char();
    while(buf is not null) loop
      if(buf = '.') then
        next_char();
        if(buf is null) then raise_application_error(-20110, 'JSON Path parse error: . is not a valid json_path end'); end if;
        if(not regexp_like(buf, '^[[:alnum:]\_ ]+', 'c') ) then
          raise_application_error(-20110, 'JSON Path parse error: alpha-numeric character or space expected at position '||indx);
        end if;
        
        if(build_path != '[') then build_path := build_path || ','; end if;
        build_path := build_path || '"';
        while(regexp_like(buf, '^[[:alnum:]\_ ]+', 'c') ) loop
          build_path := build_path || buf;
          next_char();
        end loop;
        build_path := build_path || '"';
      elsif(buf = '[') then
        next_char();
        skipws();
        if(buf is null) then raise_application_error(-20110, 'JSON Path parse error: [ is not a valid json_path end'); end if;
        if(buf in ('1','2','3','4','5','6','7','8','9') or (buf = '0' and base = 0)) then
          if(build_path != '[') then build_path := build_path || ','; end if;
          while(buf in ('0','1','2','3','4','5','6','7','8','9')) loop
            build_path := build_path || buf;
            next_char();
          end loop;      
        elsif (regexp_like(buf, '^(\"|\'')', 'c')) then
          endstring := buf;
          if(build_path != '[') then build_path := build_path || ','; end if;
          build_path := build_path || '"';
          next_char();
          if(buf is null) then raise_application_error(-20110, 'JSON Path parse error: premature json_path end'); end if;
          while(buf != endstring) loop
            build_path := build_path || buf;
            next_char();
            if(buf is null) then raise_application_error(-20110, 'JSON Path parse error: premature json_path end'); end if;
            if(buf = '\') then 
              next_char(); 
              build_path := build_path || '\' || buf; 
              next_char(); 
            end if;
          end loop;
          build_path := build_path || '"';
          next_char(); 
        else
          raise_application_error(-20110, 'JSON Path parse error: expected a string or an positive integer at '||indx);
        end if;
        skipws();
        if(buf is null) then raise_application_error(-20110, 'JSON Path parse error: premature json_path end'); end if;
        if(buf != ']') then raise_application_error(-20110, 'JSON Path parse error: no array ending found. found: '|| buf); end if;
        next_char();
        skipws();
      elsif(build_path = '[') then
        if(not regexp_like(buf, '^[[:alnum:]\_ ]+', 'c') ) then
          raise_application_error(-20110, 'JSON Path parse error: alpha-numeric character or space expected at position '||indx);
        end if;
        build_path := build_path || '"';
        while(regexp_like(buf, '^[[:alnum:]\_ ]+', 'c') ) loop
          build_path := build_path || buf;
          next_char();
        end loop;
        build_path := build_path || '"';
      else 
        raise_application_error(-20110, 'JSON Path parse error: expected . or [ found '|| buf || ' at position '|| indx);
      end if;
        
    end loop;
  
    build_path := build_path || ']';
    build_path := replace(replace(replace(replace(replace(build_path, chr(9), '\t'), chr(10), '\n'), chr(13), '\f'), chr(8), '\b'), chr(14), '\r');
    
    ret := json_list(build_path);
    if(base != 1) then
      --fix base 0 to base 1
      declare
        elem json_value;
      begin
        for i in 1 .. ret.count loop
          elem := ret.get(i);
          if(elem.is_number) then
            ret.replace(i,elem.get_number()+1);
          end if;
        end loop;
      end;
    end if;
    
    return ret;
  end parsePath;
    
  --JSON Path getters
  function get_json_value(obj json, v_path varchar2, base number default 1) return json_value as 
    path json_list;
    ret json_value; 
    o json; l json_list;
  begin
    path := parsePath(v_path, base);
    ret := obj.to_json_value;
    if(path.count = 0) then return ret; end if;
    
    for i in 1 .. path.count loop
      if(path.get(i).is_string()) then
        --string fetch only on json
        o := json(ret);
        ret := o.get(path.get(i).get_string());
      else
        --number fetch on json and json_list
        if(ret.is_array()) then
          l := json_list(ret);
          ret := l.get(path.get(i).get_number());
        else 
          o := json(ret);
          l := o.get_values();
          ret := l.get(path.get(i).get_number());
        end if;
      end if;
    end loop;
    
    return ret;
  exception
    when scanner_exception then raise;
    when parser_exception then raise;
    when jext_exception then raise;
    when others then return null;
  end get_json_value;
  
  --JSON Path getters
  function get_string(obj json, path varchar2, base number default 1) return varchar2 as 
    temp json_value;
  begin 
    temp := get_json_value(obj, path, base);
    if(temp is null or not temp.is_string) then 
      return null; 
    else 
      return temp.get_string;
    end if;
  end;
  
  function get_number(obj json, path varchar2, base number default 1) return number as 
    temp json_value;
  begin 
    temp := get_json_value(obj, path, base);
    if(temp is null or not temp.is_number) then 
      return null; 
    else 
      return temp.get_number;
    end if;
  end;
  
  function get_json(obj json, path varchar2, base number default 1) return json as 
    temp json_value;
  begin 
    temp := get_json_value(obj, path, base);
    if(temp is null or not temp.is_object) then 
      return null; 
    else 
      return json(temp);
    end if;
  end;
  
  function get_json_list(obj json, path varchar2, base number default 1) return json_list as 
    temp json_value;
  begin 
    temp := get_json_value(obj, path, base);
    if(temp is null or not temp.is_array) then 
      return null; 
    else 
      return json_list(temp);
    end if;
  end;
  
  function get_bool(obj json, path varchar2, base number default 1) return boolean as 
    temp json_value;
  begin 
    temp := get_json_value(obj, path, base);
    if(temp is null or not temp.is_bool) then 
      return null; 
    else 
      return temp.get_bool;
    end if;
  end;
  
  function get_date(obj json, path varchar2, base number default 1) return date as 
    temp json_value;
  begin 
    temp := get_json_value(obj, path, base);
    if(temp is null or not is_date(temp)) then 
      return null; 
    else 
      return json_ext.to_date2(temp);
    end if;
  end;
  
  /* JSON Path putter internal function */
  procedure put_internal(obj in out nocopy json, v_path varchar2, elem json_value, base number) as
    val json_value := elem;
    path json_list;
    backreference json_list := json_list();
    
    keyval json_value; keynum number; keystring varchar2(4000);
    temp json_value := obj.to_json_value;
    obj_temp  json;
    list_temp json_list;
    inserter json_value;
  begin
    path := json_ext.parsePath(v_path, base);
    if(path.count = 0) then raise_application_error(-20110, 'JSON_EXT put error: cannot put with empty string.'); end if;
  
    --build backreference
    for i in 1 .. path.count loop
      --backreference.print(false);
      keyval := path.get(i);
      if (keyval.is_number()) then
        --nummer index
        keynum := keyval.get_number();
        if((not temp.is_object()) and (not temp.is_array())) then
          if(val is null) then return; end if;
          backreference.remove_last;
          temp := json_list().to_json_value();
          backreference.append(temp);
        end if;
  
        if(temp.is_object()) then 
          obj_temp := json(temp);
          if(obj_temp.count < keynum) then 
            if(val is null) then return; end if;
            raise_application_error(-20110, 'JSON_EXT put error: access object with to few members.'); 
          end if;
          temp := obj_temp.get(keynum);
        else 
          list_temp := json_list(temp);
          if(list_temp.count < keynum) then 
            if(val is null) then return; end if;
            --raise error or quit if val is null
            for i in list_temp.count+1 .. keynum loop
              list_temp.append(json_value.makenull);
            end loop;
            backreference.remove_last;
            backreference.append(list_temp);
          end if;
  
          temp := list_temp.get(keynum);
        end if;
      else 
        --streng index
        keystring := keyval.get_string();
        if(not temp.is_object()) then 
          --backreference.print;
          if(val is null) then return; end if;
          backreference.remove_last;
          temp := json().to_json_value();
          backreference.append(temp);
          --raise_application_error(-20110, 'JSON_ext put error: trying to access a non object with a string.'); 
        end if;
        obj_temp := json(temp);
        temp := obj_temp.get(keystring);
      end if;
  
      if(temp is null) then 
        if(val is null) then return; end if;
        --what to expect?
        keyval := path.get(i+1);
        if(keyval is not null and keyval.is_number()) then
          temp := json_list().to_json_value; 
        else 
          temp := json().to_json_value; 
        end if;
      end if;
      backreference.append(temp);
    end loop;
      
  --  backreference.print(false);
  --  path.print(false);
      
    --use backreference and path together
    inserter := val;  
    for i in reverse 1 .. backreference.count loop
  --    inserter.print(false);
      if( i = 1 ) then
        keyval := path.get(1);
        if(keyval.is_string()) then
          keystring := keyval.get_string();
        else 
          keynum := keyval.get_number();
          declare
            t1 json_value := obj.get(keynum);
          begin
            keystring := t1.mapname;
          end;
        end if;
        if(inserter is null) then obj.remove(keystring); else obj.put(keystring, inserter); end if;
      else
        temp := backreference.get(i-1);
        if(temp.is_object()) then
          keyval := path.get(i);
          obj_temp := json(temp);
          if(keyval.is_string()) then
            keystring := keyval.get_string();
          else 
            keynum := keyval.get_number();
            declare
              t1 json_value := obj_temp.get(keynum);
            begin
              keystring := t1.mapname;
            end;
          end if;
          if(inserter is null) then 
            obj_temp.remove(keystring); 
            if(obj_temp.count > 0) then inserter := obj_temp.to_json_value; end if;
          else 
            obj_temp.put(keystring, inserter);
            inserter := obj_temp.to_json_value; 
          end if;
        else 
          --array only number
          keynum := path.get(i).get_number();
          list_temp := json_list(temp);
          list_temp.remove(keynum);
          if(not inserter is null) then 
            list_temp.append(inserter, keynum);
            inserter := list_temp.to_json_value; 
          else 
            if(list_temp.count > 0) then inserter := list_temp.to_json_value; end if;
          end if; 
        end if;    
      end if;
      
    end loop;

  end put_internal;

  /* JSON Path putters */  
  procedure put(obj in out nocopy json, path varchar2, elem varchar2, base number default 1) as
  begin 
    put_internal(obj, path, json_value(elem), base);
  end;
  
  procedure put(obj in out nocopy json, path varchar2, elem number, base number default 1) as
  begin 
    if(elem is null) then raise_application_error(-20110, 'Cannot put null-value'); end if;
    put_internal(obj, path, json_value(elem), base);
  end;

  procedure put(obj in out nocopy json, path varchar2, elem json, base number default 1) as
  begin 
    if(elem is null) then raise_application_error(-20110, 'Cannot put null-value'); end if;
    put_internal(obj, path, elem.to_json_value, base);
  end;

  procedure put(obj in out nocopy json, path varchar2, elem json_list, base number default 1) as
  begin 
    if(elem is null) then raise_application_error(-20110, 'Cannot put null-value'); end if;
    put_internal(obj, path, elem.to_json_value, base);
  end;

  procedure put(obj in out nocopy json, path varchar2, elem boolean, base number default 1) as
  begin 
    if(elem is null) then raise_application_error(-20110, 'Cannot put null-value'); end if;
    put_internal(obj, path, json_value(elem), base);
  end;

  procedure put(obj in out nocopy json, path varchar2, elem json_value, base number default 1) as
  begin 
    if(elem is null) then raise_application_error(-20110, 'Cannot put null-value'); end if;
    put_internal(obj, path, elem, base);
  end;

  procedure put(obj in out nocopy json, path varchar2, elem date, base number default 1) as
  begin 
    if(elem is null) then raise_application_error(-20110, 'Cannot put null-value'); end if;
    put_internal(obj, path, json_ext.to_json_value(elem), base);
  end;

  procedure remove(obj in out nocopy json, path varchar2, base number default 1) as
  begin
    json_ext.put_internal(obj,path,null,base);
--    if(json_ext.get_json_value(obj,path) is not null) then
--    end if;
  end remove;

    --Pretty print with JSON Path
  function pp(obj json, v_path varchar2) return varchar2 as
    json_part json_value;
  begin
    json_part := json_ext.get_json_value(obj, v_path);
    if(json_part is null) then 
      return ''; 
    else 
      return json_printer.pretty_print_any(json_part); --escapes a possible internal string
    end if;
  end pp;
  
  procedure pp(obj json, v_path varchar2) as --using dbms_output.put_line
  begin
    dbms_output.put_line(pp(obj, v_path));
  end pp;
  
  -- spaces = false!
  procedure pp_htp(obj json, v_path varchar2) as --using htp.print
    json_part json_value;
  begin
    json_part := json_ext.get_json_value(obj, v_path);
    if(json_part is null) then htp.print; else 
      htp.print(json_printer.pretty_print_any(json_part, false)); 
    end if;
  end pp_htp;
  
  function base64(binarydata blob) return json_list as
    obj json_list := json_list();
    c clob := empty_clob();
    benc blob;    
  
    v_blob_offset NUMBER := 1;
    v_clob_offset NUMBER := 1;
    v_lang_context NUMBER := DBMS_LOB.DEFAULT_LANG_CTX;
    v_warning NUMBER;
    v_amount PLS_INTEGER;
--    temp varchar2(32767);

    FUNCTION encodeBlob2Base64(pBlobIn IN BLOB) RETURN BLOB IS
      vAmount NUMBER := 45;
      vBlobEnc BLOB := empty_blob();
      vBlobEncLen NUMBER := 0;
      vBlobInLen NUMBER := 0;
      vBuffer RAW(45);
      vOffset NUMBER := 1;
    BEGIN
--      dbms_output.put_line('Start base64 encoding.');
      vBlobInLen := dbms_lob.getlength(pBlobIn);
--      dbms_output.put_line('<BlobInLength>' || vBlobInLen);
      dbms_lob.createtemporary(vBlobEnc, TRUE);
      LOOP
        IF vOffset >= vBlobInLen THEN
          EXIT;
        END IF;
        dbms_lob.read(pBlobIn, vAmount, vOffset, vBuffer);
        BEGIN
          dbms_lob.append(vBlobEnc, utl_encode.base64_encode(vBuffer));
        EXCEPTION
          WHEN OTHERS THEN
          dbms_output.put_line('<vAmount>' || vAmount || '<vOffset>' || vOffset || '<vBuffer>' || vBuffer);
          dbms_output.put_line('ERROR IN append: ' || SQLERRM);
          RAISE;
        END;
        vOffset := vOffset + vAmount;
      END LOOP;
      vBlobEncLen := dbms_lob.getlength(vBlobEnc);
--      dbms_output.put_line('<BlobEncLength>' || vBlobEncLen);
--      dbms_output.put_line('Finshed base64 encoding.');
      RETURN vBlobEnc;
    END encodeBlob2Base64;
  begin
    benc := encodeBlob2Base64(binarydata);
    dbms_lob.createtemporary(c, TRUE);
    v_amount := DBMS_LOB.GETLENGTH(benc);
    DBMS_LOB.CONVERTTOCLOB(c, benc, v_amount, v_clob_offset, v_blob_offset, 1, v_lang_context, v_warning);
  
    v_amount := DBMS_LOB.GETLENGTH(c);
    v_clob_offset := 1;
    --dbms_output.put_line('V amount: '||v_amount);
    while(v_clob_offset < v_amount) loop
      --dbms_output.put_line(v_offset);
      --temp := ;
      --dbms_output.put_line('size: '||length(temp));
      obj.append(dbms_lob.SUBSTR(c, 4000,v_clob_offset));
      v_clob_offset := v_clob_offset + 4000;
    end loop;
    dbms_lob.freetemporary(benc);
    dbms_lob.freetemporary(c);
  --dbms_output.put_line(obj.count);
  --dbms_output.put_line(obj.get_last().to_char);
    return obj;
  
  end base64;


  function base64(l json_list) return blob as
    c clob := empty_clob();
    b blob := empty_blob();
    bret blob;
  
    v_blob_offset NUMBER := 1;
    v_clob_offset NUMBER := 1;
    v_lang_context NUMBER := 0; --DBMS_LOB.DEFAULT_LANG_CTX;
    v_warning NUMBER;
    v_amount PLS_INTEGER;

    FUNCTION decodeBase642Blob(pBlobIn IN BLOB) RETURN BLOB IS
      vAmount NUMBER := 256;--32;
      vBlobDec BLOB := empty_blob();
      vBlobDecLen NUMBER := 0;
      vBlobInLen NUMBER := 0;
      vBuffer RAW(256);--32);
      vOffset NUMBER := 1;
    BEGIN
--      dbms_output.put_line('Start base64 decoding.');
      vBlobInLen := dbms_lob.getlength(pBlobIn);
--      dbms_output.put_line('<BlobInLength>' || vBlobInLen);
      dbms_lob.createtemporary(vBlobDec, TRUE);
      LOOP
        IF vOffset >= vBlobInLen THEN
          EXIT;
        END IF;
        dbms_lob.read(pBlobIn, vAmount, vOffset, vBuffer);
        BEGIN
          dbms_lob.append(vBlobDec, utl_encode.base64_decode(vBuffer));
        EXCEPTION
          WHEN OTHERS THEN
          dbms_output.put_line('<vAmount>' || vAmount || '<vOffset>' || vOffset || '<vBuffer>' || vBuffer);
          dbms_output.put_line('ERROR IN append: ' || SQLERRM);
          RAISE;
        END;
        vOffset := vOffset + vAmount;
      END LOOP;
      vBlobDecLen := dbms_lob.getlength(vBlobDec);
--      dbms_output.put_line('<BlobDecLength>' || vBlobDecLen);
--      dbms_output.put_line('Finshed base64 decoding.');
      RETURN vBlobDec;
    END decodeBase642Blob;
  begin
    dbms_lob.createtemporary(c, TRUE);
    for i in 1 .. l.count loop
      dbms_lob.append(c, l.get(i).get_string());
    end loop;
    v_amount := DBMS_LOB.GETLENGTH(c);
--    dbms_output.put_line('L C'||v_amount);
    
    dbms_lob.createtemporary(b, TRUE);
    DBMS_LOB.CONVERTTOBLOB(b, c, dbms_lob.lobmaxsize, v_clob_offset, v_blob_offset, 1, v_lang_context, v_warning);
    dbms_lob.freetemporary(c);
    v_amount := DBMS_LOB.GETLENGTH(b);
--    dbms_output.put_line('L B'||v_amount);
    
    bret := decodeBase642Blob(b); 
    dbms_lob.freetemporary(b);
    return bret;
  
  end base64;

  function encode(binarydata blob) return json_value as
    obj json_value;
    c clob := empty_clob();
    benc blob;    
  
    v_blob_offset NUMBER := 1;
    v_clob_offset NUMBER := 1;
    v_lang_context NUMBER := DBMS_LOB.DEFAULT_LANG_CTX;
    v_warning NUMBER;
    v_amount PLS_INTEGER;
--    temp varchar2(32767);

    FUNCTION encodeBlob2Base64(pBlobIn IN BLOB) RETURN BLOB IS
      vAmount NUMBER := 45;
      vBlobEnc BLOB := empty_blob();
      vBlobEncLen NUMBER := 0;
      vBlobInLen NUMBER := 0;
      vBuffer RAW(45);
      vOffset NUMBER := 1;
    BEGIN
--      dbms_output.put_line('Start base64 encoding.');
      vBlobInLen := dbms_lob.getlength(pBlobIn);
--      dbms_output.put_line('<BlobInLength>' || vBlobInLen);
      dbms_lob.createtemporary(vBlobEnc, TRUE);
      LOOP
        IF vOffset >= vBlobInLen THEN
          EXIT;
        END IF;
        dbms_lob.read(pBlobIn, vAmount, vOffset, vBuffer);
        BEGIN
          dbms_lob.append(vBlobEnc, utl_encode.base64_encode(vBuffer));
        EXCEPTION
          WHEN OTHERS THEN
          dbms_output.put_line('<vAmount>' || vAmount || '<vOffset>' || vOffset || '<vBuffer>' || vBuffer);
          dbms_output.put_line('ERROR IN append: ' || SQLERRM);
          RAISE;
        END;
        vOffset := vOffset + vAmount;
      END LOOP;
      vBlobEncLen := dbms_lob.getlength(vBlobEnc);
--      dbms_output.put_line('<BlobEncLength>' || vBlobEncLen);
--      dbms_output.put_line('Finshed base64 encoding.');
      RETURN vBlobEnc;
    END encodeBlob2Base64;
  begin
    benc := encodeBlob2Base64(binarydata);
    dbms_lob.createtemporary(c, TRUE);
    v_amount := DBMS_LOB.GETLENGTH(benc);
    DBMS_LOB.CONVERTTOCLOB(c, benc, v_amount, v_clob_offset, v_blob_offset, 1, v_lang_context, v_warning);
    
    obj := json_value(c);  

    dbms_lob.freetemporary(benc);
    dbms_lob.freetemporary(c);
  --dbms_output.put_line(obj.count);
  --dbms_output.put_line(obj.get_last().to_char);
    return obj;
  
  end encode;
  
  function decode(v json_value) return blob as
    c clob := empty_clob();
    b blob := empty_blob();
    bret blob;
  
    v_blob_offset NUMBER := 1;
    v_clob_offset NUMBER := 1;
    v_lang_context NUMBER := 0; --DBMS_LOB.DEFAULT_LANG_CTX;
    v_warning NUMBER;
    v_amount PLS_INTEGER;

    FUNCTION decodeBase642Blob(pBlobIn IN BLOB) RETURN BLOB IS
      vAmount NUMBER := 256;--32;
      vBlobDec BLOB := empty_blob();
      vBlobDecLen NUMBER := 0;
      vBlobInLen NUMBER := 0;
      vBuffer RAW(256);--32);
      vOffset NUMBER := 1;
    BEGIN
--      dbms_output.put_line('Start base64 decoding.');
      vBlobInLen := dbms_lob.getlength(pBlobIn);
--      dbms_output.put_line('<BlobInLength>' || vBlobInLen);
      dbms_lob.createtemporary(vBlobDec, TRUE);
      LOOP
        IF vOffset >= vBlobInLen THEN
          EXIT;
        END IF;
        dbms_lob.read(pBlobIn, vAmount, vOffset, vBuffer);
        BEGIN
          dbms_lob.append(vBlobDec, utl_encode.base64_decode(vBuffer));
        EXCEPTION
          WHEN OTHERS THEN
          dbms_output.put_line('<vAmount>' || vAmount || '<vOffset>' || vOffset || '<vBuffer>' || vBuffer);
          dbms_output.put_line('ERROR IN append: ' || SQLERRM);
          RAISE;
        END;
        vOffset := vOffset + vAmount;
      END LOOP;
      vBlobDecLen := dbms_lob.getlength(vBlobDec);
--      dbms_output.put_line('<BlobDecLength>' || vBlobDecLen);
--      dbms_output.put_line('Finshed base64 decoding.');
      RETURN vBlobDec;
    END decodeBase642Blob;
  begin
    dbms_lob.createtemporary(c, TRUE);
    v.get_string(c);
    v_amount := DBMS_LOB.GETLENGTH(c);
--    dbms_output.put_line('L C'||v_amount);
    
    dbms_lob.createtemporary(b, TRUE);
    DBMS_LOB.CONVERTTOBLOB(b, c, dbms_lob.lobmaxsize, v_clob_offset, v_blob_offset, 1, v_lang_context, v_warning);
    dbms_lob.freetemporary(c);
    v_amount := DBMS_LOB.GETLENGTH(b);
--    dbms_output.put_line('L B'||v_amount);
    
    bret := decodeBase642Blob(b); 
    dbms_lob.freetemporary(b);
    return bret;
  
  end decode;


end json_ext;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_HELPER with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY JSON_HELPER as
  
  --recursive merge
  function merge( p_a_json json, p_b_json json) return json as
    l_json    JSON;
    l_jv      json_value;
    l_indx    number;
    l_recursive json_value;
  begin
    --
    -- Initialize our return object
    --
    l_json := p_a_json;
    
    -- loop through p_b_json
    l_indx := p_b_json.json_data.first;
    loop
      exit when l_indx is null;
      l_jv   := p_b_json.json_data(l_indx);
      if(l_jv.is_object) then
        --recursive
        l_recursive := l_json.get(l_jv.mapname);
        if(l_recursive is not null and l_recursive.is_object) then
          l_json.put(l_jv.mapname, merge(json(l_recursive), json(l_jv)));
        else 
          l_json.put(l_jv.mapname, l_jv);
        end if;
      else
        l_json.put(l_jv.mapname, l_jv);
      end if;
      
      --increment
      l_indx := p_b_json.json_data.next(l_indx);
    end loop;
    
    return l_json;
    
  end merge;

  -- join two lists
  function join( p_a_list json_list, p_b_list json_list) return json_list as
    l_json_list json_list := p_a_list;
  begin
    for indx in 1 .. p_b_list.count loop
      l_json_list.append(p_b_list.get(indx));
    end loop;
    
    return l_json_list;
  
  end join;

  -- keep keys.
  function keep( p_json json, p_keys json_list) return json as
    l_json json := json();
    mapname varchar2(4000);
  begin
    for i in 1 .. p_keys.count loop
      mapname := p_keys.get(i).get_string;
      if(p_json.exist(mapname)) then
        l_json.put(mapname, p_json.get(mapname)); 
      end if;
    end loop;
  
    return l_json;
  end keep;
  
  -- drop keys.
  function remove( p_json json, p_keys json_list) return json as
    l_json json := p_json;
  begin
    for i in 1 .. p_keys.count loop
      l_json.remove(p_keys.get(i).get_string);
    end loop;
  
    return l_json;
  end remove;
  
  --equals functions
  
  function equals(p_v1 json_value, p_v2 number) return boolean as
  begin
    if(p_v2 is null) then
      return p_v1.is_null;
    end if;
    
    if(not p_v1.is_number) then
      return false;
    end if;
    
    return p_v2 = p_v1.get_number;
  end;

  function equals(p_v1 json_value, p_v2 boolean) return boolean as
  begin
    if(p_v2 is null) then
      return p_v1.is_null;
    end if;
    
    if(not p_v1.is_bool) then
      return false;
    end if;
    
    return p_v2 = p_v1.get_bool;
  end;
  
  function equals(p_v1 json_value, p_v2 varchar2) return boolean as
  begin
    if(p_v2 is null) then
      return p_v1.is_null;
    end if;
    
    if(not p_v1.is_string) then
      return false;
    end if;
    
    return p_v2 = p_v1.get_string;
  end;
  
  function equals(p_v1 json_value, p_v2 clob) return boolean as
    my_clob clob;
    res boolean;
  begin
    if(p_v2 is null) then
      return p_v1.is_null;
    end if;
    
    if(not p_v1.is_string) then
      return false;
    end if;
    
    my_clob := empty_clob();
    dbms_lob.createtemporary(my_clob, true);
    p_v1.get_string(my_clob);
    
    res := dbms_lob.compare(p_v2, my_clob) = 0;
    dbms_lob.freetemporary(my_clob);
  end;
  
  function equals(p_v1 json_value, p_v2 json_value, exact boolean) return boolean as
  begin
    if(p_v2 is null) then
      return p_v1.is_null;
    end if;
    
    if(p_v2.is_number) then return equals(p_v1, p_v2.get_number); end if;
    if(p_v2.is_bool) then return equals(p_v1, p_v2.get_bool); end if;
    if(p_v2.is_object) then return equals(p_v1, json(p_v2), exact); end if;
    if(p_v2.is_array) then return equals(p_v1, json_list(p_v2), exact); end if;
    if(p_v2.is_string) then 
      if(p_v2.extended_str is null) then
        return equals(p_v1, p_v2.get_string);
      else
        declare
          my_clob clob; res boolean;
        begin
          my_clob := empty_clob();
          dbms_lob.createtemporary(my_clob, true);
          p_v2.get_string(my_clob);
          res := equals(p_v1, my_clob);
          dbms_lob.freetemporary(my_clob);
          return res;
        end;
      end if;
    end if;

    return false; --should never happen
  end;
  
  function equals(p_v1 json_value, p_v2 json_list, exact boolean) return boolean as
    cmp json_list;
    res boolean := true;
  begin
--  p_v1.print(false);
--  p_v2.print(false);
--  dbms_output.put_line('labc1'||case when exact then 'X' else 'U' end);

    if(p_v2 is null) then
      return p_v1.is_null;
    end if;
    
    if(not p_v1.is_array) then
      return false;
    end if;
  
--  dbms_output.put_line('labc2'||case when exact then 'X' else 'U' end);

    cmp := json_list(p_v1);
    if(cmp.count != p_v2.count and exact) then return false; end if;
  
--  dbms_output.put_line('labc3'||case when exact then 'X' else 'U' end);

    if(exact) then
      for i in 1 .. cmp.count loop
        res := equals(cmp.get(i), p_v2.get(i), exact);
        if(not res) then return res; end if;
      end loop;
    else 
--  dbms_output.put_line('labc4'||case when exact then 'X' else 'U' end);
      if(p_v2.count > cmp.count) then return false; end if;
--  dbms_output.put_line('labc5'||case when exact then 'X' else 'U' end);
      
      --match sublist here!
      for x in 0 .. (cmp.count-p_v2.count) loop
--  dbms_output.put_line('labc7'||x);

        for i in 1 .. p_v2.count loop
          res := equals(cmp.get(x+i), p_v2.get(i), exact);
          if(not res) then 
            goto next_index; 
          end if;
        end loop;
        return true;
        
        <<next_index>>
        null;
      end loop;
      
--  dbms_output.put_line('labc7'||case when exact then 'X' else 'U' end);

    return false; --no match
    
    end if;
    
    return res;
  end;
  
  function equals(p_v1 json_value, p_v2 json, exact boolean) return boolean as
    cmp json;
    res boolean := true;
  begin
--  p_v1.print(false);
--  p_v2.print(false);
--  dbms_output.put_line('abc1');
    
    if(p_v2 is null) then
      return p_v1.is_null;
    end if;
    
    if(not p_v1.is_object) then
      return false;
    end if;
    
    cmp := json(p_v1);
    
--  dbms_output.put_line('abc2');

    if(cmp.count != p_v2.count and exact) then return false; end if;
    
--  dbms_output.put_line('abc3');
    declare
      k1 json_list := p_v2.get_keys;
      key_index number;
    begin
      for i in 1 .. k1.count loop
        key_index := cmp.index_of(k1.get(i).get_string);
        if(key_index = -1) then return false; end if;
        if(exact) then 
          if(not equals(p_v2.get(i), cmp.get(key_index),true)) then return false; end if;
        else 
          --non exact
          declare
            v1 json_value := cmp.get(key_index);
            v2 json_value := p_v2.get(i);
          begin
--  dbms_output.put_line('abc3 1/2');
--            v1.print(false);
--            v2.print(false);

            if(v1.is_object and v2.is_object) then 
              if(not equals(v1, v2, false)) then return false; end if;
            elsif(v1.is_array and v2.is_array) then
              if(not equals(v1, v2, false)) then return false; end if;
            else
              if(not equals(v1, v2, true)) then return false; end if;
            end if;
          end;
        
        end if;
      end loop;
    end;
    
--  dbms_output.put_line('abc4');

    return true;
  end;
  
  function equals(p_v1 json, p_v2 json, exact boolean) return boolean as
  begin
    return equals(p_v1.to_json_value, p_v2, exact);
  end;
  
  function equals(p_v1 json_list, p_v2 json_list, exact boolean) return boolean as
  begin
    return equals(p_v1.to_json_value, p_v2, exact);
  end;
  
  --contain
  function contains(p_v1 json, p_v2 json_value, exact boolean) return boolean as
    v_values json_list;
  begin
    if(equals(p_v1.to_json_value, p_v2, exact)) then return true; end if;
    
    v_values := p_v1.get_values;
    
    for i in 1 .. v_values.count loop
      declare
        v_val json_value := v_values.get(i);
      begin
        if(v_val.is_object) then
          if(contains(json(v_val),p_v2,exact)) then return true; end if;
        end if;
        if(v_val.is_array) then
          if(contains(json_list(v_val),p_v2, exact)) then return true; end if;
        end if;
        
        if(equals(v_val, p_v2, exact)) then return true; end if;
      end;
    
    end loop;
    
    return false;
  end;
  
  function contains(p_v1 json_list, p_v2 json_value, exact boolean) return boolean as
  begin
    if(equals(p_v1.to_json_value, p_v2, exact)) then return true; end if;

    for i in 1 .. p_v1.count loop
      declare
        v_val json_value := p_v1.get(i);
      begin
        if(v_val.is_object) then
          if(contains(json(v_val),p_v2, exact)) then return true; end if;
        end if;
        if(v_val.is_array) then
          if(contains(json_list(v_val),p_v2, exact)) then return true; end if;
        end if;
        
        if(equals(v_val, p_v2, exact)) then return true; end if;
      end;
    
    end loop;

    return false;
  end;
  
  function contains(p_v1 json, p_v2 json, exact boolean ) return boolean as 
  begin return contains(p_v1, p_v2.to_json_value,exact); end;
  function contains(p_v1 json, p_v2 json_list, exact boolean ) return boolean as 
  begin return contains(p_v1, p_v2.to_json_value,exact); end;
  function contains(p_v1 json, p_v2 number, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;
  function contains(p_v1 json, p_v2 varchar2, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;
  function contains(p_v1 json, p_v2 boolean, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;
  function contains(p_v1 json, p_v2 clob, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;

  function contains(p_v1 json_list, p_v2 json, exact boolean ) return boolean as begin 
  return contains(p_v1, p_v2.to_json_value,exact); end;
  function contains(p_v1 json_list, p_v2 json_list, exact boolean ) return boolean as begin 
  return contains(p_v1, p_v2.to_json_value,exact); end;
  function contains(p_v1 json_list, p_v2 number, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;
  function contains(p_v1 json_list, p_v2 varchar2, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;
  function contains(p_v1 json_list, p_v2 boolean, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;
  function contains(p_v1 json_list, p_v2 clob, exact boolean ) return boolean as begin 
  return contains(p_v1, json_value(p_v2),exact); end;


end json_helper;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_ML with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY JSON_ML as
  function get_jsonml_stylesheet return xmltype;

  function xml2json(xml in xmltype) return json_list as
    l_json        xmltype;
    l_returnvalue clob;
  begin
    l_json := xml.transform (get_jsonml_stylesheet);
    l_returnvalue := l_json.getclobval();
    l_returnvalue := dbms_xmlgen.convert (l_returnvalue, dbms_xmlgen.entity_decode);
    --dbms_output.put_line(l_returnvalue);
    return json_list(l_returnvalue);
  end xml2json;

  function xmlstr2json(xmlstr in varchar2) return json_list as
  begin
    return xml2json(xmltype(xmlstr));
  end xmlstr2json;

  function get_jsonml_stylesheet return xmltype as
  begin
    if(jsonml_stylesheet is null) then 
    jsonml_stylesheet := xmltype('<?xml version="1.0" encoding="UTF-8"?>
<!--
		JsonML.xslt
 
		Created: 2006-11-15-0551
		Modified: 2009-02-14-0927
 
		Released under an open-source license:
		http://jsonml.org/License.htm
 
		This transformation converts any XML document into JsonML.
		It omits processing-instructions and comment-nodes.
		
		To enable comment-nodes to be emitted as JavaScript comments,
		uncomment the Comment() template.
--> 
<xsl:stylesheet version="1.0"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
 
	<xsl:output method="text"
				media-type="application/json"
				encoding="UTF-8"
				indent="no"
				omit-xml-declaration="yes" /> 
 
	<!-- constants --> 
	<xsl:variable name="XHTML"
				  select="''http://www.w3.org/1999/xhtml''" /> 
 
	<xsl:variable name="START_ELEM"
				  select="''[''" /> 
 
	<xsl:variable name="END_ELEM"
				  select="'']''" /> 
 
	<xsl:variable name="VALUE_DELIM"
				  select="'',''" /> 
 
	<xsl:variable name="START_ATTRIB"
				  select="''{''" /> 
 
	<xsl:variable name="END_ATTRIB"
				  select="''}''" /> 
 
	<xsl:variable name="NAME_DELIM"
				  select="'':''" /> 
 
	<xsl:variable name="STRING_DELIM"
				  select="''&#x22;''" /> 
 
	<xsl:variable name="START_COMMENT"
				  select="''/*''" /> 
 
	<xsl:variable name="END_COMMENT"
				  select="''*/''" /> 
 
	<!-- root-node --> 
	<xsl:template match="/"> 
		<xsl:apply-templates select="*" /> 
	</xsl:template> 
 
	<!-- comments --> 
	<xsl:template match="comment()"> 
	<!-- uncomment to support JSON comments --> 
	<!--
		<xsl:value-of select="$START_COMMENT" />
 
		<xsl:value-of select="."
					  disable-output-escaping="yes" />
 
		<xsl:value-of select="$END_COMMENT" />
	--> 
	</xsl:template> 
 
	<!-- elements --> 
	<xsl:template match="*"> 
		<xsl:value-of select="$START_ELEM" /> 
 
		<!-- tag-name string --> 
		<xsl:value-of select="$STRING_DELIM" /> 
		<xsl:choose> 
			<xsl:when test="namespace-uri()=$XHTML"> 
				<xsl:value-of select="local-name()" /> 
			</xsl:when> 
			<xsl:otherwise> 
				<xsl:value-of select="name()" /> 
			</xsl:otherwise> 
		</xsl:choose> 
		<xsl:value-of select="$STRING_DELIM" /> 
 
		<!-- attribute object --> 
		<xsl:if test="count(@*)>0"> 
			<xsl:value-of select="$VALUE_DELIM" /> 
			<xsl:value-of select="$START_ATTRIB" /> 
			<xsl:for-each select="@*"> 
				<xsl:if test="position()>1"> 
					<xsl:value-of select="$VALUE_DELIM" /> 
				</xsl:if> 
				<xsl:apply-templates select="." /> 
			</xsl:for-each> 
			<xsl:value-of select="$END_ATTRIB" /> 
		</xsl:if> 
 
		<!-- child elements and text-nodes --> 
		<xsl:for-each select="*|text()"> 
			<xsl:value-of select="$VALUE_DELIM" /> 
			<xsl:apply-templates select="." /> 
		</xsl:for-each> 
 
		<xsl:value-of select="$END_ELEM" /> 
	</xsl:template> 
 
	<!-- text-nodes --> 
	<xsl:template match="text()"> 
		<xsl:call-template name="escape-string"> 
			<xsl:with-param name="value"
							select="." /> 
		</xsl:call-template> 
	</xsl:template> 
 
	<!-- attributes --> 
	<xsl:template match="@*"> 
		<xsl:value-of select="$STRING_DELIM" /> 
		<xsl:choose> 
			<xsl:when test="namespace-uri()=$XHTML"> 
				<xsl:value-of select="local-name()" /> 
			</xsl:when> 
			<xsl:otherwise> 
				<xsl:value-of select="name()" /> 
			</xsl:otherwise> 
		</xsl:choose> 
		<xsl:value-of select="$STRING_DELIM" /> 
 
		<xsl:value-of select="$NAME_DELIM" /> 
 
		<xsl:call-template name="escape-string"> 
			<xsl:with-param name="value"
							select="." /> 
		</xsl:call-template> 
 
	</xsl:template> 
 
	<!-- escape-string: quotes and escapes --> 
	<xsl:template name="escape-string"> 
		<xsl:param name="value" /> 
 
		<xsl:value-of select="$STRING_DELIM" /> 
 
		<xsl:if test="string-length($value)>0"> 
			<xsl:variable name="escaped-whacks"> 
				<!-- escape backslashes --> 
				<xsl:call-template name="string-replace"> 
					<xsl:with-param name="value"
									select="$value" /> 
					<xsl:with-param name="find"
									select="''\''" /> 
					<xsl:with-param name="replace"
									select="''\\''" /> 
				</xsl:call-template> 
			</xsl:variable> 
 
			<xsl:variable name="escaped-LF"> 
				<!-- escape line feeds --> 
				<xsl:call-template name="string-replace"> 
					<xsl:with-param name="value"
									select="$escaped-whacks" /> 
					<xsl:with-param name="find"
									select="''&#x0A;''" /> 
					<xsl:with-param name="replace"
									select="''\n''" /> 
				</xsl:call-template> 
			</xsl:variable> 
 
			<xsl:variable name="escaped-CR"> 
				<!-- escape carriage returns --> 
				<xsl:call-template name="string-replace"> 
					<xsl:with-param name="value"
									select="$escaped-LF" /> 
					<xsl:with-param name="find"
									select="''&#x0D;''" /> 
					<xsl:with-param name="replace"
									select="''\r''" /> 
				</xsl:call-template> 
			</xsl:variable> 
 
			<xsl:variable name="escaped-tabs"> 
				<!-- escape tabs --> 
				<xsl:call-template name="string-replace"> 
					<xsl:with-param name="value"
									select="$escaped-CR" /> 
					<xsl:with-param name="find"
									select="''&#x09;''" /> 
					<xsl:with-param name="replace"
									select="''\t''" /> 
				</xsl:call-template> 
			</xsl:variable> 
 
			<!-- escape quotes --> 
			<xsl:call-template name="string-replace"> 
				<xsl:with-param name="value"
								select="$escaped-tabs" /> 
				<xsl:with-param name="find"
								select="''&quot;''" /> 
				<xsl:with-param name="replace"
								select="''\&quot;''" /> 
			</xsl:call-template> 
		</xsl:if> 
 
		<xsl:value-of select="$STRING_DELIM" /> 
	</xsl:template> 
 
	<!-- string-replace: replaces occurances of one string with another --> 
	<xsl:template name="string-replace"> 
		<xsl:param name="value" /> 
		<xsl:param name="find" /> 
		<xsl:param name="replace" /> 
 
		<xsl:choose> 
			<xsl:when test="contains($value,$find)"> 
				<!-- replace and call recursively on next --> 
				<xsl:value-of select="substring-before($value,$find)"
							  disable-output-escaping="yes" /> 
				<xsl:value-of select="$replace"
							  disable-output-escaping="yes" /> 
				<xsl:call-template name="string-replace"> 
					<xsl:with-param name="value"
									select="substring-after($value,$find)" /> 
					<xsl:with-param name="find"
									select="$find" /> 
					<xsl:with-param name="replace"
									select="$replace" /> 
				</xsl:call-template> 
			</xsl:when> 
			<xsl:otherwise> 
				<!-- no replacement necessary --> 
				<xsl:value-of select="$value"
							  disable-output-escaping="yes" /> 
			</xsl:otherwise> 
		</xsl:choose> 
	</xsl:template> 
 
</xsl:stylesheet>');
    end if;
    return jsonml_stylesheet;
  end get_jsonml_stylesheet;

end json_ml;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_PARSER with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY "JSON_PARSER" as
  /*
  Copyright (c) 2009 Jonas Krogsboell

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
  
  decimalpoint varchar2(1 char) := '.';
  
  procedure updateDecimalPoint as
  begin
    SELECT substr(VALUE,1,1) into decimalpoint FROM NLS_SESSION_PARAMETERS WHERE PARAMETER = 'NLS_NUMERIC_CHARACTERS';
  end updateDecimalPoint;

  /*type json_src is record (len number, offset number, src varchar2(10), s_clob clob); */
  function next_char(indx number, s in out nocopy json_src) return varchar2 as
  begin
    if(indx > s.len) then return null; end if;
    --right offset?
    if(indx > 4000 + s.offset or indx < s.offset) then
    --load right offset
      s.offset := indx - (indx mod 4000);
      s.src := dbms_lob.substr(s.s_clob, 4000, s.offset+1);
    end if;
    --read from s.src
    return substr(s.src, indx-s.offset, 1);         
  end;
  
  function next_char2(indx number, s in out nocopy json_src, amount number default 1) return varchar2 as
    buf varchar2(32767) := '';
  begin
    for i in 1..amount loop
      buf := buf || next_char(indx-1+i,s);
    end loop;
    return buf;
  end;
  
  function prepareClob(buf clob) return json_parser.json_src as
    temp json_parser.json_src;
  begin
    temp.s_clob := buf;
    temp.offset := 0;
    temp.src := dbms_lob.substr(buf, 4000, temp.offset+1);
    temp.len := dbms_lob.getlength(buf);
    return temp;
  end;
  
  function prepareVarchar2(buf varchar2) return json_parser.json_src as
    temp json_parser.json_src;
  begin
    temp.s_clob := buf;
    temp.offset := 0;
    temp.src := substr(buf, 1, 4000);
    temp.len := length(buf);
    return temp;
  end;

  procedure debug(text varchar2) as
  begin
    dbms_output.put_line(text);
  end;
  
  procedure print_token(t rToken) as
  begin
    dbms_output.put_line('Line: '||t.line||' - Column: '||t.col||' - Type: '||t.type_name||' - Content: '||t.data);
  end print_token;
  
  /* SCANNER FUNCTIONS START */
  procedure s_error(text varchar2, line number, col number) as
  begin
    raise_application_error(-20100, 'JSON Scanner exception @ line: '||line||' column: '||col||' - '||text);
  end;

  procedure s_error(text varchar2, tok rToken) as
  begin
    raise_application_error(-20100, 'JSON Scanner exception @ line: '||tok.line||' column: '||tok.col||' - '||text);
  end;
  
  function mt(t varchar2, l pls_integer, c pls_integer, d varchar2) return rToken as
    token rToken;
  begin
    token.type_name := t;
    token.line := l;
    token.col := c;
    token.data := d;
    return token;
  end;

  function lexNumber(jsrc in out nocopy json_src, tok in out nocopy rToken, indx in out nocopy pls_integer) return pls_integer as
    numbuf varchar2(4000) := '';
    buf varchar2(4);
    checkLoop boolean;
  begin
    buf := next_char(indx, jsrc); 
    if(buf = '-') then numbuf := '-'; indx := indx + 1; end if;
    buf := next_char(indx, jsrc); 
    --0 or [1-9]([0-9])* 
    if(buf = '0') then 
      numbuf := numbuf || '0'; indx := indx + 1; 
      buf := next_char(indx, jsrc);  
    elsif(buf >= '1' and buf <= '9') then 
      numbuf := numbuf || buf; indx := indx + 1; 
      --read digits
      buf := next_char(indx, jsrc); 
      while(buf >= '0' and buf <= '9') loop
        numbuf := numbuf || buf; indx := indx + 1; 
        buf := next_char(indx, jsrc);  
      end loop;      
    end if;
    --fraction
    if(buf = '.') then
      numbuf := numbuf || buf; indx := indx + 1; 
      buf := next_char(indx, jsrc); 
      checkLoop := FALSE;
      while(buf >= '0' and buf <= '9') loop
        checkLoop := TRUE;
        numbuf := numbuf || buf; indx := indx + 1; 
        buf := next_char(indx, jsrc);  
      end loop; 
      if(not checkLoop) then
        s_error('Expected: digits in fraction', tok);
      end if;
    end if;
    --exp part
    if(buf in ('e', 'E')) then
      numbuf := numbuf || buf; indx := indx + 1; 
      buf := next_char(indx, jsrc); 
      if(buf = '+' or buf = '-') then 
        numbuf := numbuf || buf; indx := indx + 1; 
        buf := next_char(indx, jsrc);  
      end if;
      checkLoop := FALSE;
      while(buf >= '0' and buf <= '9') loop
        checkLoop := TRUE;
        numbuf := numbuf || buf; indx := indx + 1; 
        buf := next_char(indx, jsrc); 
      end loop;      
      if(not checkLoop) then
        s_error('Expected: digits in exp', tok);
      end if;
    end if;
    
    tok.data := numbuf;
    return indx;
  end lexNumber;
  
  -- [a-zA-Z]([a-zA-Z0-9])*
  function lexName(jsrc in out nocopy json_src, tok in out nocopy rToken, indx in out nocopy pls_integer) return pls_integer as
    varbuf varchar2(32767) := '';
    buf varchar(4);
    num number;
  begin
    buf := next_char(indx, jsrc); 
    while(REGEXP_LIKE(buf, '^[[:alnum:]\_]$', 'i')) loop
      varbuf := varbuf || buf;
      indx := indx + 1;
      buf := next_char(indx, jsrc); 
      if (buf is null) then 
        goto retname;
        --debug('Premature string ending');
      end if;
    end loop;
    <<retname>>
    
    --could check for reserved keywords here

    --debug(varbuf);
    tok.data := varbuf;
    return indx-1;
  end lexName;
  
  procedure updateClob(v_extended in out nocopy clob, v_str varchar2) as
  begin
    dbms_lob.writeappend(v_extended, length(v_str), v_str);
  end updateClob;

  function lexString(jsrc in out nocopy json_src, tok in out nocopy rToken, indx in out nocopy pls_integer, endChar char) return pls_integer as
    v_extended clob := null; v_count number := 0;
    varbuf varchar2(32767) := '';
    buf varchar(4);
    wrong boolean;
  begin
    indx := indx +1;
    buf := next_char(indx, jsrc); 
    while(buf != endChar) loop
      --clob control
      if(v_count > 8191) then --crazy oracle error (16383 is the highest working length with unistr - 8192 choosen to be safe)
        if(v_extended is null) then 
          v_extended := empty_clob();
          dbms_lob.createtemporary(v_extended, true); 
        end if;
        updateClob(v_extended, unistr(varbuf));
        varbuf := ''; v_count := 0;
      end if;
      if(buf = Chr(13) or buf = CHR(9) or buf = CHR(10)) then
        s_error('Control characters not allowed (CHR(9),CHR(10)CHR(13))', tok);
      end if;
      if(buf = '\') then
        --varbuf := varbuf || buf;
        indx := indx + 1;
        buf := next_char(indx, jsrc);  
        case
          when buf in ('\') then
            varbuf := varbuf || buf || buf; v_count := v_count + 2;
            indx := indx + 1;
            buf := next_char(indx, jsrc);  
          when buf in ('"', '/') then
            varbuf := varbuf || buf; v_count := v_count + 1;
            indx := indx + 1;
            buf := next_char(indx, jsrc);  
          when buf = '''' then
            if(json_strict = false) then 
              varbuf := varbuf || buf; v_count := v_count + 1;
              indx := indx + 1;
              buf := next_char(indx, jsrc);  
            else 
              s_error('strictmode - expected: " \ / b f n r t u ', tok);
            end if;
          when buf in ('b', 'f', 'n', 'r', 't') then
            --backspace b = U+0008
            --formfeed  f = U+000C
            --newline   n = U+000A
            --carret    r = U+000D
            --tabulator t = U+0009
            case buf
            when 'b' then varbuf := varbuf || chr(8);
            when 'f' then varbuf := varbuf || chr(13);
            when 'n' then varbuf := varbuf || chr(10);
            when 'r' then varbuf := varbuf || chr(14);
            when 't' then varbuf := varbuf || chr(9);
            end case;            
            --varbuf := varbuf || buf;
            v_count := v_count + 1;
            indx := indx + 1;
            buf := next_char(indx, jsrc);  
          when buf = 'u' then
            --four hexidecimal chars
            declare
              four varchar2(4);
            begin
              four := next_char2(indx+1, jsrc, 4);
              wrong := FALSE;              
              if(upper(substr(four, 1,1)) not in ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f')) then wrong := TRUE; end if;
              if(upper(substr(four, 2,1)) not in ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f')) then wrong := TRUE; end if;
              if(upper(substr(four, 3,1)) not in ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f')) then wrong := TRUE; end if;
              if(upper(substr(four, 4,1)) not in ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f')) then wrong := TRUE; end if;
              if(wrong) then
                s_error('expected: " \u([0-9][A-F]){4}', tok);
              end if;
--              varbuf := varbuf || buf || four;
              varbuf := varbuf || '\'||four;--chr(to_number(four,'XXXX'));
               v_count := v_count + 5;
              indx := indx + 5;
              buf := next_char(indx, jsrc); 
              end;
          else 
            s_error('expected: " \ / b f n r t u ', tok);
        end case;
      else
        varbuf := varbuf || buf; v_count := v_count + 1;
        indx := indx + 1;
        buf := next_char(indx, jsrc); 
      end if;
    end loop;
    
    if (buf is null) then 
      s_error('string ending not found', tok);
      --debug('Premature string ending');
    end if;

    --debug(varbuf);
    --dbms_output.put_line(varbuf);
    if(v_extended is not null) then 
      updateClob(v_extended, unistr(varbuf));
      tok.data_overflow := v_extended;
      tok.data := dbms_lob.substr(v_extended, 1, 32767);
    else 
      tok.data := unistr(varbuf);
    end if;
    return indx;
  end lexString;
  
  /* scanner tokens:
    '{', '}', ',', ':', '[', ']', STRING, NUMBER, TRUE, FALSE, NULL
  */
  function lexer(jsrc in out nocopy json_src) return lTokens as
    tokens lTokens;
    indx pls_integer := 1;
    tok_indx pls_integer := 1;
    buf varchar2(4);
    lin_no number := 1;
    col_no number := 0;
  begin
    while (indx <= jsrc.len) loop
      --read into buf
      buf := next_char(indx, jsrc); 
      col_no := col_no + 1;
      --convert to switch case
      case
        when buf = '{' then tokens(tok_indx) := mt('{', lin_no, col_no, null); tok_indx := tok_indx + 1;
        when buf = '}' then tokens(tok_indx) := mt('}', lin_no, col_no, null); tok_indx := tok_indx + 1;
        when buf = ',' then tokens(tok_indx) := mt(',', lin_no, col_no, null); tok_indx := tok_indx + 1;
        when buf = ':' then tokens(tok_indx) := mt(':', lin_no, col_no, null); tok_indx := tok_indx + 1;
        when buf = '[' then tokens(tok_indx) := mt('[', lin_no, col_no, null); tok_indx := tok_indx + 1;
        when buf = ']' then tokens(tok_indx) := mt(']', lin_no, col_no, null); tok_indx := tok_indx + 1;
        when buf = 't' then
          if(next_char2(indx, jsrc, 4) != 'true') then
            if(json_strict = false and REGEXP_LIKE(buf, '^[[:alpha:]]$', 'i')) then
              tokens(tok_indx) := mt('STRING', lin_no, col_no, null); 
              indx := lexName(jsrc, tokens(tok_indx), indx);
              col_no := col_no + length(tokens(tok_indx).data) + 1;
              tok_indx := tok_indx + 1; 
            else 
              s_error('Expected: ''true''', lin_no, col_no);
            end if;
          else
            tokens(tok_indx) := mt('TRUE', lin_no, col_no, null); tok_indx := tok_indx + 1; 
            indx := indx + 3;
            col_no := col_no + 3;
          end if;
        when buf = 'n' then
          if(next_char2(indx, jsrc, 4) != 'null') then
            if(json_strict = false and REGEXP_LIKE(buf, '^[[:alpha:]]$', 'i')) then
              tokens(tok_indx) := mt('STRING', lin_no, col_no, null); 
              indx := lexName(jsrc, tokens(tok_indx), indx);
              col_no := col_no + length(tokens(tok_indx).data) + 1;
              tok_indx := tok_indx + 1; 
            else 
              s_error('Expected: ''null''', lin_no, col_no);
            end if;
          else
            tokens(tok_indx) := mt('NULL', lin_no, col_no, null); tok_indx := tok_indx + 1; 
            indx := indx + 3;
            col_no := col_no + 3;
          end if;
        when buf = 'f' then
          if(next_char2(indx, jsrc, 5) != 'false') then
            if(json_strict = false and REGEXP_LIKE(buf, '^[[:alpha:]]$', 'i')) then
              tokens(tok_indx) := mt('STRING', lin_no, col_no, null); 
              indx := lexName(jsrc, tokens(tok_indx), indx);
              col_no := col_no + length(tokens(tok_indx).data) + 1;
              tok_indx := tok_indx + 1; 
            else 
              s_error('Expected: ''false''', lin_no, col_no);
            end if;
          else
            tokens(tok_indx) := mt('FALSE', lin_no, col_no, null); tok_indx := tok_indx + 1; 
            indx := indx + 4;
            col_no := col_no + 4;
          end if;
        /*   -- 9 = TAB, 10 = \n, 13 = \r (Linux = \n, Windows = \r\n, Mac = \r */        
        when (buf = Chr(10)) then --linux newlines
          lin_no := lin_no + 1;
          col_no := 0;
            
        when (buf = Chr(13)) then --Windows or Mac way
          lin_no := lin_no + 1;
          col_no := 0;
          if(jsrc.len >= indx +1) then -- better safe than sorry
            buf := next_char(indx+1, jsrc);
            if(buf = Chr(10)) then --\r\n
              indx := indx + 1;
            end if;
          end if;
      
        when (buf = CHR(9)) then null; --tabbing
        when (buf in ('-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) then --number
          tokens(tok_indx) := mt('NUMBER', lin_no, col_no, null); 
          indx := lexNumber(jsrc, tokens(tok_indx), indx)-1;
          col_no := col_no + length(tokens(tok_indx).data);
          tok_indx := tok_indx + 1; 
        when buf = '"' then --number
          tokens(tok_indx) := mt('STRING', lin_no, col_no, null); 
          indx := lexString(jsrc, tokens(tok_indx), indx, '"');
          col_no := col_no + length(tokens(tok_indx).data) + 1;
          tok_indx := tok_indx + 1; 
        when buf = '''' and json_strict = false then --number
          tokens(tok_indx) := mt('STRING', lin_no, col_no, null); 
          indx := lexString(jsrc, tokens(tok_indx), indx, '''');
          col_no := col_no + length(tokens(tok_indx).data) + 1; --hovsa her
          tok_indx := tok_indx + 1; 
        when json_strict = false and REGEXP_LIKE(buf, '^[[:alpha:]]$', 'i') then
          tokens(tok_indx) := mt('STRING', lin_no, col_no, null); 
          indx := lexName(jsrc, tokens(tok_indx), indx);
          if(tokens(tok_indx).data_overflow is not null) then
            col_no := col_no + dbms_lob.getlength(tokens(tok_indx).data_overflow) + 1;
          else 
            col_no := col_no + length(tokens(tok_indx).data) + 1;
          end if;
          tok_indx := tok_indx + 1; 
        when json_strict = false and buf||next_char(indx+1, jsrc) = '/*' then --strip comments
          declare
            saveindx number := indx;
            un_esc clob;
          begin
            indx := indx + 1;
            loop
              indx := indx + 1;
              buf := next_char(indx, jsrc)||next_char(indx+1, jsrc);
              exit when buf = '*/';
              exit when buf is null;
            end loop;
            
            if(indx = saveindx+2) then 
              --enter unescaped mode
              --dbms_output.put_line('Entering unescaped mode');
              un_esc := empty_clob();
              dbms_lob.createtemporary(un_esc, true); 
              indx := indx + 1;
              loop
                indx := indx + 1;
                buf := next_char(indx, jsrc)||next_char(indx+1, jsrc)||next_char(indx+2, jsrc)||next_char(indx+3, jsrc);
                exit when buf = '/**/';
                if buf is null then
                  s_error('Unexpected sequence /**/ to end unescaped data: '||buf, lin_no, col_no);
                end if;
                buf := next_char(indx, jsrc);
                dbms_lob.writeappend(un_esc, length(buf), buf);
              end loop;
              tokens(tok_indx) := mt('ESTRING', lin_no, col_no, null);     
              tokens(tok_indx).data_overflow := un_esc;
              col_no := col_no + dbms_lob.getlength(un_esc) + 1; --note: line count won't work properly
              tok_indx := tok_indx + 1; 
              indx := indx + 2;
            end if;
            
            indx := indx + 1;
          end;
        when buf = ' ' then null; --space
        else 
          s_error('Unexpected char: '||buf, lin_no, col_no);
      end case;
    
      indx := indx + 1;
    end loop;
  
    return tokens;
  end lexer;

  /* SCANNER END */
  
  /* PARSER FUNCTIONS START*/
  procedure p_error(text varchar2, tok rToken) as
  begin
    raise_application_error(-20101, 'JSON Parser exception @ line: '||tok.line||' column: '||tok.col||' - '||text);
  end;
  
  function parseObj(tokens lTokens, indx in out nocopy pls_integer) return json;

  function parseArr(tokens lTokens, indx in out nocopy pls_integer) return json_list as
    e_arr json_value_array := json_value_array();
    ret_list json_list := json_list();
    v_count number := 0;
    tok rToken;
  begin
    --value, value, value ]
    if(indx > tokens.count) then p_error('more elements in array was excepted', tok); end if;
    tok := tokens(indx);
    while(tok.type_name != ']') loop
      e_arr.extend;
      v_count := v_count + 1;
      case tok.type_name
        when 'TRUE' then e_arr(v_count) := json_value(true);
        when 'FALSE' then e_arr(v_count) := json_value(false);
        when 'NULL' then e_arr(v_count) := json_value;
        when 'STRING' then e_arr(v_count) := case when tok.data_overflow is not null then json_value(tok.data_overflow) else json_value(tok.data) end;
        when 'ESTRING' then e_arr(v_count) := json_value(tok.data_overflow, false);
        when 'NUMBER' then e_arr(v_count) := json_value(to_number(replace(tok.data, '.', decimalpoint))); 
        when '[' then 
          declare e_list json_list; begin
            indx := indx + 1;
            e_list := parseArr(tokens, indx);
            e_arr(v_count) := e_list.to_json_value;
          end;
        when '{' then 
          indx := indx + 1;
          e_arr(v_count) := parseObj(tokens, indx).to_json_value;
        else
          p_error('Expected a value', tok);
      end case;
      indx := indx + 1;
      if(indx > tokens.count) then p_error('] not found', tok); end if;
      tok := tokens(indx);
      if(tok.type_name = ',') then --advance
        indx := indx + 1;
        if(indx > tokens.count) then p_error('more elements in array was excepted', tok); end if;
        tok := tokens(indx);
        if(tok.type_name = ']') then --premature exit
          p_error('Premature exit in array', tok);
        end if;
      elsif(tok.type_name != ']') then --error
        p_error('Expected , or ]', tok);
      end if;

    end loop;
    ret_list.list_data := e_arr;
    return ret_list;
  end parseArr;
  
  function parseMem(tokens lTokens, indx in out pls_integer, mem_name varchar2, mem_indx number) return json_value as
    mem json_value;
    tok rToken;
  begin
    tok := tokens(indx);
    case tok.type_name
      when 'TRUE' then mem := json_value(true);
      when 'FALSE' then mem := json_value(false);
      when 'NULL' then mem := json_value;
      when 'STRING' then mem := case when tok.data_overflow is not null then json_value(tok.data_overflow) else json_value(tok.data) end;
      when 'ESTRING' then mem := json_value(tok.data_overflow, false);
      when 'NUMBER' then mem := json_value(to_number(replace(tok.data, '.', decimalpoint)));
      when '[' then 
        declare
          e_list json_list;
        begin
          indx := indx + 1;
          e_list := parseArr(tokens, indx);
          mem := e_list.to_json_value;
        end;
      when '{' then 
        indx := indx + 1;
        mem := parseObj(tokens, indx).to_json_value;
      else 
        p_error('Found '||tok.type_name, tok);
    end case;
    mem.mapname := mem_name;
    mem.mapindx := mem_indx;

    indx := indx + 1;
    return mem;
  end parseMem;
  
  /*procedure test_duplicate_members(arr in json_member_array, mem_name in varchar2, wheretok rToken) as
  begin
    for i in 1 .. arr.count loop
      if(arr(i).member_name = mem_name) then
        p_error('Duplicate member name', wheretok);
      end if;
    end loop;
  end test_duplicate_members;*/
  
  function parseObj(tokens lTokens, indx in out nocopy pls_integer) return json as
    type memmap is table of number index by varchar2(4000); -- i've read somewhere that this is not possible - but it is!
    mymap memmap;
    nullelemfound boolean := false;
    
    obj json;
    tok rToken;
    mem_name varchar(4000);
    arr json_value_array := json_value_array();
  begin
    --what to expect?
    while(indx <= tokens.count) loop
      tok := tokens(indx);
      --debug('E: '||tok.type_name);
      case tok.type_name 
      when 'STRING' then
        --member 
        mem_name := substr(tok.data, 1, 4000);
        begin
          if(mem_name is null) then
            if(nullelemfound) then          
              p_error('Duplicate empty member: ', tok);
            else 
              nullelemfound := true;        
            end if;
          elsif(mymap(mem_name) is not null) then
            p_error('Duplicate member name: '||mem_name, tok);
          end if;
        exception 
          when no_data_found then mymap(mem_name) := 1;
        end;
        
        indx := indx + 1;
        if(indx > tokens.count) then p_error('Unexpected end of input', tok); end if;
        tok := tokens(indx);
        indx := indx + 1;
        if(indx > tokens.count) then p_error('Unexpected end of input', tok); end if;
        if(tok.type_name = ':') then
          --parse 
          declare 
            jmb json_value;
            x number;
          begin
            x := arr.count + 1;
            jmb := parseMem(tokens, indx, mem_name, x);
            arr.extend;
            arr(x) := jmb;
          end;
        else
          p_error('Expected '':''', tok);
        end if;
        --move indx forward if ',' is found
        if(indx > tokens.count) then p_error('Unexpected end of input', tok); end if;
        
        tok := tokens(indx);
        if(tok.type_name = ',') then
          --debug('found ,');
          indx := indx + 1;
          tok := tokens(indx);
          if(tok.type_name = '}') then --premature exit
            p_error('Premature exit in json object', tok);
          end if;
        elsif(tok.type_name != '}') then
           p_error('A comma seperator is probably missing', tok);
        end if;
      when '}' then
        obj := json();
        obj.json_data := arr;
        return obj;
      else 
        p_error('Expected string or }', tok);
      end case;
    end loop;
    
    p_error('} not found', tokens(indx-1));
    
    return obj;
  
  end;

  function parser(str varchar2) return json as
    tokens lTokens;
    obj json;
    indx pls_integer := 1;
    jsrc json_src;
  begin
    updateDecimalPoint();
    jsrc := prepareVarchar2(str);
    tokens := lexer(jsrc); 
    if(tokens(indx).type_name = '{') then
      indx := indx + 1;
      obj := parseObj(tokens, indx);
    else
      raise_application_error(-20101, 'JSON Parser exception - no { start found');
    end if;
    if(tokens.count != indx) then
      p_error('} should end the JSON object', tokens(indx));
    end if;
    
    return obj;
  end parser;

  function parse_list(str varchar2) return json_list as
    tokens lTokens;
    obj json_list;
    indx pls_integer := 1;
    jsrc json_src;
  begin
    updateDecimalPoint();
    jsrc := prepareVarchar2(str);
    tokens := lexer(jsrc); 
    if(tokens(indx).type_name = '[') then
      indx := indx + 1;
      obj := parseArr(tokens, indx);
    else
      raise_application_error(-20101, 'JSON List Parser exception - no [ start found');
    end if;
    if(tokens.count != indx) then
      p_error('] should end the JSON List object', tokens(indx));
    end if;
    
    return obj;
  end parse_list;

  function parse_list(str clob) return json_list as
    tokens lTokens;
    obj json_list;
    indx pls_integer := 1;
    jsrc json_src;
  begin
    updateDecimalPoint();
    jsrc := prepareClob(str);
    tokens := lexer(jsrc); 
    if(tokens(indx).type_name = '[') then
      indx := indx + 1;
      obj := parseArr(tokens, indx);
    else
      raise_application_error(-20101, 'JSON List Parser exception - no [ start found');
    end if;
    if(tokens.count != indx) then
      p_error('] should end the JSON List object', tokens(indx));
    end if;
    
    return obj;
  end parse_list;

  function parser(str clob) return json as
    tokens lTokens;
    obj json;
    indx pls_integer := 1;
    jsrc json_src;
  begin
    updateDecimalPoint();
    --dbms_output.put_line('Using clob');
    jsrc := prepareClob(str);
    tokens := lexer(jsrc); 
    if(tokens(indx).type_name = '{') then
      indx := indx + 1;
      obj := parseObj(tokens, indx);
    else
      raise_application_error(-20101, 'JSON Parser exception - no { start found');
    end if;
    if(tokens.count != indx) then
      p_error('} should end the JSON object', tokens(indx));
    end if;
    
    return obj;
  end parser;
  
  function parse_any(str varchar2) return json_value as
    tokens lTokens;
    obj json_list;
    ret json_value;
    indx pls_integer := 1;
    jsrc json_src;
  begin
    updateDecimalPoint();
    jsrc := prepareVarchar2(str);
    tokens := lexer(jsrc); 
    tokens(tokens.count+1).type_name := ']';
    obj := parseArr(tokens, indx);
    if(tokens.count != indx) then
      p_error('] should end the JSON List object', tokens(indx));
    end if;
    
    return obj.head();
  end parse_any;

  function parse_any(str clob) return json_value as
    tokens lTokens;
    obj json_list;
    indx pls_integer := 1;
    jsrc json_src;
  begin
    jsrc := prepareClob(str);
    tokens := lexer(jsrc); 
    tokens(tokens.count+1).type_name := ']';
    obj := parseArr(tokens, indx);
    if(tokens.count != indx) then
      p_error('] should end the JSON List object', tokens(indx));
    end if;
    
    return obj.head();
  end parse_any;

  /* last entry is the one to keep */
  procedure remove_duplicates(obj in out nocopy json) as
    type memberlist is table of json_value index by varchar2(4000);
    members memberlist;
    nulljsonvalue json_value := null;
    validated json := json();
    indx varchar2(4000);
  begin
    for i in 1 .. obj.count loop
      if(obj.get(i).mapname is null) then 
        nulljsonvalue := obj.get(i);
      else 
        members(obj.get(i).mapname) := obj.get(i);
      end if;            
    end loop;
    
    validated.check_duplicate(false);
    indx := members.first;
    loop
      exit when indx is null;
      validated.put(indx, members(indx));
      indx := members.next(indx);
    end loop;
    if(nulljsonvalue is not null) then
      validated.put('', nulljsonvalue);
    end if;
    
    validated.check_for_duplicate := obj.check_for_duplicate;
    
    obj := validated;  
  end;
  
  function get_version return varchar2 as
  begin
    return 'PL/JSON v1.0.4';
  end get_version;

end json_parser;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_PRINTER with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY "JSON_PRINTER" as
  max_line_len number := 0;
  cur_line_len number := 0;
  
  function llcheck(str in varchar2) return varchar2 as
  begin
    --dbms_output.put_line(cur_line_len || ' : '|| str);
    if(max_line_len > 0 and length(str)+cur_line_len > max_line_len) then
      cur_line_len := length(str);
      return newline_char || str;
    else 
      cur_line_len := cur_line_len + length(str);
      return str;
    end if;
  end llcheck;  

  function escapeString(str varchar2) return varchar2 as
    sb varchar2(32767) := '';
    buf varchar2(40);
    num number;
  begin
    if(str is null) then return ''; end if;
    for i in 1 .. length(str) loop
      buf := substr(str, i, 1);
      --backspace b = U+0008
      --formfeed  f = U+000C
      --newline   n = U+000A
      --carret    r = U+000D
      --tabulator t = U+0009
      case buf
      when chr( 8) then buf := '\b';
      when chr( 9) then buf := '\t';
      when chr(10) then buf := '\n';
      when chr(13) then buf := '\f';
      when chr(14) then buf := '\r';
      when chr(34) then buf := '\"';
      when chr(47) then if(escape_solidus) then buf := '\/'; end if;
      when chr(92) then buf := '\\';
      else 
        if(ascii(buf) < 32) then
          buf := '\u'||replace(substr(to_char(ascii(buf), 'XXXX'),2,4), ' ', '0');
        elsif (ascii_output) then 
          buf := replace(asciistr(buf), '\', '\u');
        end if;
      end case;      
      
      sb := sb || buf;
    end loop;
  
    return sb;
  end escapeString;

  function newline(spaces boolean) return varchar2 as
  begin
    cur_line_len := 0;
    if(spaces) then return newline_char; else return ''; end if;
  end;

/*  function get_schema return varchar2 as
  begin
    return sys_context('userenv', 'current_schema');
  end;  
*/  
  function tab(indent number, spaces boolean) return varchar2 as
    i varchar(200) := '';
  begin
    if(not spaces) then return ''; end if;
    for x in 1 .. indent loop i := i || indent_string; end loop;
    return i;
  end;
  
  function getCommaSep(spaces boolean) return varchar2 as
  begin
    if(spaces) then return ', '; else return ','; end if;
  end;

  function getMemName(mem json_value, spaces boolean) return varchar2 as
  begin
    if(spaces) then
      return llcheck('"'||escapeString(mem.mapname)||'"') || llcheck(' : ');
    else 
      return llcheck('"'||escapeString(mem.mapname)||'"') || llcheck(':');
    end if;
  end;

/* Clob method start here */
  procedure add_to_clob(buf_lob in out nocopy clob, buf_str in out nocopy varchar2, str varchar2) as
  begin
    if(lengthb(str) > 32767 - lengthb(buf_str)) then
--      dbms_lob.append(buf_lob, buf_str);
      dbms_lob.writeappend(buf_lob, length(buf_str), buf_str);
      buf_str := str;
    else
      buf_str := buf_str || str;
    end if;  
  end add_to_clob;

  procedure flush_clob(buf_lob in out nocopy clob, buf_str in out nocopy varchar2) as
  begin
--    dbms_lob.append(buf_lob, buf_str);
    dbms_lob.writeappend(buf_lob, length(buf_str), buf_str);
  end flush_clob;

  procedure ppObj(obj json, indent number, buf in out nocopy clob, spaces boolean, buf_str in out nocopy varchar2);

  procedure ppEA(input json_list, indent number, buf in out nocopy clob, spaces boolean, buf_str in out nocopy varchar2) as
    elem json_value; 
    arr json_value_array := input.list_data;
    numbuf varchar2(4000);
  begin
    for y in 1 .. arr.count loop
      elem := arr(y);
      if(elem is not null) then
      case elem.get_type
        when 'number' then 
          numbuf := '';
          if (elem.get_number < 1 and elem.get_number > 0) then numbuf := '0'; end if;
          if (elem.get_number < 0 and elem.get_number > -1) then 
            numbuf := '-0'; 
            numbuf := numbuf || substr(to_char(elem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,'''),2);
          else
            numbuf := numbuf || to_char(elem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''');
          end if;
          add_to_clob(buf, buf_str, llcheck(numbuf));
        when 'string' then 
          if(elem.extended_str is not null) then --clob implementation
            add_to_clob(buf, buf_str, case when elem.num = 1 then '"' else '/**/' end);
            declare
              offset number := 1;
              v_str varchar(32767);
              amount number := 32767;
            begin
              while(offset <= dbms_lob.getlength(elem.extended_str)) loop
                dbms_lob.read(elem.extended_str, amount, offset, v_str);
                if(elem.num = 1) then 
                  add_to_clob(buf, buf_str, escapeString(v_str));
                else 
                  add_to_clob(buf, buf_str, v_str);
                end if;
                offset := offset + amount;
              end loop;
            end;
            add_to_clob(buf, buf_str, case when elem.num = 1 then '"' else '/**/' end || newline_char);
          else
            if(elem.num = 1) then 
              add_to_clob(buf, buf_str, llcheck('"'||escapeString(elem.get_string)||'"'));
            else 
              add_to_clob(buf, buf_str, llcheck('/**/'||elem.get_string||'/**/'));
            end if;
          end if;
        when 'bool' then
          if(elem.get_bool) then 
            add_to_clob(buf, buf_str, llcheck('true'));
          else
            add_to_clob(buf, buf_str, llcheck('false'));
          end if;
        when 'null' then
          add_to_clob(buf, buf_str, llcheck('null'));
        when 'array' then
          add_to_clob(buf, buf_str, llcheck('['));
          ppEA(json_list(elem), indent, buf, spaces, buf_str);
          add_to_clob(buf, buf_str, llcheck(']'));
        when 'object' then
          ppObj(json(elem), indent, buf, spaces, buf_str);
        else add_to_clob(buf, buf_str, llcheck(elem.get_type));
      end case;
      end if;
      if(y != arr.count) then add_to_clob(buf, buf_str, llcheck(getCommaSep(spaces))); end if;
    end loop;
  end ppEA;

  procedure ppMem(mem json_value, indent number, buf in out nocopy clob, spaces boolean, buf_str in out nocopy varchar2) as
    numbuf varchar2(4000);
  begin
    add_to_clob(buf, buf_str, llcheck(tab(indent, spaces)) || llcheck(getMemName(mem, spaces)));
    case mem.get_type
      when 'number' then 
        if (mem.get_number < 1 and mem.get_number > 0) then numbuf := '0'; end if;
        if (mem.get_number < 0 and mem.get_number > -1) then 
          numbuf := '-0'; 
          numbuf := numbuf || substr(to_char(mem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,'''),2);
        else
          numbuf := numbuf || to_char(mem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''');
        end if;
        add_to_clob(buf, buf_str, llcheck(numbuf));
      when 'string' then 
        if(mem.extended_str is not null) then --clob implementation
          add_to_clob(buf, buf_str, case when mem.num = 1 then '"' else '/**/' end);
          declare
            offset number := 1;
            v_str varchar(32767);
            amount number := 32767;
          begin
--            dbms_output.put_line('SIZE:'||dbms_lob.getlength(mem.extended_str));
            while(offset <= dbms_lob.getlength(mem.extended_str)) loop
--            dbms_output.put_line('OFFSET:'||offset);
 --             v_str := dbms_lob.substr(mem.extended_str, 8192, offset);
              dbms_lob.read(mem.extended_str, amount, offset, v_str);
--            dbms_output.put_line('VSTR_SIZE:'||length(v_str));
              if(mem.num = 1) then 
                add_to_clob(buf, buf_str, escapeString(v_str));
              else 
                add_to_clob(buf, buf_str, v_str);
              end if;
              offset := offset + amount;
            end loop;
          end;
          add_to_clob(buf, buf_str, case when mem.num = 1 then '"' else '/**/' end || newline_char);
        else 
          if(mem.num = 1) then 
            add_to_clob(buf, buf_str, llcheck('"'||escapeString(mem.get_string)||'"'));
          else 
            add_to_clob(buf, buf_str, llcheck('/**/'||mem.get_string||'/**/'));
          end if;
        end if;
      when 'bool' then
        if(mem.get_bool) then 
          add_to_clob(buf, buf_str, llcheck('true'));
        else
          add_to_clob(buf, buf_str, llcheck('false'));
        end if;
      when 'null' then
        add_to_clob(buf, buf_str, llcheck('null'));
      when 'array' then
        add_to_clob(buf, buf_str, llcheck('['));
        ppEA(json_list(mem), indent, buf, spaces, buf_str);
        add_to_clob(buf, buf_str, llcheck(']'));
      when 'object' then
        ppObj(json(mem), indent, buf, spaces, buf_str);
      else add_to_clob(buf, buf_str, llcheck(mem.get_type));
    end case;
  end ppMem;

  procedure ppObj(obj json, indent number, buf in out nocopy clob, spaces boolean, buf_str in out nocopy varchar2) as
  begin
    add_to_clob(buf, buf_str, llcheck('{') || newline(spaces));
    for m in 1 .. obj.json_data.count loop
      ppMem(obj.json_data(m), indent+1, buf, spaces, buf_str);
      if(m != obj.json_data.count) then 
        add_to_clob(buf, buf_str, llcheck(',') || newline(spaces));
      else 
        add_to_clob(buf, buf_str, newline(spaces)); 
      end if;
    end loop;
    add_to_clob(buf, buf_str, llcheck(tab(indent, spaces)) || llcheck('}')); -- || chr(13);
  end ppObj;
  
  procedure pretty_print(obj json, spaces boolean default true, buf in out nocopy clob, line_length number default 0, erase_clob boolean default true) as 
    buf_str varchar2(32767);
    amount number := dbms_lob.getlength(buf);
  begin
    if(erase_clob and amount > 0) then dbms_lob.trim(buf, 0); dbms_lob.erase(buf, amount); end if;
    
    max_line_len := line_length;
    cur_line_len := 0;
    ppObj(obj, 0, buf, spaces, buf_str);  
    flush_clob(buf, buf_str);
  end;

  procedure pretty_print_list(obj json_list, spaces boolean default true, buf in out nocopy clob, line_length number default 0, erase_clob boolean default true) as 
    buf_str varchar2(32767);
    amount number := dbms_lob.getlength(buf);
  begin
    if(erase_clob and amount > 0) then dbms_lob.trim(buf, 0); dbms_lob.erase(buf, amount); end if;
    
    max_line_len := line_length;
    cur_line_len := 0;
    add_to_clob(buf, buf_str, llcheck('['));
    ppEA(obj, 0, buf, spaces, buf_str);  
    add_to_clob(buf, buf_str, llcheck(']'));
    flush_clob(buf, buf_str);
  end;

  procedure pretty_print_any(json_part json_value, spaces boolean default true, buf in out nocopy clob, line_length number default 0, erase_clob boolean default true) as
    buf_str varchar2(32767) := '';
    numbuf varchar2(4000);
    amount number := dbms_lob.getlength(buf);
  begin
    if(erase_clob and amount > 0) then dbms_lob.trim(buf, 0); dbms_lob.erase(buf, amount); end if;
    
    case json_part.get_type
      when 'number' then 
        if (json_part.get_number < 1 and json_part.get_number > 0) then numbuf := '0'; end if;
        if (json_part.get_number < 0 and json_part.get_number > -1) then 
          numbuf := '-0'; 
          numbuf := numbuf || substr(to_char(json_part.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,'''),2);
        else
          numbuf := numbuf || to_char(json_part.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''');
        end if;
        add_to_clob(buf, buf_str, numbuf);
      when 'string' then 
        if(json_part.extended_str is not null) then --clob implementation
          add_to_clob(buf, buf_str, case when json_part.num = 1 then '"' else '/**/' end);
          declare
            offset number := 1;
            v_str varchar(32767);
            amount number := 32767;
          begin
            while(offset <= dbms_lob.getlength(json_part.extended_str)) loop
              dbms_lob.read(json_part.extended_str, amount, offset, v_str);
              if(json_part.num = 1) then 
                add_to_clob(buf, buf_str, escapeString(v_str));
              else 
                add_to_clob(buf, buf_str, v_str);
              end if;
              offset := offset + amount;
            end loop;
          end;
          add_to_clob(buf, buf_str, case when json_part.num = 1 then '"' else '/**/' end);
        else 
          if(json_part.num = 1) then 
            add_to_clob(buf, buf_str, llcheck('"'||escapeString(json_part.get_string)||'"'));
          else 
            add_to_clob(buf, buf_str, llcheck('/**/'||json_part.get_string||'/**/'));
          end if;
        end if;
      when 'bool' then
	      if(json_part.get_bool) then
          add_to_clob(buf, buf_str, 'true');
        else
          add_to_clob(buf, buf_str, 'false');
        end if;
      when 'null' then
        add_to_clob(buf, buf_str, 'null');
      when 'array' then
        pretty_print_list(json_list(json_part), spaces, buf, line_length);
        return;
      when 'object' then
        pretty_print(json(json_part), spaces, buf, line_length);
        return;
      else add_to_clob(buf, buf_str, 'unknown type:'|| json_part.get_type);
    end case;
    flush_clob(buf, buf_str);
  end;

/* Clob method end here */

/* Varchar2 method start here */

  procedure ppObj(obj json, indent number, buf in out nocopy varchar2, spaces boolean);

  procedure ppEA(input json_list, indent number, buf in out varchar2, spaces boolean) as
    elem json_value; 
    arr json_value_array := input.list_data;
    str varchar2(400);
  begin
    for y in 1 .. arr.count loop
      elem := arr(y);
      if(elem is not null) then
      case elem.get_type
        when 'number' then 
          str := '';
          if (elem.get_number < 1 and elem.get_number > 0) then str := '0'; end if;
          if (elem.get_number < 0 and elem.get_number > -1) then 
            str := '-0' || substr(to_char(elem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,'''),2);
          else
            str := str || to_char(elem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''');
          end if;
          buf := buf || llcheck(str);
        when 'string' then 
          if(elem.num = 1) then 
            buf := buf || llcheck('"'||escapeString(elem.get_string)||'"');
          else 
            buf := buf || llcheck('/**/'||elem.get_string||'/**/');
          end if;
        when 'bool' then
          if(elem.get_bool) then           
            buf := buf || llcheck('true');
          else
            buf := buf || llcheck('false');
          end if;
        when 'null' then
          buf := buf || llcheck('null');
        when 'array' then
          buf := buf || llcheck('[');
          ppEA(json_list(elem), indent, buf, spaces);
          buf := buf || llcheck(']');
        when 'object' then
          ppObj(json(elem), indent, buf, spaces);
        else buf := buf || llcheck(elem.get_type); /* should never happen */
      end case;
      end if;
      if(y != arr.count) then buf := buf || llcheck(getCommaSep(spaces)); end if;
    end loop;
  end ppEA;

  procedure ppMem(mem json_value, indent number, buf in out nocopy varchar2, spaces boolean) as
    str varchar2(400) := '';
  begin
    buf := buf || llcheck(tab(indent, spaces)) || getMemName(mem, spaces);
    case mem.get_type
      when 'number' then 
        if (mem.get_number < 1 and mem.get_number > 0) then str := '0'; end if;
        if (mem.get_number < 0 and mem.get_number > -1) then 
          str := '-0' || substr(to_char(mem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,'''),2);
        else
          str := str || to_char(mem.get_number, 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''');
        end if;
        buf := buf || llcheck(str);
      when 'string' then 
        if(mem.num = 1) then 
          buf := buf || llcheck('"'||escapeString(mem.get_string)||'"');
        else 
          buf := buf || llcheck('/**/'||mem.get_string||'/**/');
        end if;
      when 'bool' then
        if(mem.get_bool) then 
          buf := buf || llcheck('true');
        else 
          buf := buf || llcheck('false');
        end if;
      when 'null' then
        buf := buf || llcheck('null');
      when 'array' then
        buf := buf || llcheck('[');
        ppEA(json_list(mem), indent, buf, spaces);
        buf := buf || llcheck(']');
      when 'object' then
        ppObj(json(mem), indent, buf, spaces);
      else buf := buf || llcheck(mem.get_type); /* should never happen */
    end case;
  end ppMem;
  
  procedure ppObj(obj json, indent number, buf in out nocopy varchar2, spaces boolean) as
  begin
    buf := buf || llcheck('{') || newline(spaces);
    for m in 1 .. obj.json_data.count loop
      ppMem(obj.json_data(m), indent+1, buf, spaces);
      if(m != obj.json_data.count) then buf := buf || llcheck(',') || newline(spaces);
      else buf := buf || newline(spaces); end if;
    end loop;
    buf := buf || llcheck(tab(indent, spaces)) || llcheck('}'); -- || chr(13);
  end ppObj;
  
  function pretty_print(obj json, spaces boolean default true, line_length number default 0) return varchar2 as
    buf varchar2(32767) := '';
  begin
    max_line_len := line_length;
    cur_line_len := 0;
    ppObj(obj, 0, buf, spaces);
    return buf;
  end pretty_print;

  function pretty_print_list(obj json_list, spaces boolean default true, line_length number default 0) return varchar2 as
    buf varchar2(32767);
  begin
    max_line_len := line_length;
    cur_line_len := 0;
    buf := llcheck('[');
    ppEA(obj, 0, buf, spaces);
    buf := buf || llcheck(']');
    return buf;
  end;

  function pretty_print_any(json_part json_value, spaces boolean default true, line_length number default 0) return varchar2 as
    buf varchar2(32767) := '';    
  begin
    case json_part.get_type
      when 'number' then 
        if (json_part.get_number() < 1 and json_part.get_number() > 0) then buf := buf || '0'; end if;
        if (json_part.get_number() < 0 and json_part.get_number() > -1) then 
          buf := buf || '-0'; 
          buf := buf || substr(to_char(json_part.get_number(), 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,'''),2);
        else
          buf := buf || to_char(json_part.get_number(), 'TM9', 'NLS_NUMERIC_CHARACTERS=''.,''');
        end if;
      when 'string' then 
        if(json_part.num = 1) then 
          buf := buf || '"'||escapeString(json_part.get_string)||'"';
        else 
          buf := buf || '/**/'||json_part.get_string||'/**/';
        end if;
      when 'bool' then
      	if(json_part.get_bool) then buf := 'true'; else buf := 'false'; end if;
      when 'null' then
        buf := 'null';
      when 'array' then
        buf := pretty_print_list(json_list(json_part), spaces, line_length);
      when 'object' then
        buf := pretty_print(json(json_part), spaces, line_length);
      else buf := 'weird error: '|| json_part.get_type;
    end case;
    return buf;
  end;
  
  procedure dbms_output_clob(my_clob clob, delim varchar2, jsonp varchar2 default null) as 
    prev number := 1;
    indx number := 1;
    size_of_nl number := lengthb(delim);
    v_str varchar2(32767);
    amount number := 32767;
  begin
    if(jsonp is not null) then dbms_output.put_line(jsonp||'('); end if;
    while(indx != 0) loop
      --read every line
      indx := dbms_lob.instr(my_clob, delim, prev+1);
 --     dbms_output.put_line(prev || ' to ' || indx);
      
      if(indx = 0) then
        --emit from prev to end;
        amount := 32767;
 --       dbms_output.put_line(' mycloblen ' || dbms_lob.getlength(my_clob));
        loop
          dbms_lob.read(my_clob, amount, prev, v_str);
          dbms_output.put_line(v_str);
          prev := prev+amount-1;
          exit when prev >= dbms_lob.getlength(my_clob);
        end loop;
      else 
        amount := indx - prev;
        if(amount > 32767) then 
          amount := 32767;
--          dbms_output.put_line(' mycloblen ' || dbms_lob.getlength(my_clob));
          loop
            dbms_lob.read(my_clob, amount, prev, v_str);
            dbms_output.put_line(v_str);
            prev := prev+amount-1;
            amount := indx - prev;
            exit when prev >= indx - 1;
            if(amount > 32767) then amount := 32767; end if;
          end loop;
          prev := indx + size_of_nl;
        else 
          dbms_lob.read(my_clob, amount, prev, v_str);
          dbms_output.put_line(v_str);     
          prev := indx + size_of_nl;
        end if;
      end if;
    
    end loop;
    if(jsonp is not null) then dbms_output.put_line(')'); end if;

/*    while (amount != 0) loop
      indx := dbms_lob.instr(my_clob, delim, prev+1);
      
--      dbms_output.put_line(prev || ' to ' || indx);
      if(indx = 0) then 
        indx := dbms_lob.getlength(my_clob)+1;
      end if;

      if(indx-prev > 32767) then
        indx := prev+32767;
      end if;
--      dbms_output.put_line(prev || ' to ' || indx);
      --substr doesnt work properly on all platforms! (come on oracle - error on Oracle VM for virtualbox)
--        dbms_output.put_line(dbms_lob.substr(my_clob, indx-prev, prev));
      amount := indx-prev;
--        dbms_output.put_line('amount'||amount);
      dbms_lob.read(my_clob, amount, prev, v_str);
      dbms_output.put_line(v_str);
      prev := indx+size_of_nl;
      if(amount = 32767) then prev := prev-size_of_nl-1; end if;
    end loop;
    if(jsonp is not null) then dbms_output.put_line(')'); end if;*/
  end;


/*  procedure dbms_output_clob(my_clob clob, delim varchar2, jsonp varchar2 default null) as 
    prev number := 1;
    indx number := 1;
    size_of_nl number := lengthb(delim);
    v_str varchar2(32767);
    amount number;
  begin
    if(jsonp is not null) then dbms_output.put_line(jsonp||'('); end if;
    while (indx != 0) loop
      indx := dbms_lob.instr(my_clob, delim, prev+1);
      
--      dbms_output.put_line(prev || ' to ' || indx);
      if(indx-prev > 32767) then
        indx := prev+32767;
      end if;
--      dbms_output.put_line(prev || ' to ' || indx);
      --substr doesnt work properly on all platforms! (come on oracle - error on Oracle VM for virtualbox)
      if(indx = 0) then 
--        dbms_output.put_line(dbms_lob.substr(my_clob, dbms_lob.getlength(my_clob)-prev+size_of_nl, prev));
        amount := dbms_lob.getlength(my_clob)-prev+size_of_nl;
        dbms_lob.read(my_clob, amount, prev, v_str);
      else 
--        dbms_output.put_line(dbms_lob.substr(my_clob, indx-prev, prev));
        amount := indx-prev;
--        dbms_output.put_line('amount'||amount);
        dbms_lob.read(my_clob, amount, prev, v_str);
      end if;
      dbms_output.put_line(v_str);
      prev := indx+size_of_nl;
      if(amount = 32767) then prev := prev-size_of_nl-1; end if;
    end loop;
    if(jsonp is not null) then dbms_output.put_line(')'); end if;
  end;
*/  
  procedure htp_output_clob(my_clob clob, jsonp varchar2 default null) as 
    /*amount number := 4096;
    pos number := 1;
    len number;
    */
    l_amt    number default 30;
    l_off   number default 1;
    l_str   varchar2(4096);
    
  begin
    if(jsonp is not null) then htp.prn(jsonp||'('); end if;
    
    begin
      loop
        dbms_lob.read( my_clob, l_amt, l_off, l_str );

        -- it is vital to use htp.PRN to avoid 
        -- spurious line feeds getting added to your
        -- document
        htp.prn( l_str  );
        l_off := l_off+l_amt;
        l_amt := 4096;
      end loop;
    exception
      when no_data_found then NULL;
    end;
        
    /*
    len := dbms_lob.getlength(my_clob);
    
    while(pos < len) loop
      htp.prn(dbms_lob.substr(my_clob, amount, pos)); -- should I replace substr with dbms_lob.read?
      --dbms_output.put_line(dbms_lob.substr(my_clob, amount, pos)); 
      pos := pos + amount;
    end loop;
    */
    if(jsonp is not null) then htp.prn(')'); end if;
  end;

end json_printer;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_UTIL_PKG with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY JSON_UTIL_PKG 
as
  scanner_exception exception;
  pragma exception_init(scanner_exception, -20100);
  parser_exception exception;
  pragma exception_init(parser_exception, -20101);

  /*

  Purpose:    JSON utilities for PL/SQL

  Remarks:    

  Who     Date        Description
  ------  ----------  -------------------------------------
  MBR     30.01.2010  Created
  
  */


  g_json_null_object             constant varchar2(20) := '{ }';


function get_xml_to_json_stylesheet return varchar2
as
begin

  /*

  Purpose:    return XSLT stylesheet for XML to JSON transformation

  Remarks:    see http://code.google.com/p/xml2json-xslt/

  Who     Date        Description
  ------  ----------  -------------------------------------
  MBR     30.01.2010  Created
  MBR     30.01.2010  Added fix for nulls
  
  */


  return q'^<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!--
  Copyright (c) 2006,2008 Doeke Zanstra
  All rights reserved.

  Redistribution and use in source and binary forms, with or without modification, 
  are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this 
  list of conditions and the following disclaimer. Redistributions in binary 
  form must reproduce the above copyright notice, this list of conditions and the 
  following disclaimer in the documentation and/or other materials provided with 
  the distribution.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
  THE POSSIBILITY OF SUCH DAMAGE.
-->

  <xsl:output indent="no" omit-xml-declaration="yes" method="text" encoding="UTF-8" media-type="text/x-json"/>
        <xsl:strip-space elements="*"/>
  <!--contant-->
  <xsl:variable name="d">0123456789</xsl:variable>

  <!-- ignore document text -->
  <xsl:template match="text()[preceding-sibling::node() or following-sibling::node()]"/>

  <!-- string -->
  <xsl:template match="text()">
    <xsl:call-template name="escape-string">
      <xsl:with-param name="s" select="."/>
    </xsl:call-template>
  </xsl:template>
  
  <!-- Main template for escaping strings; used by above template and for object-properties 
       Responsibilities: placed quotes around string, and chain up to next filter, escape-bs-string -->
  <xsl:template name="escape-string">
    <xsl:param name="s"/>
    <xsl:text>"</xsl:text>
    <xsl:call-template name="escape-bs-string">
      <xsl:with-param name="s" select="$s"/>
    </xsl:call-template>
    <xsl:text>"</xsl:text>
  </xsl:template>
  
  <!-- Escape the backslash (\) before everything else. -->
  <xsl:template name="escape-bs-string">
    <xsl:param name="s"/>
    <xsl:choose>
      <xsl:when test="contains($s,'\')">
        <xsl:call-template name="escape-quot-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'\'),'\\')"/>
        </xsl:call-template>
        <xsl:call-template name="escape-bs-string">
          <xsl:with-param name="s" select="substring-after($s,'\')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="escape-quot-string">
          <xsl:with-param name="s" select="$s"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <!-- Escape the double quote ("). -->
  <xsl:template name="escape-quot-string">
    <xsl:param name="s"/>
    <xsl:choose>
      <xsl:when test="contains($s,'&quot;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&quot;'),'\&quot;')"/>
        </xsl:call-template>
        <xsl:call-template name="escape-quot-string">
          <xsl:with-param name="s" select="substring-after($s,'&quot;')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="$s"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <!-- Replace tab, line feed and/or carriage return by its matching escape code. Can't escape backslash
       or double quote here, because they don't replace characters (&#x0; becomes \t), but they prefix 
       characters (\ becomes \\). Besides, backslash should be seperate anyway, because it should be 
       processed first. This function can't do that. -->
  <xsl:template name="encode-string">
    <xsl:param name="s"/>
    <xsl:choose>
      <!-- tab -->
      <xsl:when test="contains($s,'&#x9;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&#x9;'),'\t',substring-after($s,'&#x9;'))"/>
        </xsl:call-template>
      </xsl:when>
      <!-- line feed -->
      <xsl:when test="contains($s,'&#xA;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&#xA;'),'\n',substring-after($s,'&#xA;'))"/>
        </xsl:call-template>
      </xsl:when>
      <!-- carriage return -->
      <xsl:when test="contains($s,'&#xD;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&#xD;'),'\r',substring-after($s,'&#xD;'))"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise><xsl:value-of select="$s"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- number (no support for javascript mantissa) -->
  <xsl:template match="text()[not(string(number())='NaN' or
                      (starts-with(.,'0' ) and . != '0' and
not(starts-with(.,'0.' ))) or
                      (starts-with(.,'-0' ) and . != '-0' and
not(starts-with(.,'-0.' )))
                      )]">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- boolean, case-insensitive -->
  <xsl:template match="text()[translate(.,'TRUE','true')='true']">true</xsl:template>
  <xsl:template match="text()[translate(.,'FALSE','false')='false']">false</xsl:template>

  <!-- object -->
  <xsl:template match="*" name="base">
    <xsl:if test="not(preceding-sibling::*)">{</xsl:if>
    <xsl:call-template name="escape-string">
      <xsl:with-param name="s" select="name()"/>
    </xsl:call-template>
    <xsl:text>:</xsl:text>
    <!-- check type of node -->
    <xsl:choose>
      <!-- null nodes -->
      <xsl:when test="count(child::node())=0">null</xsl:when>
      <!-- other nodes -->
      <xsl:otherwise>
        <xsl:apply-templates select="child::node()"/>
      </xsl:otherwise>
    </xsl:choose>
    <!-- end of type check -->
    <xsl:if test="following-sibling::*">,</xsl:if>
    <xsl:if test="not(following-sibling::*)">}</xsl:if>
  </xsl:template>

  <!-- array -->
  <xsl:template match="*[count(../*[name(../*)=name(.)])=count(../*) and count(../*)&gt;1]">
    <xsl:if test="not(preceding-sibling::*)">[</xsl:if>
    <xsl:choose>
      <xsl:when test="not(child::node())">
        <xsl:text>null</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="child::node()"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="following-sibling::*">,</xsl:if>
    <xsl:if test="not(following-sibling::*)">]</xsl:if>
  </xsl:template>
  
  <!-- convert root element to an anonymous container -->
  <xsl:template match="/">
    <xsl:apply-templates select="node()"/>
  </xsl:template>
    
</xsl:stylesheet>^';

end get_xml_to_json_stylesheet;


function ref_cursor_to_json (p_ref_cursor in sys_refcursor,
                             p_max_rows in number := null,
                             p_skip_rows in number := null) return json_list
as
  l_ctx         dbms_xmlgen.ctxhandle;
  l_num_rows    pls_integer;
  l_xml         xmltype;
  l_json        xmltype;
  l_returnvalue clob;
begin

  /*

  Purpose:    generate JSON from REF Cursor

  Remarks:    

  Who     Date        Description
  ------  ----------  -------------------------------------
  MBR     30.01.2010  Created
  JKR     01.05.2010  Edited to fit in PL/JSON
  
  */

  l_ctx := dbms_xmlgen.newcontext (p_ref_cursor);
  
  dbms_xmlgen.setnullhandling (l_ctx, dbms_xmlgen.empty_tag);
  
  -- for pagination

  if p_max_rows is not null then
    dbms_xmlgen.setmaxrows (l_ctx, p_max_rows);
  end if;
  
  if p_skip_rows is not null then
    dbms_xmlgen.setskiprows (l_ctx, p_skip_rows);
  end if;
  
  -- get the XML content
  l_xml := dbms_xmlgen.getxmltype (l_ctx, dbms_xmlgen.none);
  
  l_num_rows := dbms_xmlgen.getnumrowsprocessed (l_ctx);
  
  dbms_xmlgen.closecontext (l_ctx);
  
  close p_ref_cursor;

  if l_num_rows > 0 then
    -- perform the XSL transformation
    l_json := l_xml.transform (xmltype(get_xml_to_json_stylesheet));
    l_returnvalue := l_json.getclobval();
  else
    l_returnvalue := g_json_null_object;
  end if;

  l_returnvalue := dbms_xmlgen.convert (l_returnvalue, dbms_xmlgen.entity_decode);
  
  if(l_num_rows = 0) then
    return json_list();
  else 
    if(l_num_rows = 1) then
      declare ret json_list := json_list();
      begin
        ret.append(
          json(
            json(l_returnvalue).get('ROWSET')
          ).get('ROW')
        );
        return ret;
      end;
    else 
      return json_list(json(l_returnvalue).get('ROWSET'));
    end if;
  end if;
  
exception
  when scanner_exception then
    dbms_output.put('Scanner problem with the following input: ');
    dbms_output.put_line(l_returnvalue);
    raise;
  when parser_exception then
    dbms_output.put('Parser problem with the following input: ');
    dbms_output.put_line(l_returnvalue);
    raise;
  when others then raise;  
end ref_cursor_to_json;

function sql_to_json (p_sql in varchar2,
                      p_max_rows in number := null,
                      p_skip_rows in number := null) return json_list
as
  v_cur sys_refcursor;
begin
  open v_cur for p_sql;
  return ref_cursor_to_json(v_cur, p_max_rows, p_skip_rows);

end sql_to_json;


end json_util_pkg;
-- Unable to render PACKAGE BODY DDL for object CAMAC_DEV.JSON_XML with DBMS_METADATA attempting internal generator.
CREATE 
PACKAGE BODY JSON_XML as 

  function escapeStr(str varchar2) return varchar2 as
    buf varchar2(32767) := '';
    ch varchar2(4);
  begin
    for i in 1 .. length(str) loop
      ch := substr(str, i, 1);
      case ch
      when '&' then buf := buf || '&amp;';
      when '<' then buf := buf || '&lt;';
      when '>' then buf := buf || '&gt;';
      when '"' then buf := buf || '&quot;';
      else buf := buf || ch;
      end case;
    end loop;
    return buf;  
  end escapeStr;

/* Clob methods from printer */
  procedure add_to_clob(buf_lob in out nocopy clob, buf_str in out nocopy varchar2, str varchar2) as
  begin
    if(length(str) > 32767 - length(buf_str)) then
      dbms_lob.append(buf_lob, buf_str);
      buf_str := str;
    else
      buf_str := buf_str || str;
    end if;  
  end add_to_clob;

  procedure flush_clob(buf_lob in out nocopy clob, buf_str in out nocopy varchar2) as
  begin
    dbms_lob.append(buf_lob, buf_str);
  end flush_clob;
  
  procedure toString(obj json_value, tagname in varchar2, xmlstr in out nocopy clob, xmlbuf in out nocopy varchar2) as
    v_obj json;
    v_list json_list;

    v_keys json_list;
    v_value json_value;
    key_str varchar2(4000);
  begin
    if (obj.is_object()) then
      add_to_clob(xmlstr, xmlbuf, '<' || tagname || '>');
      v_obj := json(obj);

      v_keys := v_obj.get_keys();
      for i in 1 .. v_keys.count loop
        v_value := v_obj.get(i);
        key_str := v_keys.get(i).str;
        
        if(key_str = 'content') then
          if(v_value.is_array()) then
            declare
              v_l json_list := json_list(v_value);
            begin
              for j in 1 .. v_l.count loop
                if(j > 1) then add_to_clob(xmlstr, xmlbuf, chr(13)||chr(10)); end if;
                add_to_clob(xmlstr, xmlbuf, escapeStr(v_l.get(j).to_char()));
              end loop;
            end;
          else 
            add_to_clob(xmlstr, xmlbuf, escapeStr(v_value.to_char()));
          end if;
        elsif(v_value.is_array()) then
          declare
            v_l json_list := json_list(v_value);
          begin
            for j in 1 .. v_l.count loop
              v_value := v_l.get(j);
              if(v_value.is_array()) then 
                add_to_clob(xmlstr, xmlbuf, '<' || key_str || '>');
                add_to_clob(xmlstr, xmlbuf, escapeStr(v_value.to_char()));
                add_to_clob(xmlstr, xmlbuf, '</' || key_str || '>');
              else
                toString(v_value, key_str, xmlstr, xmlbuf);   
              end if;
            end loop;
          end;
        elsif(v_value.is_null() or (v_value.is_string and v_value.get_string = '')) then
          add_to_clob(xmlstr, xmlbuf, '<' || key_str || '/>');
        else
          toString(v_value, key_str, xmlstr, xmlbuf);   
        end if;
      end loop;

      add_to_clob(xmlstr, xmlbuf, '</' || tagname || '>');
    elsif (obj.is_array()) then
      v_list := json_list(obj);
      for i in 1 .. v_list.count loop
        v_value := v_list.get(i);
        toString(v_value, nvl(tagname, 'array'), xmlstr, xmlbuf);   
      end loop;
    else 
      add_to_clob(xmlstr, xmlbuf, '<' || tagname || '>'||escapeStr(obj.to_char())||'</' || tagname || '>');
    end if;
  end toString;

  function json_to_xml(obj json, tagname varchar2 default 'root') return xmltype as
    xmlstr clob := empty_clob();
    xmlbuf varchar2(32767) := '';
    returnValue xmltype;
  begin
    dbms_lob.createtemporary(xmlstr, true);
    
    toString(obj.to_json_value(), tagname, xmlstr, xmlbuf);
    
    flush_clob(xmlstr, xmlbuf);
    returnValue := xmltype('<?xml version="1.0"?>'||xmlstr);
    dbms_lob.freetemporary(xmlstr);
    return returnValue;
  end;

end json_xml;
