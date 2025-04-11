import typer

class Color:
    
    @staticmethod
    def green(text, bold=False):
        return typer.style(text, fg=typer.colors.BRIGHT_GREEN, bold=bold)

    @staticmethod
    def cyan(text, bold=False):
        return typer.style(text, fg=typer.colors.BRIGHT_CYAN, bold=bold)

    @staticmethod
    def blue(text, bold=False):
        return typer.style(text, fg=typer.colors.BLUE, bold=bold)

    @staticmethod
    def red(text, bold=False):
        return typer.style(text, fg=typer.colors.RED, bold=bold)