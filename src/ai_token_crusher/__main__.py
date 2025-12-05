import sys

def main():
    if any(arg in sys.argv for arg in ["--terminal", "-t", "--help", "-h"]):
        from .interfaces.cli.main import run_cli
        run_cli()
    else:
        from .interfaces.gui.app import run_gui
        run_gui()

if __name__ == "__main__":
    main()
