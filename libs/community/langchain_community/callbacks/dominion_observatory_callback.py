"""Dominion Observatory callback handler for LangChain.

Reads live behavioral trust scores from the Dominion Observatory (4,500+ MCP
servers tracked) before each tool call, optionally blocks low-trust tools, and
reports anonymized telemetry back to improve the network's baselines.

Install: ``pip install dominion-observatory``
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Optional
from uuid import UUID

try:
    from dominion_observatory import check_trust, report, OBSERVATORY_MCP_URL
    from dominion_observatory.langchain import (
        LowTrustToolBlocked,
        ObservatoryTrustCallbackHandler as _Base,
    )
except ImportError as e:
    raise ImportError(
        "Could not import dominion-observatory. "
        "Install with: pip install dominion-observatory"
    ) from e


class ObservatoryTrustCallbackHandler(_Base):
    """Callback handler that gates MCP tool calls on live behavioral trust scores.

    Before each tool call: reads the server's live trust score from the Dominion
    Observatory. Optionally blocks tools below a threshold.
    After each tool call: reports anonymized telemetry (no prompts/args/outputs).

    Args:
        tool_server_urls: Mapping of tool name → MCP server URL.
        min_trust_score: Block threshold (0–100). Default: None (no check).
        block_on_low_trust: Raise LowTrustToolBlocked if score below threshold.
        trust_cache_ttl_s: Cache trust scores for N seconds (default 60).
        report_timeout_s: Telemetry HTTP timeout (default 2s).
        trust_timeout_s: Trust read HTTP timeout (default 2s).

    Example:
        .. code-block:: python

            from langchain_community.callbacks import ObservatoryTrustCallbackHandler

            handler = ObservatoryTrustCallbackHandler(
                tool_server_urls={
                    "web_search": "https://search.example.com/mcp",
                    "transfer_funds": "https://payments.example.com/mcp",
                },
                min_trust_score=40.0,
                block_on_low_trust=True,
            )
            agent = AgentExecutor(..., callbacks=[handler])
    """


__all__ = ["ObservatoryTrustCallbackHandler", "LowTrustToolBlocked"]
