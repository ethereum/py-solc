#!/bin/bash
#
# Install solc 
#

set -e
set -u

if [ ! -e solc-versions/solc-0.4.6/solc ] ; then
    mkdir -p solc-versions/solidity-0.4.6
    cd solc-versions/solidity-0.4.6
    git clone --recurse-submodules --branch v0.4.6 https://github.com/ethereum/solidity.git
    cd solidity
    ./scripts/install_deps.sh
    mkdir -p build
    cd build
    cmake .. && make
    ln -fs $PWD/solc/solc ../../../../solc-versions/solc-0.4.6
    chmod +x ../../../../solc-versions/solc-0.4.6
    echo "Solidity installed at $PWD/../../../../solc-versions/solc-0.4.6/solc"
else
    echo "Solidity already installed at $PWD/../../../../solc-versions/solc-0.4.6/solc"
fi
