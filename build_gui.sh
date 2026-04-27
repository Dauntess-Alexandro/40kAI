#!/usr/bin/env bash
set -e

cd ~/40kAI/runtime_data
mkdir -p build
cd build

cmake ..
make -j"$(nproc)"

echo
echo "✅ GUI build finished: $(pwd)"
read -p "Press Enter to close..." _
