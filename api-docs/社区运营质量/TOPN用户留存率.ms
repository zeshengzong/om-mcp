{
  "properties" : { },
  "id" : "9baad7c69b5248588d6e23e74485a1ad",
  "script" : null,
  "groupId" : "2e2220ca1c424052ba4fa20a1e7370f8",
  "name" : "TOPN用户留存率",
  "createTime" : null,
  "updateTime" : 1773367242261,
  "lock" : null,
  "createBy" : null,
  "updateBy" : "admin",
  "path" : "/user_retention",
  "method" : "GET",
  "parameters" : [ {
    "name" : "community",
    "value" : "mindie",
    "description" : null,
    "required" : true,
    "dataType" : "String",
    "type" : null,
    "defaultValue" : null,
    "validateType" : null,
    "error" : null,
    "expression" : null,
    "children" : null
  }, {
    "name" : "date",
    "value" : "1765689600000",
    "description" : "查询时间,格式为毫秒时间戳",
    "required" : false,
    "dataType" : "Long",
    "type" : null,
    "defaultValue" : null,
    "validateType" : null,
    "error" : null,
    "expression" : null,
    "children" : null
  }],
  "options" : [ {
    "name" : "wrap_request_parameter",
    "value" : "disable-cache",
    "description" : "包装请求参数到一个变量中",
    "required" : false,
    "dataType" : "String",
    "type" : null,
    "defaultValue" : null,
    "validateType" : null,
    "error" : null,
    "expression" : null,
    "children" : null
  } ],
  "requestBody" : "",
  "headers" : [ ],
  "paths" : [ ],
  "responseBody" : null,
  "description" : "查询指定社区的TOP开发者留存率。",
  "requestBodyDefinition" : null,
  "responseBodyDefinition" : null
}
================================
community = community.toLowerCase()


var sql = """
WITH
user_count_merged AS (
    SELECT user_login, SUM(merged_pr_incre) AS count
    FROM dws_${community}_contribute_repo_user_daily dcc
    WHERE private <> 'false'
        <if test="date != null and date != ''">
            AND date >= (to_timestamp(#{date}/1000) AT TIME ZONE 'Asia/Shanghai')::date - INTERVAL '1 year'
            AND date <= (to_timestamp(#{date}/1000) AT TIME ZONE 'Asia/Shanghai')::date
        </if>
       AND NOT EXISTS (
          SELECT 1 FROM fact_community_robot_user fcru
          WHERE fcru.user_login = dcc.user_login
       )
    GROUP BY user_login
),
total_merged AS (
    SELECT SUM(count) AS s FROM user_count_merged
),
merged_result AS (
    SELECT user_login, count, running_total
    FROM (
        SELECT user_login, count,
               SUM(count) OVER (ORDER BY count DESC) AS running_total
        FROM user_count_merged
    ) t, total_merged
    WHERE running_total - count < 0.8 * total_merged.s
),
user_count_comment AS (
    SELECT user_login, SUM(comment_incre) AS count
    FROM dws_${community}_contribute_repo_user_daily dcc
    WHERE private = 'false'
        <if test="date != null and date != ''">
            AND date >= (to_timestamp(#{date}/1000) AT TIME ZONE 'Asia/Shanghai')::date - INTERVAL '1 year'
            AND date <= (to_timestamp(#{date}/1000) AT TIME ZONE 'Asia/Shanghai')::date
        </if>
       AND NOT EXISTS (
          SELECT 1 FROM fact_community_robot_user fcru
          WHERE fcru.user_login = dcc.user_login
       )
    GROUP BY user_login
),
total_comment AS (
    SELECT SUM(count) AS s FROM user_count_comment
),
comment_result AS (
    SELECT user_login, count, running_total
    FROM (
        SELECT user_login, count,
               SUM(count) OVER (ORDER BY count DESC) AS running_total
        FROM user_count_comment
    ) t, total_comment
    WHERE running_total - count < 0.8 * total_comment.s
),
history_user AS (
    SELECT user_login FROM merged_result
    UNION
    SELECT user_login FROM comment_result
),
cur_user AS (
    SELECT distinct user_login
    FROM dws_${community}_contribute_repo_user_daily dcc
    WHERE private = 'false'
        <if test="date != null and date != ''">
            AND date >= (to_timestamp(#{date}/1000) AT TIME ZONE 'Asia/Shanghai')::date - INTERVAL '1 year'
            AND date <= (to_timestamp(#{date}/1000) AT TIME ZONE 'Asia/Shanghai')::date
        </if>
       AND NOT EXISTS (
          SELECT 1 FROM fact_community_robot_user fcru
          WHERE fcru.user_login = dcc.user_login
       )
)
SELECT
    COUNT(*) FILTER (WHERE c.user_login IS NOT NULL) * 1.0 / COUNT(*) AS ratio
FROM history_user h
LEFT JOIN cur_user c ON h.user_login = c.user_login;
"""
return db.select(sql)[0]
