#!/bin/bash

# Check if argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <ELF file>"
    exit 1
fi

file_name=$1

# Check if file exists
if [ ! -f "$file_name" ]; then
    echo "Error: File does not exist"
    exit 1
fi

# Check if file is ELF
if ! file "$file_name" | grep -q ELF; then
    echo "Error: Not a valid ELF file"
    exit 1
fi

# Extract ELF header information (SAFE version — no xargs issues)
magic_number=$(readelf -h "$file_name" | grep Magic | sed 's/.*: //' | tr -s ' ' | sed 's/^ //')
class=$(readelf -h "$file_name" | grep Class | sed 's/.*: //' | tr -s ' ' | sed 's/^ //')
byte_order=$(readelf -h "$file_name" | grep Data | sed 's/.*: //' | tr -s ' ' | sed 's/^ //')
entry_point_address=$(readelf -h "$file_name" | grep "Entry point address" | sed 's/.*: //' | tr -s ' ' | sed 's/^ //')

# Source messages.sh
source ./messages.sh

# Display output
display_elf_header_info