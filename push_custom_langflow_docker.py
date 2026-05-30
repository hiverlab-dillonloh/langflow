import subprocess
import sys
from pathlib import Path
import os

ACR_NAME = "hiverlab"
IMAGE = "langflow:hiverlab"
DOCKERFILE = "docker/build_and_push_with_extras.Dockerfile"
BUILD_CONTEXT = "."
SCRIPT_DIR = Path(__file__).resolve().parent

def main():
    remote_image = f"{ACR_NAME}.azurecr.io/{IMAGE}"
    env = os.environ.copy()
    env["DOCKER_BUILDKIT"] = "1"

    subprocess.run(["az", "acr", "login", "--name", ACR_NAME], check=True)

    print(f"Building {remote_image} locally with BuildKit...")
    subprocess.run(
        [
            "docker",
            "build",
            "--progress=plain",
            "--file",
            DOCKERFILE,
            "--tag",
            remote_image,
            BUILD_CONTEXT,
        ],
        check=True,
        cwd=SCRIPT_DIR,
        env=env,
    )

    print(f"Pushing {remote_image}...")
    subprocess.run(["docker", "push", remote_image], check=True)

    print("Done.")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with exit code {exc.returncode}.")
        sys.exit(exc.returncode)
