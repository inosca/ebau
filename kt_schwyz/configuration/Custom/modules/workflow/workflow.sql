--------------------------------------------------------
--  File created - Friday-October-31-2014   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Sequence WORKFLOW_ENTRY_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "WORKFLOW_ENTRY_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 2 CACHE 20 NOORDER  NOCYCLE ;
--------------------------------------------------------
--  DDL for Sequence WORKFLOW_ITEM_SEQ
--------------------------------------------------------

   CREATE SEQUENCE  "WORKFLOW_ITEM_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 81 CACHE 20 NOORDER  NOCYCLE ;
--------------------------------------------------------
--  DDL for Table WORKFLOW_ACTION
--------------------------------------------------------

  CREATE TABLE "WORKFLOW_ACTION" 
   (	"ACTION_ID" NUMBER, 
	"WORKFLOW_ITEM_ID" NUMBER
   ) ;
--------------------------------------------------------
--  DDL for Table WORKFLOW_ENTRY
--------------------------------------------------------

  CREATE TABLE "WORKFLOW_ENTRY" 
   (	"WORKFLOW_ENTRY_ID" NUMBER, 
	"WORKFLOW_DATE" DATE, 
	"INSTANCE_ID" NUMBER, 
	"WORKFLOW_ITEM_ID" NUMBER
   ) ;
--------------------------------------------------------
--  DDL for Table WORKFLOW_ITEM
--------------------------------------------------------

  CREATE TABLE "WORKFLOW_ITEM" 
   (	"WORKFLOW_ITEM_ID" NUMBER, 
	"POSITION" NUMBER, 
	"NAME" VARCHAR2(255), 
	"AUTOMATICAL" NUMBER(1,0) DEFAULT 0, 
	"DIFFERENT_COLOR" NUMBER(1,0) DEFAULT 0
   ) ;
--------------------------------------------------------
--  DDL for Table WORKFLOW_ROLE
--------------------------------------------------------

  CREATE TABLE "WORKFLOW_ROLE" 
   (	"WORKFLOW_ITEM_ID" NUMBER, 
	"ROLE_ID" NUMBER
   ) ;
--------------------------------------------------------
--  DDL for Index WORKFLOW_ACTION_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "WORKFLOW_ACTION_PK" ON "WORKFLOW_ACTION" ("ACTION_ID") 
  ;
--------------------------------------------------------
--  DDL for Index WORKFLOW_ENTRY_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "WORKFLOW_ENTRY_PK" ON "WORKFLOW_ENTRY" ("WORKFLOW_ENTRY_ID") 
  ;
--------------------------------------------------------
--  DDL for Index WORKFLOW_ITEM_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "WORKFLOW_ITEM_PK" ON "WORKFLOW_ITEM" ("WORKFLOW_ITEM_ID") 
  ;
--------------------------------------------------------
--  DDL for Index WORKFLOW_ROLE_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "WORKFLOW_ROLE_PK" ON "WORKFLOW_ROLE" ("ROLE_ID", "WORKFLOW_ITEM_ID") 
  ;
