import os
import json
import questionary

SETTINGS_PATH = os.path.expanduser(
    os.getenv("THENKIRI_SETTINGS_PATH", "./config/settings.json")
)

DEFAULT_SETTINGS = {
    "no_certificate_check": False
}


def ensure_settings_dir():
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)


def load_settings():
    ensure_settings_dir()

    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    ensure_settings_dir()
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def show_status(settings):
    current = settings.get("no_certificate_check", False)

    print("\nSSL Certificate Verification")
    print("--------------------------------")
    print("Purpose: Controls HTTPS security verification.")
    print("ENABLED  → SSL certificates are verified (safe)")
    print("DISABLED → SSL errors are ignored (unsafe)")
    print("--------------------------------")
    print(f"Current state: {'DISABLED ' if current else 'ENABLED'}\n")


def toggle_certificate_setting():
    settings = load_settings()
    current = settings.get("no_certificate_check", False)

    print("\nSSL Certificate Verification")
    print("--------------------------------")
    print("Enabled: SSL certificates are verified")
    print("Disabled: SSL errors are ignored")
    print("--------------------------------")

    if current:
        new_value = questionary.confirm(
            "SSL is currently DISABLED. Do you want to ENABLE it?",
            default=True
        ).ask()
        final_value = not new_value
    else:
        new_value = questionary.confirm(
            "SSL is currently ENABLED. Do you want to DISABLE it?",
            default=False
        ).ask()
        final_value = new_value

    if new_value is None:
        return

    settings["no_certificate_check"] = final_value
    save_settings(settings)

    print(
        f"\Status: SSL verification is "
        f"{'DISABLED' if final_value else 'ENABLED'}\n"
    )

def settings_cli():
    while True:
        load_settings()

        choice = questionary.select(
            "Settings Menu:",
            choices=[
                "SSL Certificate Verification",
                "Back"
            ]
        ).ask()

        if choice == "SSL Certificate Verification":
            toggle_certificate_setting()

        elif choice == "Back" or not choice:
            break

if __name__ == "__main__":
    settings_cli()