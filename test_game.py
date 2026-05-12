import subprocess

def main(project_path):

    subprocess.Popen(f"start cmd.exe /k python -m engine.tests.test_main \"{project_path}\"", shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == '__main__':
    main()