"""
Main entry point for the Personal AI Assistant.
Run this file to start the interactive assistant.
"""

import sys
from core.assistant import PersonalAssistant
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def print_welcome():
    """Print welcome message."""
    print("\n" + "=" * 60)
    print(f"Welcome to {settings.ASSISTANT_NAME}!")
    print("=" * 60)
    print("Type 'help' for commands or 'exit' to quit.\n")


def print_help():
    """Print help information."""
    print("\nAvailable Commands:")
    print("  exit, quit      - Exit the assistant")
    print("  help            - Show this help message")
    print("  clear           - Clear conversation memory")
    print("  info            - Show assistant information")
    print("  summary         - Show conversation summary")
    print("  tools           - List available tools")
    print("  context         - Show current context")
    print("\nJust type your message to chat with the assistant.\n")


def handle_command(command: str, assistant: PersonalAssistant) -> bool:
    """
    Handle special commands.

    Args:
        command: User command
        assistant: Assistant instance

    Returns:
        False if should exit, True otherwise
    """
    command = command.strip().lower()

    if command in ['exit', 'quit']:
        print("\nGoodbye!")
        return False

    elif command == 'help':
        print_help()

    elif command == 'clear':
        assistant.clear_memory()
        print("✓ Conversation memory cleared.")

    elif command == 'info':
        info = assistant.get_info()
        print("\nAssistant Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()

    elif command == 'summary':
        print("\n" + assistant.get_conversation_summary())
        print()

    elif command == 'tools':
        tools = assistant.list_tools()
        if tools:
            print("\nAvailable Tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
            print()
        else:
            print("No tools available.\n")

    elif command == 'context':
        context = assistant.get_context()
        if context:
            print("\nCurrent Context:")
            for key, value in context.items():
                print(f"  {key}: {value}")
            print()
        else:
            print("No context set.\n")

    elif command == '':
        pass  # Empty input

    else:
        return None  # Not a command, treat as chat

    return True


def interactive_chat():
    """Run the interactive chat interface."""
    try:
        # Validate settings
        settings.validate()
        logger.info("Settings validated")

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        print(f"\n❌ Configuration Error: {str(e)}")
        print("Please check your .env file and try again.")
        sys.exit(1)

    try:
        # Initialize assistant
        assistant = PersonalAssistant()
        
        # Validate provider
        if not assistant.validate_provider():
            print("\n❌ Failed to connect to LLM provider.")
            print("Please check your API key and try again.")
            sys.exit(1)

        print_welcome()

        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                # Handle commands
                if user_input.startswith('/'):
                    command_result = handle_command(user_input[1:], assistant)
                    if command_result is False:
                        break
                    if command_result is True:
                        continue

                # Regular chat
                if user_input:
                    print("\nAssistant: ", end="", flush=True)
                    response = assistant.chat(user_input)
                    print(response)
                    print()

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break

            except Exception as e:
                logger.error(f"Error in chat loop: {str(e)}")
                print(f"\n❌ Error: {str(e)}")
                print("Please try again.\n")

    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        print(f"\n❌ Fatal Error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Personal AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start interactive chat
  python main.py --test-connection # Test LLM connection
  python main.py --info             # Show assistant info
        """,
    )

    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test connection to LLM provider",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show assistant information",
    )

    args = parser.parse_args()

    if args.test_connection:
        try:
            settings.validate()
            assistant = PersonalAssistant()
            if assistant.validate_provider():
                print("✓ Connection successful!")
                sys.exit(0)
            else:
                print("✗ Connection failed!")
                sys.exit(1)
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            sys.exit(1)

    elif args.info:
        try:
            settings.validate()
            assistant = PersonalAssistant()
            info = assistant.get_info()
            print("\nAssistant Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            sys.exit(0)
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            sys.exit(1)

    else:
        interactive_chat()


if __name__ == "__main__":
    main()
