{
  "properties" : { },
  "id" : "670e1f90a55c48a59a004ae7c9e481bb",
  "script" : null,
  "groupId" : "39c33765c93e4af089275fbe9ae18d07",
  "name" : "服务汇总分页",
  "createTime" : null,
  "updateTime" : 1758620150654,
  "lock" : null,
  "createBy" : null,
  "updateBy" : "admin",
  "path" : "/source/total/page",
  "method" : "POST",
  "parameters" : [ ],
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
  "requestBody" : "{\r\n    \"startDate\":1730390400000,\r\n    \"endDate\":1742400000000,\r\n    \"source\":\"email\",\r\n    \"community\":\"opengauss\",\r\n    \"pageNum\":2,\r\n    \"pageSize\": 10,\r\n    \"desc\": \"subscribe_count\"\r\n}",
  "headers" : [ ],
  "paths" : [ ],
  "responseBody" : "{\n    \"code\": 1,\n    \"message\": \"success\",\n    \"data\": {\n        \"total_count\": 66,\n        \"total_page\": 7,\n        \"list\": [{\n            \"list_id\": \"docs.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 20,\n            \"email_subject_count\": 11\n        }, {\n            \"list_id\": \"embdded.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 0,\n            \"email_subject_count\": 0\n        }, {\n            \"list_id\": \"embedded.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 0,\n            \"email_subject_count\": 0\n        }, {\n            \"list_id\": \"gis.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 11,\n            \"email_subject_count\": 8\n        }, {\n            \"list_id\": \"graph.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 11,\n            \"email_subject_count\": 8\n        }, {\n            \"list_id\": \"infra.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 15,\n            \"email_subject_count\": 12\n        }, {\n            \"list_id\": \"inplaceupdate.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 11,\n            \"email_subject_count\": 8\n        }, {\n            \"list_id\": \"iot.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 11,\n            \"email_subject_count\": 8\n        }, {\n            \"list_id\": \"knowledgegraph.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 10,\n            \"email_subject_count\": 7\n        }, {\n            \"list_id\": \"ai.opengauss.org\",\n            \"subscribe_count\": 0,\n            \"email_count\": 15,\n            \"email_subject_count\": 11\n        }]\n    },\n    \"timestamp\": 1754033911551,\n    \"executeTime\": 74\n}",
  "description" : null,
  "requestBodyDefinition" : null,
  "responseBodyDefinition" : null
}
================================
import '@/util/timestamp2Date' as timestamp2Date;
Date start = timestamp2Date(body.startDate);
Date end = timestamp2Date(body.endDate);
