#!/bin/bash
#
# Install solc 
#

set -e
set -u

if [ ! -e solc-versions/solidity-0.4.6/build/solc/solc ] ; then
    mkdir -p solc-versions/solidity-0.4.6
    cd solc-versions/solidity-0.4.6
    git clone --recurse-submodules --branch v0.4.6 https://github.com/ethereum/solidity.git
    cd solidity
    ./scripts/install_deps.sh
    mkdir -p build
    cd build
    cmake .. && make
    ln -fs $PWD/solc/solc ../../../solc-versions/solc-0.4.6
    chmod +x ../../../solc-versions/solc-0.4.6
    echo "Geth installed at $PWD/solc-0.4.6"
else
    echo "Geth already installed at $PWD/solc/solc-0.4.6"
fi
