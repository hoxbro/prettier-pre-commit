# /// script
# dependencies = ["httpx"]
# ///

import re
from subprocess import run
from textwrap import dedent

import httpx

URL = "https://registry.npmjs.org/prettier/latest"
HOOKFILE = ".pre-commit-hooks.yaml"
READMEFILE = "README.md"


def main():
    resp = httpx.get(URL).raise_for_status()
    version = resp.json()["version"]

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

    with open(READMEFILE) as f:
        readme = f.read()

    readme = re.sub("rev: v.*", f"rev: v{version}", readme)

    with open(READMEFILE, "w") as f:
        f.write(readme)

    run(["git", "add", HOOKFILE, READMEFILE], check=True)
    run(["git", "commit", "-m", f"Update to version {version}"], check=True)
    run(["git", "tag", f"v{version}"], check=True)
    run(["git", "push", "origin"], check=True)
    run(["git", "push", "origin", "--tags"], check=True)


if __name__ == "__main__":
    main()
