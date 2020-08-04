VIEWS = [
    (
        "ANSWER_DOK_NR",
        """
        CREATE OR REPLACE VIEW public."ANSWER_DOK_NR" AS
         SELECT "ANSWER"."ANSWER",
            "ANSWER"."INSTANCE_ID"
           FROM public."ANSWER"
          WHERE (("ANSWER"."QUESTION_ID" = 6) AND ("ANSWER"."CHAPTER_ID" = 2) AND ("ANSWER"."ITEM" = 1));
        """,
    ),
    (
        "ANSWER_STREET_247",
        """
        CREATE OR REPLACE VIEW public."ANSWER_STREET_247" AS
         SELECT "ANSWER"."ANSWER",
            "ANSWER"."INSTANCE_ID"
           FROM public."ANSWER"
          WHERE (("ANSWER"."QUESTION_ID" = 93) AND ("ANSWER"."CHAPTER_ID" = 102) AND ("ANSWER"."ITEM" = 1));
        """,
    ),
    (
        "ANSWER_STREET_BG",
        """
        CREATE OR REPLACE VIEW public."ANSWER_STREET_BG" AS
         SELECT "ANSWER"."ANSWER",
            "ANSWER"."INSTANCE_ID"
           FROM public."ANSWER"
          WHERE (("ANSWER"."QUESTION_ID" = 93) AND ("ANSWER"."CHAPTER_ID" = 21) AND ("ANSWER"."ITEM" = 1));
        """,
    ),
    (
        "ANSWER_STREET_NP",
        """
        CREATE OR REPLACE VIEW public."ANSWER_STREET_NP" AS
         SELECT "ANSWER"."ANSWER",
            "ANSWER"."INSTANCE_ID"
           FROM public."ANSWER"
          WHERE (("ANSWER"."QUESTION_ID" = 93) AND ("ANSWER"."CHAPTER_ID" = 101) AND ("ANSWER"."ITEM" = 1));
        """,
    ),
    (
        "APPLICANT_DATA_VIEW",
        """
        CREATE OR REPLACE VIEW public."APPLICANT_DATA_VIEW" AS
         SELECT "NAME_TBL"."ANSWER" AS "NAME",
            "EMAIL_TBL"."ANSWER" AS "EMAIL",
            "NAME_TBL"."INSTANCE_ID"
           FROM (public."ANSWER" "NAME_TBL"
             JOIN public."ANSWER" "EMAIL_TBL" ON ((("EMAIL_TBL"."CHAPTER_ID" = 1) AND ("EMAIL_TBL"."QUESTION_ID" = 66) AND ("EMAIL_TBL"."ITEM" = 1))))
          WHERE (("NAME_TBL"."CHAPTER_ID" = 1) AND ("NAME_TBL"."QUESTION_ID" = 23) AND ("NAME_TBL"."ITEM" = 1) AND ("NAME_TBL"."INSTANCE_ID" = "EMAIL_TBL"."INSTANCE_ID"));
        """,
    ),
    (
        "APPLICANT_VIEW",
        """
        CREATE OR REPLACE VIEW public."APPLICANT_VIEW" AS
         SELECT "INSTANCE"."INSTANCE_ID",
            ( SELECT string_agg(("ANSWER"."ANSWER")::text, ', '::text ORDER BY "ANSWER"."QUESTION_ID" DESC) AS string_agg
                   FROM public."ANSWER"
                  WHERE (("INSTANCE"."INSTANCE_ID" = "ANSWER"."INSTANCE_ID") AND (("ANSWER"."QUESTION_ID" = 23) OR ("ANSWER"."QUESTION_ID" = 221)) AND ("ANSWER"."CHAPTER_ID" = 1) AND ("ANSWER"."ITEM" = 1))) AS "APPLICANT"
           FROM public."INSTANCE";
        """,
    ),
    (
        "BILLING_ENTRY_ACTUAL_AMOUNT",
        """
        CREATE OR REPLACE VIEW public."BILLING_ENTRY_ACTUAL_AMOUNT" AS
         SELECT
                CASE "BILLING_ENTRY"."AMOUNT_TYPE"
                    WHEN 0 THEN "BILLING_ENTRY"."AMOUNT"
                    WHEN 1 THEN ("BILLING_ENTRY"."AMOUNT" * ((( SELECT "BILLING_CONFIG"."VALUE"
                       FROM public."BILLING_CONFIG"
                      WHERE (("BILLING_CONFIG"."NAME")::text = 'hourly_rate'::text)))::integer)::double precision)
                    WHEN 2 THEN (("BILLING_ENTRY"."AMOUNT" * ((( SELECT "BILLING_CONFIG"."VALUE"
                       FROM public."BILLING_CONFIG"
                      WHERE (("BILLING_CONFIG"."NAME")::text = 'hourly_rate'::text)))::integer)::double precision) / (2)::double precision)
                    ELSE NULL::double precision
                END AS "ACTUAL_AMOUNT",
            "BILLING_ENTRY"."BILLING_ENTRY_ID"
           FROM public."BILLING_ENTRY";
        """,
    ),
    (
        "BILLING_ENTRY_TYPE",
        """
        CREATE OR REPLACE VIEW public."BILLING_ENTRY_TYPE" AS
         SELECT
                CASE "BILLING_ENTRY"."TYPE"
                    WHEN 0 THEN 'BEW'::text
                    WHEN 1 THEN 'BGL'::text
                    ELSE NULL::text
                END AS "TYPE",
            "BILLING_ENTRY"."BILLING_ENTRY_ID"
           FROM public."BILLING_ENTRY";
        """,
    ),
    (
        "OTHER_INTENTIONS",
        """
        CREATE OR REPLACE VIEW public."OTHER_INTENTIONS" AS
         SELECT "ANSWER"."ANSWER",
            "ANSWER"."INSTANCE_ID"
           FROM public."ANSWER"
          WHERE ((("ANSWER"."QUESTION_ID" = 98) AND (("ANSWER"."CHAPTER_ID" = 21) OR ("ANSWER"."CHAPTER_ID" = 101)) AND ("ANSWER"."ITEM" = 1)) OR (("ANSWER"."QUESTION_ID" = 244) AND ("ANSWER"."CHAPTER_ID" = 102)));
        """,
    ),
    (
        "PRESET_INTENTIONS",
        """
        CREATE OR REPLACE VIEW public."PRESET_INTENTIONS" AS
         SELECT "ANSWER_LIST"."NAME",
            "ANSWER_LIST"."VALUE",
            "ANSWER"."INSTANCE_ID"
           FROM (public."ANSWER_LIST"
             JOIN public."ANSWER" ON ((("ANSWER"."QUESTION_ID" = 97) AND ("ANSWER"."CHAPTER_ID" = 21) AND ("ANSWER"."ITEM" = 1))))
          WHERE (("ANSWER_LIST"."QUESTION_ID" = 97) AND (("ANSWER"."ANSWER")::jsonb ? ("ANSWER_LIST"."VALUE")::text));
        """,
    ),
    (
        "INTENTIONS",
        """
        CREATE OR REPLACE VIEW public."INTENTIONS" AS
         SELECT "PRESET_INTENTIONS"."NAME",
            "PRESET_INTENTIONS"."INSTANCE_ID"
           FROM public."PRESET_INTENTIONS"
        UNION
         SELECT "OTHER_INTENTIONS"."ANSWER" AS "NAME",
            "OTHER_INTENTIONS"."INSTANCE_ID"
           FROM public."OTHER_INTENTIONS";
        """,
    ),
    (
        "PROJECT_AUTHOR_DATA_VIEW",
        """
        CREATE OR REPLACE VIEW public."PROJECT_AUTHOR_DATA_VIEW" AS
         SELECT "NAME_TBL"."ANSWER" AS "NAME",
            "EMAIL_TBL"."ANSWER" AS "EMAIL",
            "NAME_TBL"."INSTANCE_ID"
           FROM (public."ANSWER" "NAME_TBL"
             JOIN public."ANSWER" "EMAIL_TBL" ON ((("EMAIL_TBL"."CHAPTER_ID" = 1) AND ("EMAIL_TBL"."QUESTION_ID" = 77) AND ("EMAIL_TBL"."ITEM" = 1))))
          WHERE (("NAME_TBL"."CHAPTER_ID" = 1) AND ("NAME_TBL"."QUESTION_ID" = 71) AND ("NAME_TBL"."ITEM" = 1) AND ("NAME_TBL"."INSTANCE_ID" = "EMAIL_TBL"."INSTANCE_ID"));
        """,
    ),
    (
        "PROJECT_SUBMITTER_VIEW",
        """
        CREATE OR REPLACE VIEW public."PROJECT_SUBMITTER_VIEW" AS
         SELECT "INSTANCE"."INSTANCE_ID",
            COALESCE("NAME_TBL"."ANSWER", '0'::character varying) AS "ANSWER"
           FROM (public."INSTANCE"
             LEFT JOIN public."ANSWER" "NAME_TBL" ON ((("NAME_TBL"."CHAPTER_ID" = 103) AND ("NAME_TBL"."QUESTION_ID" = 257) AND ("NAME_TBL"."ITEM" = 1) AND ("INSTANCE"."INSTANCE_ID" = "NAME_TBL"."INSTANCE_ID"))));
         """,
    ),
    (
        "PROJECT_SUBMITTER_DATA",
        """
        CREATE OR REPLACE VIEW public."PROJECT_SUBMITTER_DATA" AS
         SELECT
                CASE "PROJECT_SUBMITTER_VIEW"."ANSWER"
                    WHEN '0'::text THEN "APPLICANT_DATA_VIEW"."NAME"
                    WHEN '1'::text THEN "PROJECT_AUTHOR_DATA_VIEW"."NAME"
                    ELSE NULL::character varying
                END AS "NAME",
                CASE "PROJECT_SUBMITTER_VIEW"."ANSWER"
                    WHEN '0'::text THEN "APPLICANT_DATA_VIEW"."EMAIL"
                    WHEN '1'::text THEN "PROJECT_AUTHOR_DATA_VIEW"."EMAIL"
                    ELSE NULL::character varying
                END AS "EMAIL",
            "PROJECT_SUBMITTER_VIEW"."INSTANCE_ID",
            "PROJECT_SUBMITTER_VIEW"."ANSWER"
           FROM ((public."PROJECT_SUBMITTER_VIEW"
             LEFT JOIN public."APPLICANT_DATA_VIEW" ON (("PROJECT_SUBMITTER_VIEW"."INSTANCE_ID" = "APPLICANT_DATA_VIEW"."INSTANCE_ID")))
             LEFT JOIN public."PROJECT_AUTHOR_DATA_VIEW" ON (("PROJECT_SUBMITTER_VIEW"."INSTANCE_ID" = "PROJECT_AUTHOR_DATA_VIEW"."INSTANCE_ID")));
         """,
    ),
]


def drop_view_sql():
    return "\n".join([f"""DROP VIEW "{view}";""" for view, _ in reversed(VIEWS)])


def create_view_sql():
    return "\n".join([view_sql for _, view_sql in VIEWS])
