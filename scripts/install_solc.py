"""
Compile solidity.

  - if [ -n "$SOLC_VERSION" ]; then export SOLC_BINARY="$TRAVIS_BUILD_DIR/solc-versions/solc-$SOLC_VERSION/solc"; fi
  - if [ -n "$SOLC_VERSION" ]; then export LD_LIBRARY_PATH="$TRAVIS_BUILD_DIR/solc-versions/solc-$SOLC_VERSION"; fi
  - if [ -n "$SOLC_VERSION" ]; then sudo apt-get install -y tree unzip; fi

mkdir -p solc-versions/solc-$SOLC_VERSION
cd solc-versions/solc-$SOLC_VERSION
git clone --recurse-submodules --branch v$SOLC_VERSION --depth 50 https://github.com/ethereum/solidity.git
./solidity/scripts/install_deps.sh
"""
import os
import stat
import subprocess
import sys

import zipfile


SUPPORTED_VERSIONS = {
    "0.4.1",
    "0.4.2",
    "0.4.6",
    "0.4.7",
    "0.4.8",
    "0.4.11",
}


BASE_INSTALL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'bin',
)


INSTALL_PATH_TEMPLATE = os.path.join(
    BASE_INSTALL_PATH,
    "solc-{0}",
)


def is_executable_available(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath = os.path.dirname(program)
    if fpath:
        if is_exe(program):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return True

    return False


def ensure_path_exists(dir_path):
    """
    Make sure that a path exists
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        return True
    return False


def ensure_parent_dir_exists(path):
    ensure_path_exists(os.path.dirname(path))


def check_subprocess_call(command, message=None, stderr=subprocess.STDOUT, **proc_kwargs):
    if message:
        print(message)
    print("Executing: {0}".format(" ".join(command)))

    return subprocess.check_call(
        command,
        stderr=subprocess.STDOUT,
        **proc_kwargs
    )


def check_subprocess_output(command, message=None, stderr=subprocess.STDOUT, **proc_kwargs):
    if message:
        print(message)
    print("Executing: {0}".format(" ".join(command)))

    return subprocess.check_output(
        command,
        stderr=subprocess.STDOUT,
        **proc_kwargs
    )


is_git_available = is_executable_available('git')


SOLIDITY_GIT_URI = "https://github.com/ethereum/solidity.git"


def get_source_path(identifier):
    return os.path.join(
        INSTALL_PATH_TEMPLATE.format(identifier),
        'source',
    )


def clone_solidity_repository(identifier):
    destination = get_source_path(identifier)
    ensure_parent_dir_exists(destination)
    command = [
        "git", "clone",
        "--recurse-submodules",
        "--branch", identifier,
        "--depth", "10",
        SOLIDITY_GIT_URI,
        destination,
    ]

    return check_subprocess_call(
        command,
        message="Checking out solidity repository @ {0}".format(identifier),
    )


def install_dependencies(identifier):
    source_path = get_source_path(identifier)
    install_deps_script_path = os.path.join(source_path, 'scripts', 'install_deps.sh')

    return check_subprocess_call(
        command=["sh", install_deps_script_path],
        message="Running dependency installation script `install_deps.sh` @ {0}".format(
            install_deps_script_path,
        ),
    )


def get_release_zipfile_path(identifier):
    return os.path.join(
        INSTALL_PATH_TEMPLATE.format(identifier),
        'release.zip',
    )


def get_extract_path(identifier):
    return os.path.join(
        INSTALL_PATH_TEMPLATE.format(identifier),
        'bin',
    )


def get_executable_path(identifier):
    extract_path = get_extract_path(identifier)
    return os.path.join(
        extract_path,
        'solc',
    )


DOWNLOAD_UBUNTU_RELEASE_URI_TEMPLATE = "https://github.com/ethereum/solidity/releases/download/{0}/solidity-ubuntu-trusty.zip"


def download_ubuntu_release(identifier):
    download_uri = DOWNLOAD_UBUNTU_RELEASE_URI_TEMPLATE.format(identifier)
    release_zipfile_path = get_release_zipfile_path(identifier)

    ensure_parent_dir_exists(release_zipfile_path)

    command = [
        "wget", download_uri,
        '-c',  # resume previously incomplete download.
        '-O', release_zipfile_path,
    ]

    return check_subprocess_call(
        command,
        message="pulling down ubuntu release from {0}".format(download_uri),
    )


DOWNLOAD_STATIC_RELEASE_URI_TEMPLATE = "https://github.com/ethereum/solidity/releases/download/{0}/solc-static-linux"


def download_static_release(identifier):
    download_uri = DOWNLOAD_STATIC_RELEASE_URI_TEMPLATE

    # TODO:command
    assert False, "todo, construct command"

    return check_subprocess_call(
        command,
        message="pulling down ubuntu release from {0}".format(download_uri),
    )


def extract_release(identifier):
    release_zipfile_path = get_release_zipfile_path(identifier)

    extract_path = get_extract_path(identifier)
    ensure_path_exists(extract_path)

    print("Extracting zipfile: {0} -> {1}".format(release_zipfile_path, extract_path))

    with zipfile.ZipFile(release_zipfile_path) as zipfile_file:
        zipfile_file.extractall(extract_path)

    print("Making `solc` binary executable: `chmod +x {0}`".format(executable_path))

    executable_path = get_executable_path(identifier)
    current_st = os.stat(executable_path)
    os.chmod(executable_path, current_st.st_mode | stat.S_IEXEC)


def install_solc_dependencies(identifier):
    source_git_dir = os.path.join(
        get_source_path(identifier),
        '.git',
    )
    if not os.path.exists(source_git_dir):
        clone_solidity_repository(identifier)

    install_dependencies(identifier)


def install_solc_from_ubuntu_release_zip(identifier):
    download_ubuntu_release(identifier)
    extract_release(identifier)

    extract_path = get_extract_path(identifier)
    executable_path = get_executable_path(identifier)
    assert os.path.exists(executable_path), "Executable not found @".format(executable_path)

    check_version_command = [executable_path, '--version']

    version_output = check_subprocess_output(
        check_version_command,
        message="Checking installed executable version @ {0}".format(executable_path),
        env={'LD_LIBRARY_PATH': extract_path},
    )

    print("solc successfully installed at: {0}".format(executable_path))


def install_solc_from_static_linux(identifier):


V0_4_8 = 'v0.4.8'
V0_4_11 = 'v0.4.11'


SUPPORTED_VERSIONS = {
    V0_4_8,
    V0_4_11,
}


def install_v0_4_8():
    install_solc_dependencies(V0_4_8)
    install_solc_from_ubuntu_release_zip(V0_4_8)


def install_v0_4_11():
    install_solc_dependencies(V0_4_11)


INSTALL_FUNCTIONS = {
    V0_4_8:
    V0_4_11,
}


def install_solc(identifier):
    if identifier not in SUPPORTED_VERSIONS:
        raise ValueError(
            "Installation of solidity=={0} is not supported.  Must be one of {1}".format(
                identifier,
                ', '.join(sorted(SUPPORTED_VERSIONS)),
            )
        )
    install_fn = INSTALL_FUNCTIONS[identifier]
    install_fn()


if __name__ == "__main__":
    try:
        identifier = sys.argv[1]
    except IndexError:
        print("Invocation error.  Should be invoked as `./install_solc.py <version>`")
        sys.exit(1)

    install_solc(identifier)
