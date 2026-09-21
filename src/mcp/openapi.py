import sys
from pathlib import Path

import httpx

from mcp.server.fastmcp import FastMCP

# Adiciona a raiz do projeto ao PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

mcp = FastMCP("FromDotNetToPython-OpenAPI")

FASTAPI_OPENAPI_URL = "http://127.0.0.1:8000/openapi.json"
FASTAPI_BASE_URL = "http://127.0.0.1:8000"


def load_tools_from_openapi():
    """Lê o OpenAPI do FastAPI e registra cada endpoint como uma Tool MCP."""
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(FASTAPI_OPENAPI_URL)
            if response.status_code != 200:
                print(f"[Aviso] Não foi possível obter o OpenAPI de {FASTAPI_OPENAPI_URL}")
                return
            openapi_spec = response.json()
    except Exception as e:
        print(f"[Aviso] FastAPI não parece estar rodando em {FASTAPI_BASE_URL}. Inicie o uvicorn primeiro! Erro: {e}")
        return

    paths = openapi_spec.get("paths", {})

    for path_url, methods in paths.items():
        for method, operation in methods.items():
            method_upper = method.upper()
            summary = operation.get("summary") or operation.get("description") or f"Executa {method_upper} em {path_url}"
            operation_id = operation.get("operation_id", f"{method}_{path_url.replace('/', '_')}")

            tool_name = operation_id.replace("-", "_").lower()

            def create_tool_handler(url_path: str, http_method: str):
                async def execute_api_call(**kwargs) -> str:
                    async with httpx.AsyncClient(base_url=FASTAPI_BASE_URL) as async_client:
                        # Substitui os parâmetros de path (ex: {user_id}) caso existam
                        formatted_path = url_path
                        query_params = {}
                        json_body = None

                        for key, value in kwargs.items():
                            if f"{{{key}}}" in formatted_path:
                                formatted_path = formatted_path.replace(f"{{{key}}}", str(value))
                            elif http_method in ["POST", "PUT", "PATCH"]:
                                if json_body is None:
                                    json_body = {}
                                json_body[key] = value
                            else:
                                query_params[key] = value

                        res = await async_client.request(
                            method=http_method,
                            url=formatted_path,
                            params=query_params if query_params else None,
                            json=json_body if json_body else None,
                        )
                        return f"Status: {res.status_code}\nResponse: {res.text}"

                return execute_api_call

            handler = create_tool_handler(path_url, method_upper)
            handler.__name__ = tool_name
            handler.__doc__ = f"{summary}\nHTTP Method: {method_upper} | Path: {path_url}"

            mcp.add_tool(handler)


load_tools_from_openapi()

if __name__ == "__main__":
    mcp.run()