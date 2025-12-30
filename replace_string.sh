#!/bin/sh


find . -type f -name "*.txt" -exec sed -i -e 's/foo/bar/g' {} +