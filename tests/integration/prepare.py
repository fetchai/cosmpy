import os
import tempfile

import docker

TAG = "fetchai/fetchd:0.8.4"
ENTRYPOINT_FILENAME = "entry.sh"
ENTRYPOINT_LINES = (
    "#!/usr/bin/env bash",
    "# Add keys",
    'echo "erase weekend bid boss knee vintage goat syrup use tumble device album fortune water sweet maple kind degree toss owner crane half useless sleep" |fetchd keys add validator --recover',
    'echo "account snack twist chef razor sing gain birth check identify unable vendor model utility fragile stadium turtle sun sail enemy violin either keep fiction" | fetchd keys add bob --recover',
    "# Configure node",
    "fetchd init --chain-id=testing testing",
    "fetchd add-genesis-account $(fetchd keys show validator -a) 100000000000000000000000stake",
    "fetchd gentx validator 10000000000000000000000stake --chain-id testing",
    "fetchd collect-gentxs",
    "# Enable rest-api",
    "sed -i '/^\[api\]$/,/^\[/ s/^enable = false/enable = true/' ~/.fetchd/config/app.toml",
    "# Start FetchD local node",
    "fetchd start",
)
MOUNT_PATH = "/mnt"
CONTAINER_NAME = "fetchd_test"


def _make_entrypoint(dirpath):
    path = os.path.join(dirpath, ENTRYPOINT_FILENAME)
    with open(path, "w") as f:
        f.writelines(line + "\n" for line in ENTRYPOINT_LINES)
    os.chmod(path, 300)  # nosec


def run():
    container = None
    with tempfile.TemporaryDirectory() as tmpdir:
        _make_entrypoint(tmpdir)
        volumes = {tmpdir: {"bind": MOUNT_PATH, "mode": "rw"}}
        entrypoint = os.path.join(MOUNT_PATH, ENTRYPOINT_FILENAME)
        container = client.containers.run(
            TAG,
            detach=True,
            # network="host",
            volumes=volumes,
            entrypoint=str(entrypoint),
            name=CONTAINER_NAME,
        )
    return container


if __name__ == "__main__":
    client = docker.from_env()
    client.images.pull(TAG)
    run()
