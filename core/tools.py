"""
Tool management and built-in tools for the AI Assistant.
Allows registration and execution of custom tools.
"""

from typing import Callable, Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Tool:
    """Represents a callable tool for the assistant."""

    name: str
    description: str
    func: Callable
    parameters: Dict[str, Any]
    category: str = "general"

    def __call__(self, *args, **kwargs) -> Any:
        """Execute the tool."""
        try:
            result = self.func(*args, **kwargs)
            logger.debug(f"Tool '{self.name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool '{self.name}' failed: {str(e)}")
            raise


class ToolRegistry:
    """Registry for managing assistant tools."""

    def __init__(self):
        """Initialize tool registry."""
        self.tools: Dict[str, Tool] = {}
        self._register_builtin_tools()
        logger.debug("ToolRegistry initialized")

    def register_tool(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Optional[Dict[str, Any]] = None,
        category: str = "general",
    ) -> Tool:
        """
        Register a new tool.

        Args:
            name: Tool name (must be unique)
            description: Tool description
            func: Callable function
            parameters: Tool parameters
            category: Tool category

        Returns:
            Registered Tool object
        """
        if name in self.tools:
            logger.warning(f"Tool '{name}' already registered. Overwriting.")

        tool = Tool(
            name=name,
            description=description,
            func=func,
            parameters=parameters or {},
            category=category,
        )
        self.tools[name] = tool
        logger.info(f"Tool '{name}' registered")
        return tool

    def get_tool(self, name: str) -> Optional[Tool]:
        """
        Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool object or None if not found
        """
        return self.tools.get(name)

    def execute_tool(self, name: str, **kwargs) -> Any:
        """
        Execute a tool by name.

        Args:
            name: Tool name
            **kwargs: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")

        logger.debug(f"Executing tool '{name}' with args: {kwargs}")
        return tool(**kwargs)

    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all registered tools.

        Args:
            category: Optional category filter

        Returns:
            List of tool information dictionaries
        """
        tools = []
        for tool in self.tools.values():
            if category and tool.category != category:
                continue
            tools.append({
                'name': tool.name,
                'description': tool.description,
                'category': tool.category,
                'parameters': tool.parameters,
            })
        return tools

    def _register_builtin_tools(self) -> None:
        """Register built-in tools."""
        # Time tool
        self.register_tool(
            name="get_time",
            description="Get current date and time",
            func=self._tool_get_time,
            category="utility",
        )

        # Math tool
        self.register_tool(
            name="calculator",
            description="Perform mathematical calculations",
            func=self._tool_calculator,
            parameters={"operation": "add|subtract|multiply|divide|power"},
            category="utility",
        )

        # String tool
        self.register_tool(
            name="string_tools",
            description="Perform string operations",
            func=self._tool_string_operations,
            parameters={"operation": "uppercase|lowercase|reverse|length"},
            category="utility",
        )

        logger.info("Built-in tools registered")

    @staticmethod
    def _tool_get_time() -> str:
        """Get current time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _tool_calculator(operation: str, a: float, b: float) -> float:
        """Perform calculations."""
        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else None,
            'power': lambda x, y: x ** y,
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")
        
        result = operations[operation](a, b)
        if result is None:
            raise ValueError("Division by zero")
        
        return result

    @staticmethod
    def _tool_string_operations(operation: str, text: str) -> str:
        """Perform string operations."""
        operations = {
            'uppercase': lambda s: s.upper(),
            'lowercase': lambda s: s.lower(),
            'reverse': lambda s: s[::-1],
            'length': lambda s: str(len(s)),
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")
        
        return operations[operation](text)

    def __repr__(self) -> str:
        """String representation."""
        return f"ToolRegistry(tools={len(self.tools)})"


# Global tool registry instance
_tool_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get or create the global tool registry."""
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry


def register_tool(
    name: str,
    description: str,
    func: Callable,
    parameters: Optional[Dict[str, Any]] = None,
    category: str = "general",
) -> Tool:
    """
    Convenience function to register a tool globally.

    Args:
        name: Tool name
        description: Tool description
        func: Callable function
        parameters: Tool parameters
        category: Tool category

    Returns:
        Registered Tool object
    """
    registry = get_tool_registry()
    return registry.register_tool(name, description, func, parameters, category)
