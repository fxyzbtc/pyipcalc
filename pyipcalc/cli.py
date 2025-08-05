"""Command-line interface for pyipcalc."""

import typer
from typing import Optional
from loguru import logger

from .calculator import IPCalculator
from .display import DisplayFormatter


app = typer.Typer(
    help="A utility to calculate IPv4 and IPv6 network information.",
    add_completion=False,
    no_args_is_help=True
)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    ip_address: Optional[str] = typer.Argument(
        None,
        help="IP address with network (e.g., 192.168.1.0/24, 192.168.1.0/255.255.255.0, 2001:db8::/32)"
    ),
    verbose: bool = typer.Option(
        False, 
        "--verbose", 
        "-v", 
        help="Enable verbose logging"
    ),
    quiet: bool = typer.Option(
        False, 
        "--quiet", 
        "-q", 
        help="Suppress all output except results"
    ),
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version information"
    )
) -> None:
    """Calculate network information for IPv4 or IPv6 addresses."""
    
    if version:
        from . import __version__
        typer.echo(f"pyipcalc version {__version__}")
        return
    
    if ip_address is None:
        typer.echo("Error: Missing argument 'IP_ADDRESS'")
        typer.echo("Try 'pyipcalc --help' for help.")
        raise typer.Exit(1)
    
    # Configure logging
    if quiet:
        logger.remove()
    elif verbose:
        logger.add(lambda msg: typer.echo(f"DEBUG: {msg}", err=True), level="DEBUG")
    
    try:
        # Calculate network information
        result = IPCalculator.calculate(ip_address)
        
        # Format and display output
        output = DisplayFormatter.format_output(result)
        typer.echo(output)
        
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            typer.echo(traceback.format_exc(), err=True)
        raise typer.Exit(1)

@app.command()
def version() -> None:
    """Show version information."""
    from . import __version__
    typer.echo(f"pyipcalc version {__version__}")


def main() -> None:
    """Entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()
