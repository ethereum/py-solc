from __future__ import absolute_import

import functools
import json
import re

from .exceptions import (
    SolcError,
    ContractsNotFound,
)

from .utils.formatting import (
    add_0x_prefix,
)
from .utils.filesystem import (
    is_executable_available,
)
from .wrapper import (
    SOLC_BINARY,
    solc_wrapper,
)


version_regex = re.compile('Version: ([0-9]+\.[0-9]+\.[0-9]+(-[a-f0-9]+)?)')


is_solc_available = functools.partial(is_executable_available, SOLC_BINARY)


def get_solc_version(**kwargs):
    kwargs['version'] = True
    stdoutdata, stderrdata = solc_wrapper(**kwargs)
    version_match = version_regex.search(stdoutdata)
    if version_match is None:
        raise SolcError(
            "Unable to extract version string from command output: `{0}`".format(
                stdoutdata,
            )
        )
    return version_match.groups()[0]


def _parse_compiler_output(stdoutdata, compiler_version):

    output = json.loads(stdoutdata)

    if "contracts" not in output:
        # {'sources': {}, 'version': 'xxx'}
        # solc did not pick up any contracts
        raise ContractsNotFound(output)

    contracts = output['contracts']

    for _, data in contracts.items():
        data['abi'] = json.loads(data['abi'])

    sorted_contracts = sorted(contracts.items(), key=lambda c: c[0])

    return {
        contract_name: {
            'abi': contract_data['abi'],
            'code': add_0x_prefix(contract_data['bin']),
            'code_runtime': add_0x_prefix(contract_data['bin-runtime']),
            'source': None,
            'meta': {
                'compilerVersion': compiler_version,
                'language': 'Solidity',
                'languageVersion': '0',
            },
        }
        for contract_name, contract_data
        in sorted_contracts
    }


ALL_OUTPUT_VALUES = [
    "abi",
    "asm",
    "ast",
    "bin",
    "bin-runtime",
    "clone-bin",
    "devdoc",
    "interface",
    "opcodes",
    "userdoc",
]


def compile_source(source, output_values=ALL_OUTPUT_VALUES, **kwargs):
    if 'stdin_bytes' in kwargs:
        raise ValueError(
            "The `stdin_bytes` keyword is not allowed in the `compile_source` function"
        )
    if 'combined_json' in kwargs:
        raise ValueError(
            "The `combined_json` keyword is not allowed in the `compile_source` function"
        )

    combined_json = ','.join(output_values)

    stdoutdata, stderrdata = solc_wrapper(
        stdin_bytes=source,
        combined_json=combined_json,
        **kwargs
    )

    compiler_version = get_solc_version(version=True, **kwargs)

    contracts = _parse_compiler_output(stdoutdata, compiler_version)
    return contracts


def compile_files(source_files, output_values=ALL_OUTPUT_VALUES, **kwargs):
    if 'source_files' in kwargs:
        raise ValueError(
            "The `source_files` keyword is not allowed in the `compile_files` function"
        )
    if 'combined_json' in kwargs:
        raise ValueError(
            "The `combined_json` keyword is not allowed in the `compile_files` function"
        )

    combined_json = ','.join(output_values)

    stdoutdata, stderrdata = solc_wrapper(
        source_files=source_files,
        combined_json=combined_json,
        **kwargs
    )

    compiler_version = get_solc_version(version=True, **kwargs)

    contracts = _parse_compiler_output(stdoutdata, compiler_version)
    return contracts


def link_code(unliked_data, libraries):
    libraries_arg = ','.join((
        ':'.join((lib_name, lib_address))
        for lib_name, lib_address in libraries.items()
    ))
    stdoutdata, stderrdata = solc_wrapper(
        stdin_bytes=unliked_data,
        link=True,
        libraries=libraries_arg,
    )

    return stdoutdata.strip()
