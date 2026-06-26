import json
import os
from typing import List, Optional

from lib.template_loader import ParamDef, ToolTemplate

_SEPARATOR = "================================"
_APIDOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "api-docs")


def load_apidocs_templates() -> List[ToolTemplate]:
    templates = []

    if not os.path.isdir(_APIDOCS_DIR):
        print(f"No api docs in path: {_APIDOCS_DIR}")
        return templates

    _walk_dir(_APIDOCS_DIR, {}, templates)
    return templates


def _walk_dir(dir_path: str, parent_group_info: dict, templates: list):
    group_info = _merge_group_info(parent_group_info, _load_group_info(dir_path))

    for filename in sorted(os.listdir(dir_path)):
        full_path = os.path.join(dir_path, filename)
        if filename.endswith(".ms") and os.path.isfile(full_path):
            template = _parse_ms_file(full_path, group_info)
            if template:
                templates.append(template)

    for entry in sorted(os.listdir(dir_path)):
        sub_path = os.path.join(dir_path, entry)
        if os.path.isdir(sub_path):
            _walk_dir(sub_path, group_info, templates)


def _merge_group_info(parent: dict, child: dict) -> dict:
    if not child:
        return parent
    merged = dict(child)
    child_path = (merged.get("path") or "").strip("/")
    parent_path = (parent.get("path") or "").rstrip("/")
    merged["path"] = parent_path + "/" + child_path if child_path else parent_path
    parent_name = parent.get("name", "")
    child_name = child.get("name", "")
    if parent_name and child_name:
        merged["name"] = parent_name + " > " + child_name
    elif parent_name:
        merged["name"] = parent_name
    return merged


def _load_group_info(group_dir: str) -> dict:
    group_json = os.path.join(group_dir, "group.json")
    if not os.path.exists(group_json):
        return {}
    with open(group_json, encoding="utf-8") as f:
        data = json.load(f)
        return data


def _parse_ms_file(path: str, group_info: dict) -> Optional[ToolTemplate]:
    with open(path, encoding="utf-8") as f:
        content = f.read()

    json_part = content.split(_SEPARATOR)[0].strip()
    try:
        data = json.loads(json_part)
    except json.JSONDecodeError:
        return None

    ms_path = data.get("path", "")
    if not ms_path:
        return None

    group_prefix = group_info.get("path", "").rstrip("/")
    full_path = group_prefix + "/" + ms_path.lstrip("/")
    http_method = data.get("method", "POST").lower()
    name = data.get("name", ms_path)
    description = data.get("description") or name
    if group_info.get("name"):
        description = group_info.get("name") + ": " + description

    tool_name = _path_to_tool_name(http_method, full_path)
    params = []

    # 处理路径参数（paths 字段）
    path_params_list = data.get("paths") or []
    path_param_names = []
    for path_param in path_params_list:
        param_def = _infer_single_param(path_param, "path")
        params.append(param_def)
        path_param_names.append(param_def.name)

    # 处理 query 和 body 参数
    params.extend(_infer_params(data.get("parameters"), "query"))

    request_body = data.get("requestBodyDefinition") or {}
    params.extend(_infer_params(request_body.get("children") or [], "body"))

    response_body = data.get("responseBodyDefinition") or {}
    response_config = _detect_response_config(response_body.get("children") or [])

    return ToolTemplate(
        name=tool_name,
        description=description,
        http_method=http_method,
        http_path=full_path,
        use_extract_data=True,
        path_params=path_param_names,
        constant_params={},
        params=params,
        empty_data_message="暂无数据",
        response_config=response_config,
    )


def _path_to_tool_name(http_method: str, path: str) -> str:
    parts = [p for p in path.strip("/").split("/") if p]

    # 将路径参数占位符 {xxx} 替换为 "pathName"
    cleaned_parts = []
    for part in parts:
        if part.startswith("{") and part.endswith("}"):
            # 提取花括号内的参数名
            param_name = part[1:-1]  # 去掉首尾花括号
            cleaned_parts.append(param_name)
        else:
            cleaned_parts.append(part)

    return f"{http_method}_{'_'.join(cleaned_parts)}"


_TYPE_MAP = {
    "long": "int",
    "integer": "int",
    "int": "int",
    "double": "int",
    "float": "int",
    "number": "int",
    "string": "str",
    "integer": "int",
    "array": "list",
    "object": "dict",
}


def _infer_params(params_list: list, param_type: str) -> List[ParamDef]:
    params = []
    if not params_list:
        return params
    for item in params_list:
        param_def = _infer_single_param(item, param_type)
        params.append(param_def)
    return params


def _infer_single_param(item: dict, param_type: str) -> ParamDef:
    data_type = _TYPE_MAP.get((item.get("dataType") or "").lower(), "str")
    
    # 处理默认值
    default = item.get("defaultValue")
    if data_type == "list" and default is None:
        default = []

    return ParamDef(
        name=item.get("name"),
        type=data_type,
        default=default,
        required=item.get("required") or False,
        description=item.get("description") or "",
        body_key=item.get("name"),
        in_=param_type,
        conditional=True,
        is_community=item.get("name") == "community",
    )


def _detect_response_config(response_body: list) -> dict:
    return {"type": "formatter"}
