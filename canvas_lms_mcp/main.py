from mcp.server.fastmcp import FastMCP

from canvas_lms_mcp.client import CanvasClient
from canvas_lms_mcp.usecases import TOOLS_DEFINITION


class CanvasLMSMCP:
    def __init__(
        self,
        mcp_port: int,
        api_token: str,
        base_url: str = "https://canvas.instructure.com",
    ):
        self.mcp_port = mcp_port
        self.canvas_client = CanvasClient(api_token, base_url)
        self._setup_server()

    def _setup_server(self):
        self._connect_to_canvas()
        self.mcp = FastMCP(
            name="canvas-lms-mcp", port=self.mcp_port, debug=True
        )  # TODO: remove debug
        self.__setup_tools()

    def _connect_to_canvas(self):
        pass

    def __setup_tools(self):
        for tool_schema in TOOLS_DEFINITION:
            self.mcp.tool()(tool_schema)

    def run(self):
        print("Running MCP server on port", self.mcp_port)  # TODO: use logger
        self.mcp.run(transport="sse")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5173)
    parser.add_argument("--api-token", type=str, required=True)
    parser.add_argument(
        "--base-url", type=str, default="https://canvas.instructure.com"
    )
    args = parser.parse_args()

    CanvasLMSMCP(
        mcp_port=args.port, api_token=args.api_token, base_url=args.base_url
    ).run()


if __name__ == "__main__":
    main()
