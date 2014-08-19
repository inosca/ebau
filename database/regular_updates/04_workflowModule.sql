-- ------------------------------------------------------
--  File created - Tuesday-August-19-2014   
-- ------------------------------------------------------
-- ------------------------------------------------------
--  DDL for Sequence WORKFLOW_ENTRY_SEQ
-- ------------------------------------------------------

   CREATE SEQUENCE  "WORKFLOW_ENTRY_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE;
-- ------------------------------------------------------
--  DDL for Sequence WORKFLOW_SEQ
-- ------------------------------------------------------

   CREATE SEQUENCE  "WORKFLOW_SEQ"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE;
-- ------------------------------------------------------
--  DDL for Table WORKFLOW
-- ------------------------------------------------------

  CREATE TABLE "WORKFLOW" 
   (	"WORKFLOW_ID" NUMBER, 
	"POSITION" NUMBER, 
	"NAME" VARCHAR2(255), 
	"AUTOMATICAL" NUMBER(1,0) DEFAULT 0, 
	"DIFFERENT_COLOR" NUMBER(1,0) DEFAULT 0
   );
-- ------------------------------------------------------
--  DDL for Table WORKFLOW_ENTRY
-- ------------------------------------------------------

  CREATE TABLE "WORKFLOW_ENTRY" 
   (	"WORKFLOW_ENTRY_ID" NUMBER, 
	"WORKFLOW_DATE" DATE, 
	"INSTANCE_ID" NUMBER, 
	"WORKFLOW_ID" NUMBER
   );
-- ------------------------------------------------------
--  DDL for Table WORKFLOW_ROLE
-- ------------------------------------------------------

  CREATE TABLE "WORKFLOW_ROLE" 
   (	"WORKFLOW_ID" NUMBER, 
	"ROLE_ID" NUMBER
   );
-- ------------------------------------------------------
--  DDL for Index WORKFLOW_ENTRY_PK
-- ------------------------------------------------------

  CREATE UNIQUE INDEX "WORKFLOW_ENTRY_PK" ON "WORKFLOW_ENTRY" ("WORKFLOW_ENTRY_ID");
-- ------------------------------------------------------
--  DDL for Index WORKFLOW_PK
-- ------------------------------------------------------

  CREATE UNIQUE INDEX "WORKFLOW_PK" ON "WORKFLOW" ("WORKFLOW_ID");
-- ------------------------------------------------------
--  DDL for Index WORKFLOW_ROLE_PK
-- ------------------------------------------------------

  CREATE UNIQUE INDEX "WORKFLOW_ROLE_PK" ON "WORKFLOW_ROLE" ("ROLE_ID", "WORKFLOW_ID");
-- ------------------------------------------------------
--  Constraints for Table WORKFLOW
-- ------------------------------------------------------

  ALTER TABLE "WORKFLOW" ADD CONSTRAINT "WORKFLOW_PK" PRIMARY KEY ("WORKFLOW_ID") ENABLE;
  ALTER TABLE "WORKFLOW" MODIFY ("DIFFERENT_COLOR" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW" MODIFY ("AUTOMATICAL" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW" MODIFY ("NAME" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW" MODIFY ("POSITION" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW" MODIFY ("WORKFLOW_ID" NOT NULL ENABLE);
-- ------------------------------------------------------
--  Constraints for Table WORKFLOW_ENTRY
-- ------------------------------------------------------

  ALTER TABLE "WORKFLOW_ENTRY" ADD CONSTRAINT "WORKFLOW_ENTRY_PK" PRIMARY KEY ("WORKFLOW_ENTRY_ID") ENABLE;
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("WORKFLOW_ID" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("INSTANCE_ID" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("WORKFLOW_DATE" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ENTRY" MODIFY ("WORKFLOW_ENTRY_ID" NOT NULL ENABLE);
-- ------------------------------------------------------
--  Constraints for Table WORKFLOW_ROLE
-- ------------------------------------------------------

  ALTER TABLE "WORKFLOW_ROLE" ADD CONSTRAINT "WORKFLOW_ROLE_PK" PRIMARY KEY ("ROLE_ID", "WORKFLOW_ID") ENABLE;
  ALTER TABLE "WORKFLOW_ROLE" MODIFY ("ROLE_ID" NOT NULL ENABLE);
  ALTER TABLE "WORKFLOW_ROLE" MODIFY ("WORKFLOW_ID" NOT NULL ENABLE);
-- ------------------------------------------------------
--  Ref Constraints for Table WORKFLOW_ENTRY
-- ------------------------------------------------------

  ALTER TABLE "WORKFLOW_ENTRY" ADD CONSTRAINT "WORKFLOW_ENTRY_INSTANCE" FOREIGN KEY ("INSTANCE_ID")
	  REFERENCES "INSTANCE" ("INSTANCE_ID") ON DELETE CASCADE ENABLE;
  ALTER TABLE "WORKFLOW_ENTRY" ADD CONSTRAINT "WORKFLOW_ENTRY_WORKFLOW" FOREIGN KEY ("WORKFLOW_ID")
	  REFERENCES "WORKFLOW" ("WORKFLOW_ID") ON DELETE CASCADE ENABLE;
-- ------------------------------------------------------
--  Ref Constraints for Table WORKFLOW_ROLE
-- ------------------------------------------------------

  ALTER TABLE "WORKFLOW_ROLE" ADD CONSTRAINT "WORKFLOW_ROLE_ROLE" FOREIGN KEY ("ROLE_ID")
	  REFERENCES "ROLE" ("ROLE_ID") ON DELETE CASCADE ENABLE;
  ALTER TABLE "WORKFLOW_ROLE" ADD CONSTRAINT "WORKFLOW_ROLE_WORKFLOW" FOREIGN KEY ("WORKFLOW_ID")
	  REFERENCES "WORKFLOW" ("WORKFLOW_ID") ON DELETE CASCADE ENABLE;
-- ------------------------------------------------------
--  DDL for Trigger WORKFLOW_ENTRY_TRG
-- ------------------------------------------------------

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
ALTER TRIGGER "WORKFLOW_ENTRY_TRG" ENABLE;
-- ------------------------------------------------------
--  DDL for Trigger WORKFLOW_TRG
-- ------------------------------------------------------

  CREATE OR REPLACE TRIGGER "WORKFLOW_TRG" 
BEFORE INSERT ON WORKFLOW 
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.WORKFLOW_ID IS NULL THEN
      SELECT WORKFLOW_SEQ.NEXTVAL INTO :NEW.WORKFLOW_ID FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
ALTER TRIGGER "WORKFLOW_TRG" ENABLE;
