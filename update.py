from subprocess import run
from textwrap import dedent

import httpx

URL = "https://api.github.com/repos/prettier/prettier/releases/latest"
HOOKFILE = ".pre-commit-hooks.yaml"


def main():
    resp = httpx.get(URL).raise_for_status()
    version = resp.json()["tag_name"]

    hook = f"""\
    - id: prettier
      name: prettier
      description: ""
      entry: prettier --write --ignore-unknown
      language: node
      types: [text]
      args: []
      require_serial: false
      additional_dependencies: ["prettier@{version}"]
      minimum_pre_commit_version: "0"
      """
    hook = dedent(hook)

    with open(HOOKFILE) as f:
        cur_hook = f.read()

    if hook == cur_hook:
        return

    with open(HOOKFILE, "w") as f:
        f.write(hook)

    run(["git", "add", HOOKFILE], check=True)
    run(["git", "commit", "-m", f"Update to version {version}"], check=True)
    run(["git", "tag", f"v{version}"], check=True)
    run(["git", "push", "origin"], check=True)
    run(["git", "push", "origin", "--tags"], check=True)


if __name__ == "__main__":
    main()
