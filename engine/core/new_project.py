import os
from tkinter import Tk, filedialog, simpledialog
from engine.systems.commands import get_command
from pathlib import Path
from run import VERSION
import state


class Project:
    def run(self):
        while True:
            print("Choose: New/Load\n")
            action_choice = get_command()
            action_choice = action_choice.strip().upper()

            match action_choice:
                case 'L' | 'LOAD':
                    Project.load()
                    return

                case 'N' | 'NEW':
                    Project.new()
                    return

                case _:
                    print("Wrong choice.")

    @staticmethod
    def load():
        root = Tk()
        root.withdraw()
        path = filedialog.askdirectory(title="Choose diection.")

        if path:
            p = Path(path)
            project_file = p / f"{p.name}.project"

            if project_file.is_file():
                state.state.path = path
                return
            else:
                print("Wrong project.")
        else:
            print("Wrong project.")

    def new():
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

                            file_path = Path(f"{new_folder_path}/{new_folder_name}.project")

                            with open(file_path, 'w') as f:
                                f.write(f"VERSION: {VERSION}")

                            data_folder = os.path.join(new_folder_path, 'data')
                            os.makedirs(data_folder, exist_ok=True)

                            enemies_folder = os.path.join(data_folder, 'enemies')
                            os.makedirs(enemies_folder, exist_ok=True)

                            entities_folder = os.path.join(data_folder, 'entities')
                            os.makedirs(entities_folder, exist_ok=True)

                            events_folder = os.path.join(data_folder, 'events')
                            os.makedirs(events_folder, exist_ok=True)

                            map_folder = os.path.join(data_folder, 'map')
                            os.makedirs(map_folder, exist_ok=True)

                            players_folder = os.path.join(data_folder, 'players')
                            os.makedirs(players_folder, exist_ok=True)

                            print("Created:", new_folder_path)

                            return
                case 'N' | 'NO':
                    return
                case _:
                    print("Wrong choice.")


def main():
    project = Project()
    project.run()

if __name__ == '__main__':
    main()