--------------------------------------------------------
--  Constraints for Table WORKFLOW_ACTION
--------------------------------------------------------

  ALTER TABLE "WORKFLOW_ACTION" ADD CONSTRAINT "WORKFLOW_ACTION_PK" PRIMARY KEY ("ACTION_ID") ENABLE;
  ALTER TABLE "WORKFLOW_ACTION" MODIFY ("WORKFLOW_ITEM_ID" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ACTION" MODIFY ("ACTION_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table WORKFLOW_ENTRY
--------------------------------------------------------

  ALTER TABLE "WORKFLOW_ENTRY" ADD CONSTRAINT "WORKFLOW_ENTRY_PK" PRIMARY KEY ("WORKFLOW_ENTRY_ID") ENABLE;
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("WORKFLOW_ITEM_ID" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("INSTANCE_ID" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("WORKFLOW_DATE" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("WORKFLOW_ENTRY_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table WORKFLOW_ITEM
--------------------------------------------------------

  ALTER TABLE "WORKFLOW_ITEM" ADD CONSTRAINT "WORKFLOW_ITEM_PK" PRIMARY KEY ("WORKFLOW_ITEM_ID") ENABLE;
  ALTER TABLE "WORKFLOW_ITEM" MODIFY ("DIFFERENT_COLOR" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ITEM" MODIFY ("AUTOMATICAL" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ITEM" MODIFY ("NAME" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ITEM" MODIFY ("POSITION" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ITEM" MODIFY ("WORKFLOW_ITEM_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Constraints for Table WORKFLOW_ROLE
--------------------------------------------------------

  ALTER TABLE "WORKFLOW_ROLE" ADD CONSTRAINT "WORKFLOW_ROLE_PK" PRIMARY KEY ("ROLE_ID", "WORKFLOW_ITEM_ID") ENABLE;
  ALTER TABLE "WORKFLOW_ROLE" MODIFY ("ROLE_ID" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ROLE" MODIFY ("WORKFLOW_ITEM_ID" NOT NULL ENABLE);
--------------------------------------------------------
--  Ref Constraints for Table WORKFLOW_ACTION
--------------------------------------------------------

  ALTER TABLE "WORKFLOW_ACTION" ADD CONSTRAINT "WORKFLOW_ACTION_FK1" FOREIGN KEY ("ACTION_ID")
	  REFERENCES "ACTION" ("ACTION_ID") ENABLE;
  ALTER TABLE "WORKFLOW_ACTION" ADD CONSTRAINT "WORKFLOW_ACTION_FK2" FOREIGN KEY ("WORKFLOW_ITEM_ID")
	  REFERENCES "WORKFLOW_ITEM" ("WORKFLOW_ITEM_ID") ENABLE;
--------------------------------------------------------
--  Ref Constraints for Table WORKFLOW_ENTRY
--------------------------------------------------------

  ALTER TABLE "WORKFLOW_ENTRY" ADD CONSTRAINT "WORKFLOW_ENTRY_INSTANCE" FOREIGN KEY ("INSTANCE_ID")
	  REFERENCES "INSTANCE" ("INSTANCE_ID") ON DELETE CASCADE ENABLE;
  ALTER TABLE "WORKFLOW_ENTRY" ADD CONSTRAINT "WORKFLOW_ENTRY_WORKFLOW" FOREIGN KEY ("WORKFLOW_ITEM_ID")
	  REFERENCES "WORKFLOW_ITEM" ("WORKFLOW_ITEM_ID") ON DELETE CASCADE ENABLE;
--------------------------------------------------------
--  Ref Constraints for Table WORKFLOW_ROLE
--------------------------------------------------------

  ALTER TABLE "WORKFLOW_ROLE" ADD CONSTRAINT "WORKFLOW_ROLE_ROLE" FOREIGN KEY ("ROLE_ID")
	  REFERENCES "ROLE" ("ROLE_ID") ON DELETE CASCADE ENABLE;
  ALTER TABLE "WORKFLOW_ROLE" ADD CONSTRAINT "WORKFLOW_ROLE_WORKFLOW" FOREIGN KEY ("WORKFLOW_ITEM_ID")
	  REFERENCES "WORKFLOW_ITEM" ("WORKFLOW_ITEM_ID") ON DELETE CASCADE ENABLE;
--------------------------------------------------------
--  DDL for Trigger WORKFLOW_ENTRY_TRG
--------------------------------------------------------

  CREATE OR REPLACE TRIGGER "WORKFLOW_ENTRY_TRG" 
BEFORE INSERT ON WORKFLOW_ENTRY 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.WORKFLOW_ENTRY_ID IS NULL THEN
      SELECT WORKFLOW_ENTRY_SEQ.NEXTVAL INTO :NEW.WORKFLOW_ENTRY_ID FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
/
ALTER TRIGGER "WORKFLOW_ENTRY_TRG" ENABLE;
--------------------------------------------------------
--  DDL for Trigger WORKFLOW_ITEM_TRG
--------------------------------------------------------

  CREATE OR REPLACE TRIGGER "WORKFLOW_ITEM_TRG" BEFORE INSERT ON WORKFLOW_ITEM 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.WORKFLOW_ITEM_ID IS NULL THEN
      SELECT WORKFLOW_ITEM_SEQ.NEXTVAL INTO :NEW.WORKFLOW_ITEM_ID FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
/
ALTER TRIGGER "WORKFLOW_ITEM_TRG" ENABLE;

-- Data for the instance resource
Insert into AVAILABLE_INSTANCE_RESOURCE (AVAILABLE_INSTANCE_RESOURCE_ID,MODULE_NAME,CONTROLLER_NAME,DESCRIPTION) values ('workflow','workflow','list','Show the workflow entries');

Insert into AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('workflow','list',0);
Insert into AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('workflow','save',1);
Insert into AIR_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,ACTION_NAME,HIDDEN) values ('workflow','delete',1);

-- Data for the Action
Insert into AVAILABLE_ACTION (AVAILABLE_ACTION_ID,MODULE_NAME,DESCRIPTION) values ('workflow','workflow','Set Workflow Date');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('newform','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('formpages','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editnotice','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpages','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('page','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editcirculation','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('circulation','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('allformpages','workflow');
Insert into INSTANCE_RESOURCE_ACTION (AVAILABLE_INSTANCE_RESOURCE_ID,AVAILABLE_ACTION_ID) values ('editformpage','workflow');
