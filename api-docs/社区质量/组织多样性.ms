{
  "properties" : { },
  "id" : "ce28848368494e49ade20b4ef6c8cae4",
  "script" : null,
  "groupId" : "2e2220ca1c424052ba4fa20a1e7370f8",
  "name" : "组织多样性",
  "createTime" : null,
  "updateTime" : 1773129488909,
  "lock" : null,
  "createBy" : null,
  "updateBy" : "admin",
  "path" : "/company",
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
    "value" : "1745689600000",
    "description" : "查询范围结束时间",
    "required" : false,
    "dataType" : "Long",
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
  } ],
  "options" : [ ],
  "requestBody" : "",
  "headers" : [ ],
  "paths" : [ ],
  "responseBody" : "{\n    \"code\": 1,\n    \"message\": \"success\",\n    \"data\": [{\n        \"month_date\": \"2025-01-01\",\n        \"count\": 49\n    }, {\n        \"month_date\": \"2025-02-01\",\n        \"count\": 49\n    }, {\n        \"month_date\": \"2025-03-01\",\n        \"count\": 48\n    }, {\n        \"month_date\": \"2025-04-01\",\n        \"count\": 46\n    }],\n    \"timestamp\": 1773129036978,\n    \"executeTime\": null\n}",
  "description" : "查询指定社区的日/月/年度的贡献组织/企业/公司多样性，适合：趋势分析、历史对比、汇总某年/某月数据。",
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
          "name" : "count",
          "value" : "49",
          "description" : "",
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
      "value" : "1773127708010",
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
SELECT date_trunc('${interval}', date)::date as month_date, count(distinct company)
FROM dws_${community}_contribute_company_daily 
WHERE company <> 'robot' AND company <> '个人贡献者'
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