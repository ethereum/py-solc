from __future__ import absolute_import

import functools
import json
import re

from .exceptions import (
    SolcError,
    ContractsNotFound,
)

from .utils.filesystem import (
    is_executable_available,
)
from .wrapper import (
    SOLC_BINARY,
    solc_wrapper,
)

import semantic_version


VERSION_DEV_DATE_MANGLER_RE = re.compile(r'(\d{4})\.0?(\d{1,2})\.0?(\d{1,2})')
strip_zeroes_from_month_and_day = functools.partial(VERSION_DEV_DATE_MANGLER_RE.sub,
                                                    r'\g<1>.\g<2>.\g<3>')
is_solc_available = functools.partial(is_executable_available, SOLC_BINARY)


def get_solc_version_string(**kwargs):
    kwargs['version'] = True
    stdoutdata, stderrdata, command, proc = solc_wrapper(**kwargs)
    _, _, version_string = stdoutdata.partition('\n')
    if not version_string or not version_string.startswith('Version: '):
        raise SolcError(
            command=command,
            return_code=proc.returncode,
            stdout_data=stdoutdata,
            stderr_data=stderrdata,
            message="Unable to extract version string from command output",
        )
    return version_string


def get_solc_version(**kwargs):
    # semantic_version as of 2017-5-5 expects only one + to be used in string
    return semantic_version.Version(
        strip_zeroes_from_month_and_day(
            get_solc_version_string(**kwargs)
            [len('Version: '):]
            .replace('++', 'pp')))


def _parse_compiler_output(stdoutdata):
    output = json.loads(stdoutdata)

    if "contracts" not in output:
        return {}

    contracts = output['contracts']

    for _, data in contracts.items():
        data['abi'] = json.loads(data['abi'])

    return contracts


ALL_OUTPUT_VALUES = (
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
)


def compile_source(source,
                   allow_empty=False,
                   output_values=ALL_OUTPUT_VALUES,
                   **kwargs):
    if 'stdin_bytes' in kwargs:
        raise ValueError(
            "The `stdin_bytes` keyword is not allowed in the `compile_source` function"
        )
    if 'combined_json' in kwargs:
        raise ValueError(
            "The `combined_json` keyword is not allowed in the `compile_source` function"
        )

    combined_json = ','.join(output_values)
    compiler_kwargs = dict(stdin_bytes=source, combined_json=combined_json, **kwargs)

    stdoutdata, stderrdata, command, proc = solc_wrapper(**compiler_kwargs)

    contracts = _parse_compiler_output(stdoutdata)

    if not contracts and not allow_empty:
        raise ContractsNotFound(
            command=command,
            return_code=proc.returncode,
            stdout_data=stdoutdata,
            stderr_data=stderrdata,
        )
    return contracts


def compile_files(source_files,
                  allow_empty=False,
                  output_values=ALL_OUTPUT_VALUES,
                  **kwargs):
    if 'combined_json' in kwargs:
        raise ValueError(
            "The `combined_json` keyword is not allowed in the `compile_files` function"
        )

    combined_json = ','.join(output_values)
    compiler_kwargs = dict(source_files=source_files, combined_json=combined_json, **kwargs)

    stdoutdata, stderrdata, command, proc = solc_wrapper(**compiler_kwargs)

    contracts = _parse_compiler_output(stdoutdata)

    if not contracts and not allow_empty:
        raise ContractsNotFound(
            command=command,
            return_code=proc.returncode,
            stdout_data=stdoutdata,
            stderr_data=stderrdata,
        )
    return contracts


def link_code(unliked_data, libraries):
    libraries_arg = ','.join((
        ':'.join((lib_name, lib_address))
        for lib_name, lib_address in libraries.items()
    ))
    stdoutdata, stderrdata, _, _ = solc_wrapper(
        stdin_bytes=unliked_data,
        link=True,
        libraries=libraries_arg,
    )

    return stdoutdata.strip()
