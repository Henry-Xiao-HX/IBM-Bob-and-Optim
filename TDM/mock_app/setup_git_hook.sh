#!/bin/bash
# Setup script to install the pre-commit hook for TDM mock app testing
# Run this script after cloning the repository to enable automated testing

set -e

echo "═══════════════════════════════════════════════════════════════════"
echo "  Setting up Pre-Commit Hook for TDM Mock App"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Get the repository root directory
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"

if [ -z "$REPO_ROOT" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Define paths
HOOK_SOURCE="$REPO_ROOT/TDM/mock_app/git-hooks/pre_commit_test_app_tdm"
HOOK_TARGET="$REPO_ROOT/.git/hooks/pre_commit_test_app_tdm"
HOOK_LINK="$REPO_ROOT/.git/hooks/pre-commit"

# Check if source hook exists
if [ ! -f "$HOOK_SOURCE" ]; then
    echo "❌ Error: Hook source file not found at:"
    echo "   $HOOK_SOURCE"
    echo ""
    echo "   Please ensure you have the latest version of the repository."
    exit 1
fi

# Copy the hook to .git/hooks/
echo "📋 Copying pre-commit hook..."
cp "$HOOK_SOURCE" "$HOOK_TARGET"
chmod +x "$HOOK_TARGET"
echo "✅ Hook copied to .git/hooks/"

# Create symbolic link
echo "🔗 Creating symbolic link..."
if [ -L "$HOOK_LINK" ] || [ -f "$HOOK_LINK" ]; then
    echo "⚠️  Existing pre-commit hook found, backing up..."
    mv "$HOOK_LINK" "$HOOK_LINK.backup.$(date +%s)"
fi

ln -sf "pre_commit_test_app_tdm" "$HOOK_LINK"
echo "✅ Symbolic link created"

# Verify installation
echo ""
echo "🔍 Verifying installation..."
if [ -x "$HOOK_TARGET" ] && [ -L "$HOOK_LINK" ]; then
    echo "✅ Pre-commit hook installed successfully!"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  Installation Complete"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    echo "The pre-commit hook is now active. When you commit changes to"
    echo "TDM/mock_app/app.py, tests will run automatically."
    echo ""
    echo "Test the hook manually:"
    echo "  cd TDM/mock_app && ./run_tests.sh"
    echo ""
    echo "See TDM/mock_app/README.md for full documentation."
    echo ""
else
    echo "❌ Installation verification failed"
    exit 1
fi

# Made with Bob
