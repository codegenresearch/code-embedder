import click
from colorama import Fore, Style, Back
import json
import os

METADATA_FILE = "drd.json"


class DIContainer:
    def __init__(self):
        self.providers = {}

    def add_provider(self, name, provider):
        self.providers[name] = provider

    def get_provider(self, name):
        return self.providers.get(name)


di_container = DIContainer()


def print_error(message, indent=0):
    click.echo(f"{' ' * indent}{Fore.RED}✘ {message}{Style.RESET_ALL}")


def print_success(message, indent=0):
    click.echo(f"{' ' * indent}{Fore.GREEN}✔ {message}{Style.RESET_ALL}")


def print_info(message, indent=0):
    click.echo(f"{' ' * indent}{Fore.YELLOW}ℹ {message}{Style.RESET_ALL}")


def print_warning(message, indent=0):
    click.echo(f"{' ' * indent}{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_debug(message, indent=0):
    click.echo(click.style(f"{' ' * indent}DEBUG: {message}", fg="cyan"))


def print_step(step_number, total_steps, message, indent=0):
    click.echo(
        f"{' ' * indent}{Fore.CYAN}[{step_number}/{total_steps}] {message}{Style.RESET_ALL}"
    )


def create_confirmation_box(message, action):
    terminal_width = os.get_terminal_size().columns
    box_width = min(len(message) + 4, terminal_width - 4)
    box_top = f"╔{'═' * box_width}╗"
    box_bottom = f"╚{'═' * box_width}╝"
    box_content = f"║  {message.center(box_width - 2)}  ║"

    confirmation_box = f"""
{Fore.YELLOW}{box_top}
║  {Back.RED}{Fore.WHITE}CONFIRMATION REQUIRED{Style.RESET_ALL}{Fore.YELLOW}  ║
{box_content}
╠{'═' * box_width}╣
║  Do you want to {action}?  ║
{box_bottom}{Style.RESET_ALL}
"""
    return confirmation_box


def print_header(header, style="bold", indent=0):
    if style == "bold":
        click.echo(
            f"{' ' * indent}{Fore.YELLOW}{Style.BRIGHT}{header}{Style.RESET_ALL}"
        )
    else:
        click.echo(f"{' ' * indent}{Fore.YELLOW}{header}{Style.RESET_ALL}")


def print_command_details(commands):
    print_header("Command Details")
    for index, cmd in enumerate(commands, start=1):
        cmd_type = cmd.get("type", "Unknown")
        print_info(f"Command {index} - Type: {cmd_type}", indent=2)

        if cmd_type == "shell":
            print_info(f"  Command: {cmd.get('command', 'N/A')}", indent=2)

        elif cmd_type == "explanation":
            print_info(f"  Explanation: {cmd.get('content', 'N/A')}", indent=2)

        elif cmd_type == "file":
            operation = cmd.get("operation", "N/A")
            filename = cmd.get("filename", "N/A")
            content_preview = cmd.get("content", "N/A")
            if len(content_preview) > 50:
                content_preview = content_preview[:50] + "..."
            print_info(f"  Operation: {operation}", indent=2)
            print_info(f"  Filename: {filename}", indent=2)
            print_info(f"  Content: {content_preview}", indent=2)

        elif cmd_type == "metadata":
            operation = cmd.get("operation", "N/A")
            print_info(f"  Operation: {operation}", indent=2)
            if operation == "UPDATE_DEV_SERVER":
                print_info(
                    f"  Start Command: {cmd.get('start_command', 'N/A')}", indent=2
                )
                print_info(f"  Framework: {cmd.get('framework', 'N/A')}", indent=2)
                print_info(f"  Language: {cmd.get('language', 'N/A')}", indent=2)
            elif operation in ["UPDATE_FILE", "UPDATE"]:
                print_info(f"  Filename: {cmd.get('filename', 'N/A')}", indent=2)
                print_info(f"  Language: {cmd.get('language', 'N/A')}", indent=2)
                print_info(f"  Description: {cmd.get('description', 'N/A')}", indent=2)

        else:
            print_warning(f"  Unknown command type: {cmd_type}", indent=2)

