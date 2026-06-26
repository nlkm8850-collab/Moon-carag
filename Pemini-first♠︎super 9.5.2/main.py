"""
Pemini Girl 9.5.2 - Main Launcher
==================================
"""

import sys
import argparse
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth_system import AuthenticationManager, UserRole
from version_switcher import VersionManager, PeminiVersion
from code_engine import CodeIntelligenceEngine
from language_router import LanguageRouter
from cli_interface import PeminiGirlCLI

class PeminiGirlLauncher:
    VERSION = "9.5.2"
    CODENAME = "Lumina"

    def __init__(self):
        self.auth = AuthenticationManager()
        self.version_manager = VersionManager()
        self.code_engine = CodeIntelligenceEngine()
        self.language_router = LanguageRouter()
        self.cli = PeminiGirlCLI()
        self.current_user = None

    def print_header(self):
        print("""
    +---------------------------------------------------------------+
    |                                                               |
    |           Pemini Girl 9.5.2 - Lumina                          |
    |                                                               |
    |         Trilingual AI Code Assistant                          |
    |         AR | ZH | EN                                          |
    |                                                               |
    +---------------------------------------------------------------+
        """)

    def print_menu(self):
        print("\nMain Menu:")
        print("   1. Login")
        print("   2. Register")
        print("   3. Interactive Mode")
        print("   4. Web Interface")
        print("   5. Switch Version")
        print("   6. System Info")
        print("   7. Help")
        print("   0. Exit")

    def login_flow(self):
        print("\nLogin:")
        username = input("   Username/Email: ")
        password = input("   Password: ")
        result = self.auth.login(username, password)
        if result["success"]:
            self.current_user = result["user"]
            print(f"\nWelcome {result['user'].display_name}!")
            return True
        else:
            print(f"\nError: {result['message']}")
            return False

    def register_flow(self):
        print("\nRegister:")
        username = input("   Username: ")
        email = input("   Email: ")
        display_name = input("   Display Name (optional): ") or None
        password = input("   Password: ")
        result = self.auth.register_user(username, email, password, display_name)
        if result["success"]:
            print(f"\nSuccess: {result['message']}")
        else:
            print(f"\nError: {result['message']}")

    def switch_version_flow(self):
        print("\nAvailable Versions:")
        versions = self.version_manager.get_all_versions()
        for i, (ver, info) in enumerate(versions.items(), 1):
            status = "[ACTIVE]" if ver == self.version_manager.current_version else "       "
            print(f"   {status} {i}. {info.name} {info.version_number} ({info.codename})")
        choice = input("\nSelect version (1-2): ")
        if choice == "1":
            target = PeminiVersion.PRO_7_0
        elif choice == "2":
            target = PeminiVersion.GIRL_9_5_2
        else:
            print("Invalid choice")
            return
        result = self.version_manager.switch_version(target)
        status_icon = "OK" if result["success"] else "FAIL"
        print(f"\n[{status_icon}] {result['message']}")
        if result["success"] and "migration_notes" in result:
            print("\nMigration Notes:")
            for note in result["migration_notes"]:
                print(f"   {note}")

    def system_info(self):
        current = self.version_manager.get_current_version_info()
        print("\nSystem Info:")
        print(f"   Version: {current.name} {current.version_number} ({current.codename})")
        print(f"   Languages: {', '.join(current.supported_languages)}")
        print(f"   Code Languages: {len(current.supported_code_languages)}")
        print(f"   Max Context: {current.max_context_length} tokens")
        print(f"   Voice: {current.supports_voice}")
        print(f"   Web: {current.supports_web_interface}")
        print(f"   Mobile: {current.supports_mobile}")
        print(f"   Collaboration: {current.supports_collaboration}")
        print(f"   Users: {len(self.auth.users)}")
        print(f"   Active Sessions: {len(self.auth.sessions)}")

    def run_web(self):
        print("\nStarting Web Server...")
        print("   Open browser: http://localhost:8080")
        print("   Press Ctrl+C to stop")
        try:
            import uvicorn
            uvicorn.run("web_app:app", host="0.0.0.0", port=8080, reload=True)
        except ImportError:
            print("Please install uvicorn: pip install uvicorn")

    def run_interactive(self):
        self.cli.interactive_mode()

    def run(self):
        self.print_header()
        while True:
            self.print_menu()
            choice = input("\nSelect option: ").strip()
            if choice == "1":
                self.login_flow()
            elif choice == "2":
                self.register_flow()
            elif choice == "3":
                self.run_interactive()
            elif choice == "4":
                self.run_web()
            elif choice == "5":
                self.switch_version_flow()
            elif choice == "6":
                self.system_info()
            elif choice == "7":
                self.print_help()
            elif choice == "0":
                print("\nGoodbye! See you soon!")
                break
            else:
                print("Invalid option")

    def print_help(self):
        print("\nHelp:")
        print("   Pemini Girl 9.5.2 is a trilingual AI code assistant")
        print("   Supports Arabic, Chinese, and English")
        print("   Supports 25+ programming languages")
        print("   You can switch between Pro 7.0 and Girl 9.5.2")
        print("\n   For more info: https://github.com/nlkm8850-collab/Moon-carag")

def main():
    parser = argparse.ArgumentParser(description="Pemini Girl 9.5.2")
    parser.add_argument("--web", action="store_true", help="Run web interface")
    parser.add_argument("--cli", action="store_true", help="Run CLI mode")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--setup", action="store_true", help="Setup system")
    args = parser.parse_args()
    launcher = PeminiGirlLauncher()
    if args.version:
        print(f"Pemini Girl {launcher.VERSION} - {launcher.CODENAME}")
    elif args.web:
        launcher.run_web()
    elif args.cli:
        launcher.run_interactive()
    elif args.setup:
        print("Setup complete!")
    else:
        launcher.run()

if __name__ == "__main__":
    main()
