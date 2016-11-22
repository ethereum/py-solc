#!/bin/bash
#
# Install solc 
#

set -e
set -u

if [ ! -e solc-versions/solidity-0.4.5/build/solc/solc ] ; then
    wget -O solc.tar.gz "https://github.com/ethereum/solidity/archive/v0.4.5.tar.gz"
    install -d solc-versions
    cd solc-versions
    tar -zxvf ../solc.tar.gz
    cd solidity-0.4.5
    ./scripts/install_deps.sh
    echo "2dabbdf06f414750ef0425c664f861aeb3e470b8" > commit_hash.txt
    mkdir -p build
    cd build
    cmake .. && make
    ln -fs $PWD/solc/solc ../../../solc-versions/solc-0.4.5
    chmod +x ../../../solc-versions/solc-0.4.5
    echo "Geth installed at $PWD/solc-0.4.5"
else
    echo "Geth already installed at $PWD/solc/solc-0.4.5"
fi
