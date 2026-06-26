import os
import yaml
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional


@dataclass
class ParamDef:
    name: str
    type: str           # 'str' | 'int' | 'list'
    default: Any
    required: bool
    description: str
    body_key: str       # API 字段名（默认同 name）
    in_: str            # 'body' | 'query' | 'path'
    conditional: bool   # true: 非空才加入请求体
    is_community: bool  # true: 是否是社区参数


@dataclass
class ToolTemplate:
    name: str
    description: str
    http_method: str            # 'post' | 'get'
    http_path: str
    use_extract_data: bool
    path_params: List[str]
    constant_params: Dict[str, Any]
    params: List[ParamDef]
    empty_data_message: str
    response_config: Dict[str, Any]


def load_all_templates() -> List[ToolTemplate]:
    templates_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "tools", "templates"
    )
    templates = []
    for filename in sorted(os.listdir(templates_dir)):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            path = os.path.join(templates_dir, filename)
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            templates.append(_parse_template(data, filename))
    return templates


def _parse_template(data: dict, filename: str) -> ToolTemplate:
    try:
        tool = data["tool"]
        http = data["http"]
    except KeyError as e:
        raise ValueError(f"Template {filename} missing required top-level key: {e}")

    params_data = data.get("params") or []
    params = []
    for p in params_data:
        name = p.get("name")
        if not name:
            raise ValueError(f"Template {filename}: param missing 'name'")
        param_type = p.get("type", "str")
        if param_type not in ("str", "int", "list"):
            raise ValueError(f"Template {filename}: param '{name}' has unsupported type '{param_type}'")

        # default: str→"", int→0, list→[] if not explicitly set
        if "default" in p:
            default = p["default"]
        else:
            if param_type == "str":
                default = ""
            elif param_type == "int":
                default = 0
            else:  # list
                default = []

        params.append(ParamDef(
            name=name,
            type=param_type,
            default=default,
            required=p.get("required", False),
            description=p.get("description", ""),
            body_key=p.get("body_key", name),
            in_=p.get("in", "body"),
            conditional=p.get("conditional", False),
            is_community=name == "community",
        ))

    http_method = http.get("method", "post").lower()
    if http_method not in ("get", "post"):
        raise ValueError(f"Template {filename}: http.method must be 'get' or 'post'")

    return ToolTemplate(
        name=tool["name"],
        description=str(tool.get("description", "")).strip(),
        http_method=http_method,
        http_path=http["path"],
        use_extract_data=http.get("use_extract_data", False),
        path_params=http.get("path_params") or [],
        constant_params=http.get("constant_params") or {},
        params=params,
        empty_data_message=data.get("empty_data_message", "暂无数据"),
        response_config=data.get("response") or {},
    )
