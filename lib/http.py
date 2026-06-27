import httpx
import logging
import json
import os

API_BASE_URL = "https://datastat.osinfra.cn/server"

logger = logging.getLogger("om-mcp")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def _get_mcp_key() -> str:
    """从环境变量获取 MAGIC_API_TOKEN"""
    return os.getenv("MAGIC_API_TOKEN", "")


async def get(
    path: str, params: dict = None, base_url: str = API_BASE_URL, community: str = ""
) -> dict:
    url = f"{base_url}{path}"
    headers = {}
    mcp_key = _get_mcp_key()
    if mcp_key:
        headers["mcp-key"] = mcp_key
    logger.info("GET %s params=%s", url, params)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            result = resp.json()
            logger.info(
                "GET %s -> %s", url, json.dumps(result, ensure_ascii=False)[:500]
            )
            return result
    except httpx.HTTPStatusError as e:
        logger.error("GET %s -> HTTP %s", url, e.response.status_code)
        return {
            "code": -1,
            "message": f"HTTP {e.response.status_code}：接口暂不可用",
            "data": None,
        }
    except Exception as e:
        logger.error("GET %s -> %s", url, e)
        return {"code": -1, "message": str(e), "data": None}


async def post(
    path: str, body: dict = None, base_url: str = API_BASE_URL, community: str = ""
) -> dict:
    url = f"{base_url}{path}"
    payload = body or {}
    headers = {}
    mcp_key = _get_mcp_key()
    if mcp_key:
        headers["mcp-key"] = mcp_key
    logger.info("POST %s body=%s", url, json.dumps(payload, ensure_ascii=False))
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            result = resp.json()
            logger.info(
                "POST %s -> %s", url, json.dumps(result, ensure_ascii=False)[:500]
            )
            return result
    except httpx.HTTPStatusError as e:
        logger.error("POST %s -> HTTP %s", url, e.response.status_code)
        return {
            "code": -1,
            "message": f"HTTP {e.response.status_code}：接口暂不可用",
            "data": None,
        }
    except Exception as e:
        logger.error("POST %s -> %s", url, e)
        return {"code": -1, "message": str(e), "data": None}


def extract_data(result: dict):
    """统一提取 data 字段，兼容双层嵌套结构。"""
    data = result.get("data")
    if isinstance(data, dict) and "code" in data and "data" in data:
        return data.get("data")
    return data