class TerminalUI:
    def __init__(self, width: int):
        self.width = width

    def display_text(self, text: str):
        print(text)

    def get_choice(self, prompt: str, options: list):
        print(prompt)
        for i, option in enumerate(options):
            print(f"{i}: {option}")
        choice = int(input("Wähle eine Option: "))
        return choice

    def clear_screen(self):
        # Logik zum Löschen des Bildschirms
        print("\033[H\033[J")  # ANSI Escape Codes zum Löschen des Bildschirms

    def display_title(self, title: str):
        # Logik zur Anzeige des Titels
        print(f"\n{'=' * self.width}\n{title.center(self.width)}\n{'=' * self.width}\n") 