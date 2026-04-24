import os
from tkinter import Tk, filedialog, simpledialog
from engine.systems.commands import get_command
from engine.core.navigation import MainMenu

class Project:
    def run(self):
        while True:
            print("Choose: New/Load\n")
            action_choice = get_command()
            action_choice = action_choice.strip().upper()

            match action_choice:
                case 'L' | 'LOAD':
                    root = Tk()
                    root.withdraw()
                    path = filedialog.askdirectory(title="Choose diection.")

                    if path:
                        MainMenu.path = path

                case 'N' | 'NEW':
                    while True:
                        print("Choice: Yes/No")
                        print("Do you want to create new project?")

                        choice = get_command()
                        choice = choice.strip().upper()
                        match choice:
                            case 'Y' | 'YES':
                                root = Tk()
                                root.withdraw()
                                path = filedialog.askdirectory(title="Choose direction.")

                                if path:
                                    new_folder_name = simpledialog.askstring("New folder", "Enter name for folder:")

                                    if new_folder_name:
                                        new_folder_path = os.path.join(path, new_folder_name)
                                        os.makedirs(new_folder_path, exist_ok=True)
                                        print("Created:", new_folder_path)

                                    break
                            case 'N' | 'NO':
                                break
                            case _:
                                print("Wrong choice.")
                case _:
                    print("Wrong choice.")


def main():
    project = Project()
    project.run()

if __name__ == '__main__':
    main()