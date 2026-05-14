#!/bin/bash
LANGUAGE=$1

echo "Scanning repository for $LANGUAGE tests..."

find . -type d -name "$LANGUAGE" | while read dir; do
    echo "Running tests in $dir"
    cd "$dir"
    
    case $LANGUAGE in
        python)     pytest ;;
        typescript) npm install && npm test ;;
        go)         go test -v ./... ;;
        rust)       cargo test ;;
        java)       mvn clean test ;;
        csharp)     dotnet test ;;
        cpp)        g++ -std=c++17 test.cpp -o test_bin && ./test_bin ;;
    esac
    
    cd - > /dev/null
done
