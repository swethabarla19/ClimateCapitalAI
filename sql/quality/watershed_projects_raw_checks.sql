-- Standard SQL. Read-only quality checks for the source-faithful raw snapshot.
-- Every row should pass. failure_details exposes the affected source rows/values.

WITH
  raw_projects AS (
    SELECT
      source_id,
      source_pdf_page,
      source_table_row_order,
      map_label,
      subproject_id,
      project_name,
      current_funding_request_estimate_source,
      current_funding_request_estimate_dollars,
      council_districts_source
    FROM `climatecapital-ai.raw.watershed_projects_2025_11_21`
  ),
  expected_schema AS (
    SELECT *
    FROM UNNEST([
      STRUCT(1 AS ordinal_position, 'source_id' AS column_name, 'STRING' AS data_type, 'NO' AS is_nullable),
      STRUCT(2, 'source_pdf_page', 'INT64', 'NO'),
      STRUCT(3, 'source_table_row_order', 'INT64', 'NO'),
      STRUCT(4, 'map_label', 'STRING', 'NO'),
      STRUCT(5, 'subproject_id', 'STRING', 'NO'),
      STRUCT(6, 'project_name', 'STRING', 'NO'),
      STRUCT(7, 'current_funding_request_estimate_source', 'STRING', 'NO'),
      STRUCT(8, 'current_funding_request_estimate_dollars', 'INT64', 'NO'),
      STRUCT(9, 'council_districts_source', 'STRING', 'NO')
    ])
  ),
  actual_schema AS (
    SELECT ordinal_position, column_name, data_type, is_nullable
    FROM `climatecapital-ai.raw.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'watershed_projects_2025_11_21'
  ),
  schema_mismatches AS (
    SELECT
      COALESCE(expected.ordinal_position, actual.ordinal_position) AS ordinal_position,
      expected.column_name AS expected_name,
      actual.column_name AS actual_name,
      expected.data_type AS expected_type,
      actual.data_type AS actual_type,
      expected.is_nullable AS expected_nullable,
      actual.is_nullable AS actual_nullable
    FROM expected_schema AS expected
    FULL OUTER JOIN actual_schema AS actual
      USING (ordinal_position)
    WHERE
      expected.column_name IS DISTINCT FROM actual.column_name
      OR expected.data_type IS DISTINCT FROM actual.data_type
      OR expected.is_nullable IS DISTINCT FROM actual.is_nullable
  ),
  metrics AS (
    SELECT
      COUNT(*) AS row_count,
      COUNT(DISTINCT subproject_id) AS distinct_subproject_ids,
      SUM(current_funding_request_estimate_dollars) AS funding_total,
      COUNTIF(
        source_id IS NULL
        OR source_pdf_page IS NULL
        OR source_table_row_order IS NULL
        OR map_label IS NULL
        OR subproject_id IS NULL
        OR project_name IS NULL
        OR current_funding_request_estimate_source IS NULL
        OR current_funding_request_estimate_dollars IS NULL
        OR council_districts_source IS NULL
      ) AS required_null_rows,
      COUNTIF(
        source_id IS NULL
        OR source_id != 'austin_wpd_2026_bond_projects_2025_11_21'
      ) AS unexpected_source_id_rows,
      COUNT(DISTINCT source_table_row_order) AS distinct_row_orders,
      MIN(source_table_row_order) AS minimum_row_order,
      MAX(source_table_row_order) AS maximum_row_order,
      COUNTIF(source_table_row_order NOT BETWEEN 1 AND 37) AS out_of_range_row_orders,
      COUNT(DISTINCT map_label) AS distinct_map_labels,
      COUNTIF(source_pdf_page NOT IN (4, 5)) AS unexpected_pdf_pages,
      COUNTIF(source_pdf_page = 4) AS page_4_rows,
      COUNTIF(source_pdf_page = 5) AS page_5_rows,
      COUNTIF(current_funding_request_estimate_dollars <= 0) AS nonpositive_funding_rows
    FROM raw_projects
  ),
  duplicate_subproject_ids AS (
    SELECT subproject_id, COUNT(*) AS duplicate_count
    FROM raw_projects
    GROUP BY subproject_id
    HAVING COUNT(*) > 1
  ),
  duplicate_row_orders AS (
    SELECT source_table_row_order, COUNT(*) AS duplicate_count
    FROM raw_projects
    GROUP BY source_table_row_order
    HAVING COUNT(*) > 1
  ),
  missing_row_orders AS (
    SELECT expected_order
    FROM UNNEST(GENERATE_ARRAY(1, 37)) AS expected_order
    LEFT JOIN raw_projects
      ON source_table_row_order = expected_order
    WHERE source_table_row_order IS NULL
  ),
  expected_map_labels AS (
    SELECT zero_based_order + 1 AS source_table_row_order, expected_map_label
    FROM UNNEST([
      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
      'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK'
    ]) AS expected_map_label WITH OFFSET AS zero_based_order
  ),
  map_label_mismatches AS (
    SELECT
      expected.source_table_row_order,
      expected.expected_map_label,
      actual.map_label AS actual_map_label
    FROM expected_map_labels AS expected
    LEFT JOIN raw_projects AS actual
      USING (source_table_row_order)
    WHERE expected.expected_map_label IS DISTINCT FROM actual.map_label
  ),
  funding_source_mismatches AS (
    SELECT
      source_table_row_order,
      subproject_id,
      current_funding_request_estimate_source AS source_text,
      current_funding_request_estimate_dollars AS normalized_dollars
    FROM raw_projects
    WHERE
      NOT REGEXP_CONTAINS(
        current_funding_request_estimate_source,
        r'^\$[0-9]{1,3}(?:,[0-9]{3})+$'
      )
      OR SAFE_CAST(
        REPLACE(REPLACE(current_funding_request_estimate_source, '$', ''), ',', '')
        AS INT64
      ) IS DISTINCT FROM current_funding_request_estimate_dollars
  ),
  council_district_mismatches AS (
    SELECT source_table_row_order, subproject_id, council_districts_source
    FROM raw_projects
    WHERE
      council_districts_source = ''
      OR NOT REGEXP_CONTAINS(
        council_districts_source,
        r'^(?:[1-9]|10)(?:,(?:[1-9]|10))*$'
      )
      OR (
        SELECT COUNT(*)
        FROM UNNEST(SPLIT(council_districts_source, ','))
      ) != (
        SELECT COUNT(DISTINCT district)
        FROM UNNEST(SPLIT(council_districts_source, ',')) AS district
      )
  ),
  expected_spot_rows AS (
    SELECT *
    FROM UNNEST([
      STRUCT(
        '15_spot_check_first_row' AS check_name,
        1 AS source_table_row_order,
        4 AS source_pdf_page,
        'A' AS map_label,
        '4015.001' AS subproject_id,
        'Country Club Creek (Between Metcalfe & Oltorf) Wastewater Improvements' AS project_name,
        '$5,470,000' AS funding_source,
        5470000 AS funding_dollars,
        '3' AS council_districts_source
      ),
      STRUCT(
        '16_spot_check_page_4_page_5_boundary',
        19,
        4,
        'S',
        '5789.141',
        'Boggy Creek - Oakwood Cemetery Storm Drain Improvements',
        '$7,350,000',
        7350000,
        '1'
      ),
      STRUCT(
        '16_spot_check_page_4_page_5_boundary',
        20,
        5,
        'T',
        '5789.150',
        'Lady Bird Lake – Citywide Storm Drain Renewal Program – Phase 1',
        '$3,000,000',
        3000000,
        '9'
      ),
      STRUCT(
        '17_spot_check_multi_district',
        29,
        5,
        'AC',
        '6039.109',
        'Shoal Creek - Brentwood Integrated Drainage Improvements',
        '$33,500,000',
        33500000,
        '4,7,9'
      ),
      STRUCT(
        '18_spot_check_final_row',
        37,
        5,
        'AK',
        '11889.004',
        'William Cannon Drive Corridor - US 290 to East of Brodie Ln',
        '$2,625,000',
        2625000,
        '5,8'
      )
    ])
  ),
  spot_row_match_counts AS (
    SELECT
      expected.check_name,
      expected.source_table_row_order,
      COUNTIF(
        actual.source_pdf_page = expected.source_pdf_page
        AND actual.map_label = expected.map_label
        AND actual.subproject_id = expected.subproject_id
        AND actual.project_name = expected.project_name
        AND actual.current_funding_request_estimate_source = expected.funding_source
        AND actual.current_funding_request_estimate_dollars = expected.funding_dollars
        AND actual.council_districts_source = expected.council_districts_source
      ) AS exact_match_count
    FROM expected_spot_rows AS expected
    LEFT JOIN raw_projects AS actual
      USING (source_table_row_order)
    GROUP BY expected.check_name, expected.source_table_row_order
  ),
  expected_order_anomaly AS (
    SELECT *
    FROM UNNEST([
      STRUCT(20 AS source_table_row_order, 'T' AS map_label, '5789.150' AS subproject_id),
      STRUCT(21, 'U', '5789.145'),
      STRUCT(22, 'V', '5789.146')
    ])
  ),
  order_anomaly_match_counts AS (
    SELECT
      expected.source_table_row_order,
      COUNTIF(
        actual.map_label = expected.map_label
        AND actual.subproject_id = expected.subproject_id
      ) AS exact_match_count
    FROM expected_order_anomaly AS expected
    LEFT JOIN raw_projects AS actual
      USING (source_table_row_order)
    GROUP BY expected.source_table_row_order
  ),
  source_artifact_fingerprint AS (
    SELECT
      LOWER(TO_HEX(SHA256(STRING_AGG(
        CONCAT(
          source_id, CHR(31),
          CAST(source_pdf_page AS STRING), CHR(31),
          CAST(source_table_row_order AS STRING), CHR(31),
          map_label, CHR(31),
          subproject_id, CHR(31),
          project_name, CHR(31),
          current_funding_request_estimate_source, CHR(31),
          CAST(current_funding_request_estimate_dollars AS STRING), CHR(31),
          council_districts_source
        ),
        '\x1e' ORDER BY source_table_row_order
      )))) AS sha256
    FROM raw_projects
  ),
  quality_results AS (
    SELECT
      '00_schema_contract' AS check_name,
      (SELECT COUNT(*) FROM schema_mismatches) = 0 AS passed,
      '9 ordered REQUIRED columns with governed STRING/INT64 types' AS expected,
      FORMAT('%d schema mismatches', (SELECT COUNT(*) FROM schema_mismatches)) AS observed,
      COALESCE((
        SELECT STRING_AGG(
          FORMAT(
            'position %d expected %s/%s/%s observed %s/%s/%s',
            ordinal_position,
            COALESCE(expected_name, '<missing>'),
            COALESCE(expected_type, '<missing>'),
            COALESCE(expected_nullable, '<missing>'),
            COALESCE(actual_name, '<missing>'),
            COALESCE(actual_type, '<missing>'),
            COALESCE(actual_nullable, '<missing>')
          ),
          '; ' ORDER BY ordinal_position
        )
        FROM schema_mismatches
      ), 'none') AS failure_details
    UNION ALL
    SELECT
      '01_row_count',
      row_count = 37,
      '37',
      CAST(row_count AS STRING),
      IF(row_count = 37, 'none', FORMAT('found %d rows', row_count))
    FROM metrics
    UNION ALL
    SELECT
      '02_distinct_subproject_id_count',
      distinct_subproject_ids = 37,
      '37',
      CAST(distinct_subproject_ids AS STRING),
      IF(
        distinct_subproject_ids = 37,
        'none',
        FORMAT('found %d distinct IDs', distinct_subproject_ids)
      )
    FROM metrics
    UNION ALL
    SELECT
      '03_no_duplicate_subproject_ids',
      (SELECT COUNT(*) FROM duplicate_subproject_ids) = 0,
      'no duplicate subproject_id values',
      FORMAT('%d duplicated IDs', (SELECT COUNT(*) FROM duplicate_subproject_ids)),
      COALESCE((
        SELECT STRING_AGG(
          FORMAT('%s (%d rows)', subproject_id, duplicate_count),
          ', ' ORDER BY subproject_id
        )
        FROM duplicate_subproject_ids
      ), 'none')
    UNION ALL
    SELECT
      '04_funding_request_total',
      IFNULL(funding_total = 327970000, FALSE),
      '327970000',
      COALESCE(CAST(funding_total AS STRING), '<NULL>'),
      IF(
        funding_total = 327970000,
        'none',
        FORMAT('found %s normalized dollars', COALESCE(CAST(funding_total AS STRING), '<NULL>'))
      )
    FROM metrics
    UNION ALL
    SELECT
      '05_required_fields_not_null',
      required_null_rows = 0,
      '0 rows with a NULL governed field',
      FORMAT('%d rows', required_null_rows),
      IF(required_null_rows = 0, 'none', 'one or more governed fields are NULL')
    FROM metrics
    UNION ALL
    SELECT
      '06_source_id_contract',
      unexpected_source_id_rows = 0,
      'austin_wpd_2026_bond_projects_2025_11_21 only',
      FORMAT('%d unexpected rows', unexpected_source_id_rows),
      COALESCE((
        SELECT STRING_AGG(
          FORMAT('%s (%d rows)', COALESCE(source_id, '<NULL>'), source_rows),
          ', ' ORDER BY source_id
        )
        FROM (
          SELECT source_id, COUNT(*) AS source_rows
          FROM raw_projects
          GROUP BY source_id
        )
        WHERE source_id IS NULL OR source_id != 'austin_wpd_2026_bond_projects_2025_11_21'
      ), 'none')
    FROM metrics
    UNION ALL
    SELECT
      '07_source_table_row_order_contract',
      distinct_row_orders = 37
        AND minimum_row_order = 1
        AND maximum_row_order = 37
        AND out_of_range_row_orders = 0
        AND (SELECT COUNT(*) FROM duplicate_row_orders) = 0
        AND (SELECT COUNT(*) FROM missing_row_orders) = 0,
      '37 unique contiguous integers from 1 through 37',
      FORMAT(
        'distinct=%d min=%d max=%d out_of_range=%d duplicates=%d missing=%d',
        distinct_row_orders,
        minimum_row_order,
        maximum_row_order,
        out_of_range_row_orders,
        (SELECT COUNT(*) FROM duplicate_row_orders),
        (SELECT COUNT(*) FROM missing_row_orders)
      ),
      IF(
        distinct_row_orders = 37
          AND minimum_row_order = 1
          AND maximum_row_order = 37
          AND out_of_range_row_orders = 0
          AND (SELECT COUNT(*) FROM duplicate_row_orders) = 0
          AND (SELECT COUNT(*) FROM missing_row_orders) = 0,
        'none',
        'row-order range, uniqueness, or continuity failed'
      )
    FROM metrics
    UNION ALL
    SELECT
      '08_map_label_unique',
      distinct_map_labels = 37,
      '37 unique map_label values',
      FORMAT('%d distinct labels', distinct_map_labels),
      IF(distinct_map_labels = 37, 'none', 'map_label values are missing or duplicated')
    FROM metrics
    UNION ALL
    SELECT
      '09_map_label_source_sequence',
      (SELECT COUNT(*) FROM map_label_mismatches) = 0,
      'A through AK in source_table_row_order',
      FORMAT('%d mismatches', (SELECT COUNT(*) FROM map_label_mismatches)),
      COALESCE((
        SELECT STRING_AGG(
          FORMAT(
            'row %d expected %s observed %s',
            source_table_row_order,
            expected_map_label,
            COALESCE(actual_map_label, '<missing>')
          ),
          '; ' ORDER BY source_table_row_order
        )
        FROM map_label_mismatches
      ), 'none')
    UNION ALL
    SELECT
      '10_source_pdf_page_domain',
      unexpected_pdf_pages = 0,
      'physical PDF pages 4 or 5 only',
      FORMAT('%d unexpected rows', unexpected_pdf_pages),
      IF(unexpected_pdf_pages = 0, 'none', 'one or more source_pdf_page values are outside 4/5')
    FROM metrics
    UNION ALL
    SELECT
      '11_source_pdf_page_counts',
      page_4_rows = 19 AND page_5_rows = 18,
      'page 4 = 19 rows; page 5 = 18 rows',
      FORMAT('page 4 = %d; page 5 = %d', page_4_rows, page_5_rows),
      IF(page_4_rows = 19 AND page_5_rows = 18, 'none', 'page boundary counts differ')
    FROM metrics
    UNION ALL
    SELECT
      '12_funding_amounts_positive',
      nonpositive_funding_rows = 0,
      'all normalized INTEGER dollars > 0',
      FORMAT('%d nonpositive rows', nonpositive_funding_rows),
      IF(nonpositive_funding_rows = 0, 'none', 'one or more normalized amounts are nonpositive')
    FROM metrics
    UNION ALL
    SELECT
      '13_funding_source_text_reconciles',
      (SELECT COUNT(*) FROM funding_source_mismatches) = 0,
      'source currency text parses exactly to normalized INTEGER dollars',
      FORMAT('%d mismatches', (SELECT COUNT(*) FROM funding_source_mismatches)),
      COALESCE((
        SELECT STRING_AGG(
          FORMAT(
            'row %d %s source=%s normalized=%d',
            source_table_row_order,
            subproject_id,
            source_text,
            normalized_dollars
          ),
          '; ' ORDER BY source_table_row_order
        )
        FROM funding_source_mismatches
      ), 'none')
    UNION ALL
    SELECT
      '14_council_district_source_contract',
      (SELECT COUNT(*) FROM council_district_mismatches) = 0,
      'nonempty source strings containing unique comma-separated districts 1–10',
      FORMAT('%d invalid rows', (SELECT COUNT(*) FROM council_district_mismatches)),
      COALESCE((
        SELECT STRING_AGG(
          FORMAT(
            'row %d %s districts=%s',
            source_table_row_order,
            subproject_id,
            council_districts_source
          ),
          '; ' ORDER BY source_table_row_order
        )
        FROM council_district_mismatches
      ), 'none')
    UNION ALL
    SELECT
      check_name,
      COUNTIF(exact_match_count != 1) = 0,
      'each source-verified row matches all governed fields exactly once',
      FORMAT(
        '%d of %d expected rows matched exactly once',
        COUNTIF(exact_match_count = 1),
        COUNT(*)
      ),
      COALESCE(STRING_AGG(
        IF(
          exact_match_count != 1,
          FORMAT('row %d exact matches=%d', source_table_row_order, exact_match_count),
          NULL
        ),
        '; ' ORDER BY source_table_row_order
      ), 'none')
    FROM spot_row_match_counts
    GROUP BY check_name
    UNION ALL
    SELECT
      '19_spot_check_preserved_id_order_anomaly',
      COUNTIF(exact_match_count != 1) = 0,
      '20/T/5789.150, 21/U/5789.145, 22/V/5789.146',
      FORMAT('%d of 3 anomaly rows matched', COUNTIF(exact_match_count = 1)),
      COALESCE(STRING_AGG(
        IF(
          exact_match_count != 1,
          FORMAT('row %d exact matches=%d', source_table_row_order, exact_match_count),
          NULL
        ),
        '; ' ORDER BY source_table_row_order
      ), 'none')
    FROM order_anomaly_match_counts
    UNION ALL
    SELECT
      '20_full_source_artifact_fidelity',
      IFNULL(
        sha256 = 'c9091117734b2f793ed5f396dba3b8897169ad168659df0fe4f97cd92aeb072a',
        FALSE
      ),
      'canonical semantic SHA-256 c9091117734b2f793ed5f396dba3b8897169ad168659df0fe4f97cd92aeb072a',
      CONCAT('canonical semantic SHA-256 ', COALESCE(sha256, '<NULL>')),
      IF(
        sha256 = 'c9091117734b2f793ed5f396dba3b8897169ad168659df0fe4f97cd92aeb072a',
        'none',
        'one or more ordered governed field values differ from the committed CSV'
      )
    FROM source_artifact_fingerprint
  )
SELECT check_name, passed, expected, observed, failure_details
FROM quality_results
ORDER BY check_name;
