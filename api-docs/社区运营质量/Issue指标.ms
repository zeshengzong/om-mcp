{
  "properties" : { },
  "id" : "copy1773747165020d55157",
  "script" : null,
  "groupId" : "2e2220ca1c424052ba4fa20a1e7370f8",
  "name" : "Issue指标",
  "createTime" : null,
  "updateTime" : 1773747654481,
  "lock" : null,
  "createBy" : null,
  "updateBy" : "admin",
  "path" : "/issue",
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
    "value" : "1767196800000",
    "description" : "查询范围开始时间，格式为毫秒时间戳",
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
    "value" : "1769875200000",
    "description" : "查询范围结束时间，格式为毫秒时间戳",
    "required" : false,
    "dataType" : "Long",
    "type" : null,
    "defaultValue" : null,
    "validateType" : null,
    "error" : null,
    "expression" : null,
    "children" : null
  } ],
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
  "responseBody" : "{\n    \"code\": 1,\n    \"message\": \"success\",\n    \"data\": [{\n        \"count\": 2158,\n        \"avg_first_reply_time\": 27.72,\n        \"avg_closed_time\": 4.72,\n        \"median_first_reply_time\": 12.79,\n        \"median_closed_time\": 46.64\n    }],\n    \"timestamp\": 1773747573722,\n    \"executeTime\": 173\n}",
  "description" : "统计社区Issue汇总指标（平均首次响应时间、平均闭环时间、首次响应时间中位数、闭环时间中位数）",
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
      "description" : "响应码",
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
      "description" : "响应消息",
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
      "description" : "响应数据",
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
          "name" : "count",
          "value" : "2600",
          "description" : "Issue帖子总数",
          "required" : false,
          "dataType" : "Integer",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "avg_first_reply_time",
          "value" : "21.29",
          "description" : "首次响应时间平均值",
          "required" : false,
          "dataType" : "Double",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "avg_closed_time",
          "value" : "21.29",
          "description" : "关闭时间平均值",
          "required" : false,
          "dataType" : "Double",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "median_first_reply_time",
          "value" : "29.21",
          "description" : "首次响应时间中位数",
          "required" : false,
          "dataType" : "Double",
          "type" : null,
          "defaultValue" : null,
          "validateType" : "",
          "error" : "",
          "expression" : "",
          "children" : [ ]
        }, {
          "name" : "median_closed_time",
          "value" : "588.67",
          "description" : "关闭时间中位数",
          "required" : false,
          "dataType" : "Double",
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
      "value" : "1773367432276",
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
      "value" : "7",
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
  }
}
================================
community = community.toLowerCase()
if (community == 'cann'){
    community == 'cannopen'
}
var sql = """
SELECT
        count(*) as count, 
        ROUND((AVG(COALESCE(first_reply_time, 0)) / 86400.0)::NUMERIC, 2) AS avg_first_reply_time,
        ROUND((AVG(COALESCE(closed_time, 0)) / 86400.0)::NUMERIC, 2) AS avg_closed_time,
        ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY COALESCE(first_reply_time, 0)) / 86400.0)::NUMERIC, 2) AS median_first_reply_time,
        ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY COALESCE(closed_time, open_time, 0)) / 86400.0)::NUMERIC, 2) AS median_closed_time
FROM dws_${community}_contribute
<where>
    contrib_type = 'issue' and is_hide is null and is_removed is null
    <if test="start != null and start != ''">
        AND created_at >= (to_timestamp(#{start}/1000) AT TIME ZONE 'Asia/Shanghai')::date
    </if>
    <if test="end != null and end != ''">
        AND created_at <= (to_timestamp(#{end}/1000) AT TIME ZONE 'Asia/Shanghai')::date
    </if>
    <if test="namespace != null and namespace != ''">
        and namespace LIKE CONCAT('%', #{namespace}, '%')
    </if>
    <if test="repo_path != null and repo_path != ''">
        and repo_path LIKE CONCAT('%', #{repo_path}, '%')
    </if>
    <if test="source != null and source != ''">
        and source = #{source}
    </if>
    <if test="private != null and private != ''">
        and private = #{private}
    </if>
    <if test="internalList != null and internalList.size() > 0">
        and internal in
        <foreach collection="internalList" item="item" open="(" separator="," close=")">
            #{item}
        </foreach>
    </if>
</where>     
"""
var resp = db.select(sql)
return resp