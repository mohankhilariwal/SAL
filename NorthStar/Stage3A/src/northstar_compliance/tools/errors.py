class ToolGatewayError(Exception):
    """Base error for Stage 3A gateway failures."""


class TransientToolError(ToolGatewayError):
    """Adapter error that can be retried when the descriptor permits it."""


class PermanentToolError(ToolGatewayError):
    """Adapter error that must not be retried."""
