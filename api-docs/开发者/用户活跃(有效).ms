{
  "properties" : { },
  "id" : "copy1743582663599d84445",
  "script" : null,
  "groupId" : "905e0bee16764ec9be1e96b78cae9466",
  "name" : "用户活跃(有效)",
  "createTime" : null,
  "updateTime" : 1773818370052,
  "lock" : null,
  "createBy" : null,
  "updateBy" : "admin",
  "path" : "/active/user",
  "method" : "POST",
  "parameters" : [ ],
  "options" : [ ],
  "requestBody" : "{\r\n    \"start\":1730419200000,\r\n    \"end\":1747211237554,\r\n    \"orgList\":[],\r\n    \"source\":\"\",\r\n    \"internalList\":[\"外部\"],\r\n    \"private\":\"\",\r\n    \"community\":\"openubmc\",\r\n    \"levelList\":[\"D0\"],\r\n    \"eventList\":[\"\"],\r\n    \"interval\":\"daily\"\r\n}",
  "headers" : [ ],
  "paths" : [ ],
  "responseBody" : "{\n    \"code\": 1,\n    \"message\": \"success\",\n    \"data\": [{\n        \"level_type\": \"D0\",\n        \"date\": \"2024-11-01\",\n        \"increase\": 0\n    }, {\n        \"level_type\": \"D0\",\n        \"date\": \"2024-11-02\",\n        \"increase\": 0\n    }, {\n        \"level_type\": \"D0\",\n        \"date\": \"2025-05-12\",\n        \"increase\": 2\n    }, {\n        \"level_type\": \"D0\",\n        \"date\": \"2025-05-13\",\n        \"increase\": 1\n    }, {\n        \"level_type\": \"D0\",\n        \"date\": \"2025-05-14\",\n        \"increase\": 1\n    }],\n    \"timestamp\": 1747281186456,\n    \"executeTime\": 6\n}",
  "description" : "获取活跃开发者数量，支持用户级别（D0/D1/D2），周期（天/周/月）维度",
  "requestBodyDefinition" : {
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
      "name" : "start",
      "value" : "1730419200000",
      "description" : "开始时间",
      "required" : true,
      "dataType" : "Long",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "pass",
      "error" : null,
      "expression" : "",
      "children" : [ ]
    }, {
      "name" : "end",
      "value" : "1747211237554",
      "description" : "结束时间",
      "required" : true,
      "dataType" : "Long",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "pass",
      "error" : null,
      "expression" : "",
      "children" : [ ]
    }, {
      "name" : "orgList",
      "value" : "",
      "description" : "组织",
      "required" : false,
      "dataType" : "Array",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ ]
    }, {
      "name" : "source",
      "value" : "",
      "description" : "来源平台",
      "required" : false,
      "dataType" : "String",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "pattern",
      "error" : null,
      "expression" : "^[a-zA-Z]*$",
      "children" : [ ]
    }, {
      "name" : "internalList",
      "value" : "",
      "description" : "内外部",
      "required" : false,
      "dataType" : "Array",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ {
        "name" : "",
        "value" : "外部",
        "description" : "",
        "required" : false,
        "dataType" : "String",
        "type" : null,
        "defaultValue" : null,
        "validateType" : "pattern",
        "error" : null,
        "expression" : "^(内部|外部)$",
        "children" : [ ]
      } ]
    }, {
      "name" : "private",
      "value" : "",
      "description" : "公私仓",
      "required" : false,
      "dataType" : "String",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "pattern",
      "error" : null,
      "expression" : "^(true|false)?$",
      "children" : [ ]
    }, {
      "name" : "community",
      "value" : "openubmc",
      "description" : "社区",
      "required" : true,
      "dataType" : "String",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "pattern",
      "error" : null,
      "expression" : "^[a-zA-Z]{1,32}$",
      "children" : [ ]
    }, {
      "name" : "levelList",
      "value" : "",
      "description" : "用户级别",
      "required" : true,
      "dataType" : "Array",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "",
      "error" : "",
      "expression" : "",
      "children" : [ {
        "name" : "",
        "value" : "D0",
        "description" : "",
        "required" : false,
        "dataType" : "String",
        "type" : null,
        "defaultValue" : null,
        "validateType" : "pattern",
        "error" : null,
        "expression" : "^(D0|D1|D2)$",
        "children" : [ ]
      } ]
    }, {
      "name" : "eventList",
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
        "dataType" : "String",
        "type" : null,
        "defaultValue" : null,
        "validateType" : "pattern",
        "error" : null,
        "expression" : "^(pr|issue|comment)?$",
        "children" : [ ]
      } ]
    }, {
      "name" : "interval",
      "value" : "daily",
      "description" : "时间周期",
      "required" : true,
      "dataType" : "String",
      "type" : null,
      "defaultValue" : null,
      "validateType" : "pattern",
      "error" : null,
      "expression" : "^(daily|week|month)$",
      "children" : [ ]
    } ]
  },
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
          "name" : "level_type",
          "value" : "D0",
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
          "name" : "date",
          "value" : "2024-11-01",
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
          "name" : "increase",
          "value" : "0",
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
      "value" : "1747281171576",
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
      "value" : "9",
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
import '@/util/timestamp2Date' as timestamp2Date;
Date start = timestamp2Date(body.start);
Date end = timestamp2Date(body.end);
// 服务平台
var source = body.source;
// 组织
var orgList = body.orgList; 
// 内外部
var internalList = body.internalList;
// 是否私仓
var private = body.private;
// 用户类比: D0,D1,D2
var levelList = body.levelList;
var level = levelList[0];
// 用户贡献类型: pr,issue,comment
var eventList = body.eventList;
var event = eventList[0];
// 统计周期：daily-天，week-周，month-月
var interval = body.interval;
if(interval == 'daily'){
    interval = 'day'
}
var community = body.community.toLowerCase();
var activeTable = 'dwm_' + community+ '_contribute_active_user_' + interval;
// 社区表
var contributeTable = "dws_"+body.community+"_contribute";
var sql = """
WITH periods AS (
    SELECT 
        start_date,
        end_date,
        #{interval} as period_type,
        CASE 
            WHEN #{interval} = 'week' THEN date_trunc('week', start_date)::DATE 
            WHEN #{interval} = 'month' THEN date_trunc('month', start_date)::DATE
            ELSE date_trunc('day', start_date)::DATE 
        END AS first_period_start,
        CASE 
            WHEN #{interval} = 'week' THEN date_trunc('week', end_date)::DATE
            WHEN #{interval} = 'month' THEN date_trunc('month', end_date)::DATE
            ELSE date_trunc('day', end_date)::DATE 
        END AS last_period_start
    FROM (VALUES (#{start}, #{end})) AS input(start_date, end_date)
),date_series AS (
  SELECT
    generate_series ( (SELECT start_date FROM periods), (SELECT end_date FROM periods), '1 day' :: INTERVAL ) :: DATE AS date
),
group_series AS (
    SELECT
    <if test="interval == 'day'">
        date_trunc('day', date)::DATE as date
    </if>
    <elseif test="interval == 'week'">
        DISTINCT date_trunc('week', date)::DATE as date
    </elseif>
    <else>
       DISTINCT date_trunc('month', date)::DATE as date
    </else>
    from date_series  
),
full_periods AS (
   select 
        date,
        <if test="level == 'D0'">
            sum(d0_count) as increase
        </if>
        <if test="level == 'D1' and event == null">
            sum(d1_count) as increase
        </if>
        <if test="level == 'D1' and event == 'pr'">
            sum(d1_pr_count) as increase
        </if>
        <if test="level == 'D1' and event == 'issue'">
            sum(d1_issue_count) as increase
        </if>
        <if test="level == 'D1' and event == 'comment'">
            sum(d1_comment_count) as increase
        </if>
        <if test="level == 'D2'">
            sum(d2_count) as increase
        </if>
    from ${activeTable}, periods
    <where> 
        date BETWEEN periods.first_period_start AND periods.last_period_start      
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
    group by date
),
combined_data AS (
    SELECT   
        *
    FROM full_periods
),
joined_data AS (
    SELECT 
        gs.date,
        COALESCE(d.increase, 0) AS increase
    FROM group_series gs
    LEFT JOIN combined_data d ON gs.date = d.date
)
SELECT
    <if test="level == 'D0'">
        'D0' as level_type,
    </if>
    <if test="level == 'D1' and event == null">
        'D1' as level_type,
    </if>
    <if test="level == 'D1' and event == 'pr'">
        'D1' as level_type,
        'pr' as event_type,
    </if>
    <if test="level == 'D1' and event == 'issue'">
        'D1' as level_type,
        'issue' as event_type,
    </if>
    <if test="level == 'D1' and event == 'comment'">
        'D1' as level_type,
        'comment' as event_type,
    </if>
    <if test="level == 'D2'">
        'D2' as level_type,
        'pr' as event_type,
    </if>
    date, increase
FROM joined_data
ORDER BY date;
""";
return db.select(sql)