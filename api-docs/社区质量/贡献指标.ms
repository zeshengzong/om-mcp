{
  "properties" : { },
  "id" : "dff537f2baaa4c6eab941cd0c19239bf",
  "script" : null,
  "groupId" : "2e2220ca1c424052ba4fa20a1e7370f8",
  "name" : "贡献指标",
  "createTime" : null,
  "updateTime" : 1773129470884,
  "lock" : null,
  "createBy" : null,
  "updateBy" : "admin",
  "path" : "/contribute",
  "method" : "GET",
  "parameters" : [ {
    "name" : "community",
    "value" : "openeuler",
    "description" : "社区名称",
    "required" : true,
    "dataType" : "String",
    "type" : null,
    "defaultValue" : null,
    "validateType" : null,
    "error" : null,
    "expression" : null,
    "children" : null
  }, {
    "name" : "interval",
    "value" : "month",
    "description" : "时间维度，如日、月、年",
    "required" : true,
    "dataType" : "String",
    "type" : null,
    "defaultValue" : null,
    "validateType" : "pattern",
    "error" : null,
    "expression" : "^(day|month|year)$",
    "children" : null
  }, {
    "name" : "start",
    "value" : "1735689600000",
    "description" : "查询范围开始时间",
    "required" : false,
    "dataType" : "Long",
    "type" : null,
    "defaultValue" : null,
    "validateType" : null,
    "error" : null,
    "expression" : null,
    "children" : null
  }, {
    "name" : "end",
    "value" : "1747205600000",
    "description" : "查询范围结束时间",
    "required" : false,
    "dataType" : "Long",
    "type" : null,
    "defaultValue" : null,
    "validateType" : null,
    "error" : null,
    "expression" : null,
    "children" : null
  } ],
  "options" : [ ],
  "requestBody" : "",
  "headers" : [ ],
  "paths" : [ ],
  "responseBody" : "{\n    \"code\": 1,\n    \"message\": \"success\",\n    \"data\": [{\n        \"month_date\": \"2025-01-01\",\n        \"activate_user\": 868,\n        \"prissues\": 5068,\n        \"prs\": 3276,\n        \"merged_prs\": 2516,\n        \"issues\": 2552,\n        \"merged_pr_user\": 340\n    }, {\n        \"month_date\": \"2025-02-01\",\n        \"activate_user\": 923,\n        \"prissues\": 5952,\n        \"prs\": 3984,\n        \"merged_prs\": 3460,\n        \"issues\": 2492,\n        \"merged_pr_user\": 411\n    }, {\n        \"month_date\": \"2025-03-01\",\n        \"activate_user\": 989,\n        \"prissues\": 5364,\n        \"prs\": 5112,\n        \"merged_prs\": 3790,\n        \"issues\": 1574,\n        \"merged_pr_user\": 446\n    }, {\n        \"month_date\": \"2025-04-01\",\n        \"activate_user\": 1020,\n        \"prissues\": 4852,\n        \"prs\": 4150,\n        \"merged_prs\": 3124,\n        \"issues\": 1728,\n        \"merged_pr_user\": 443\n    }, {\n        \"month_date\": \"2025-05-01\",\n        \"activate_user\": 539,\n        \"prissues\": 1819,\n        \"prs\": 1451,\n        \"merged_prs\": 987,\n        \"issues\": 832,\n        \"merged_pr_user\": 211\n    }],\n    \"timestamp\": 1773129191575,\n    \"executeTime\": null\n}",
  "description" : "查询指定社区的日/月/年度的贡献数据，包含提交的 PR 数、合并的 PR 数、提交的 Issue 数、活跃用户数、合并 PR 用户（也叫留存用户）数。\n返回从建社至今的完整月度数据列表，不支持时间范围过滤。\n适合：趋势分析、历史对比、汇总某年/某月数据。\n注意：不同周期用户有重复，不能将日期维度的用户数直接相加。",
  "requestBodyDefinition" : null,
  "responseBodyDefinition" : {
    "name" : "",
    "value" : "",
    "description" : "",
    "required" : false,
    "dataType" : "Object",
    "type" : null,
    "defaultValue" : null,
    "validateType" : "",
    "error" : "",
    "expression" : "",
    "children" : [ {
      "name" : "code",
      "value" : "1",
      "description" : "",
      "required" : false,
      "dataType" : "Integer",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ ]
    }, {
      "name" : "message",
      "value" : "success",
      "description" : "",
      "required" : false,
      "dataType" : "String",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ ]
    }, {
      "name" : "data",
      "value" : "",
      "description" : "",
      "required" : false,
      "dataType" : "Array",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ {
        "name" : "",
        "value" : "",
        "description" : "",
        "required" : false,
        "dataType" : "Object",
        "type" : null,
        "defaultValue" : null,
        "validateType" : "",
        "error" : "",
        "expression" : "",
        "children" : [ {
          "name" : "month_date",
          "value" : "2025-01-01",
          "description" : "",
          "required" : false,
          "dataType" : "String",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "activate_user",
          "value" : "868",
          "description" : "当期活跃开发者人数",
          "required" : false,
          "dataType" : "Integer",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "prissues",
          "value" : "5068",
          "description" : "提交的pr和issue总数",
          "required" : false,
          "dataType" : "Integer",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "prs",
          "value" : "3276",
          "description" : "提交的pr总数",
          "required" : false,
          "dataType" : "Integer",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "merged_prs",
          "value" : "2516",
          "description" : "合并的pr总数",
          "required" : false,
          "dataType" : "Integer",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "issues",
          "value" : "2552",
          "description" : "提交的issue总数",
          "required" : false,
          "dataType" : "Integer",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "merged_pr_user",
          "value" : "340",
          "description" : "当期合并的pr用户",
          "required" : false,
          "dataType" : "Integer",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        } ]
      } ]
    }, {
      "name" : "timestamp",
      "value" : "1773126470356",
      "description" : "",
      "required" : false,
      "dataType" : "Long",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ ]
    }, {
      "name" : "executeTime",
      "value" : "null",
      "description" : "",
      "required" : false,
      "dataType" : "Object",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ ]
    } ]
  }
}
================================
community = community.toLowerCase()
var sql = """
SELECT date_trunc('${interval}', date)::date as month_date, 
       count(distinct user_login) as activate_user, 
       sum(merged_pr_incre + issue_incre) as prissues, 
       sum(pr_incre) as prs,
       sum(merged_pr_incre) as merged_prs, 
       sum(issue_incre) as issues, 
       count(distinct user_login) filter (where merged_pr_incre > 0) as merged_pr_user
FROM dws_${community}_contribute_repo_user_daily
WHERE 1 = 1
    <if test="start != null and start != ''">
        AND date >= (to_timestamp(#{start}/1000) AT TIME ZONE 'Asia/Shanghai')::date
    </if>
    <if test="end != null and end != ''">
        AND date <= (to_timestamp(#{end}/1000) AT TIME ZONE 'Asia/Shanghai')::date
    </if>
GROUP BY date_trunc('${interval}', date)
ORDER BY date_trunc('${interval}', date) asc;
"""

var resp = db.select(sql)
return resp