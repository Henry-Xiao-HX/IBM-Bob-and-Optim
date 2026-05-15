#!/bin/bash
# Helper script to manually run SQL tests for TDM/mock_app/credit_risk_queries.sql
# This script can be run independently or is automatically triggered by git pre-commit hook

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  SQL QUERY TEST SUITE${NC}"
echo -e "${BLUE}  Testing with Synthetic Data from Optim Archive${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

# Run the SQL test suite
python3 test_sql.py
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}Your code is validated and ready to commit!${NC}"
    echo ""
else
    echo -e "${RED}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}❌ TESTS FAILED${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${RED}Please fix the issues before committing.${NC}"
    echo ""
fi

exit $TEST_EXIT_CODE

# Made with Bob
