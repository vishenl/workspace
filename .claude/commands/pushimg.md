---
description: Push only NEW/MODIFIED images to GitHub (smart, not wasteful)
---

# Push Images Command

Intelligently add only new or modified images to git and push to GitHub.

**Strategy:**
1. Check `git status` to find untracked/modified files in `images/` directory
2. Only add NEW images (untracked) or MODIFIED images (changed)
3. If no new images found, inform user and exit
4. If images found, commit with descriptive message and push

**Implementation:**
- Use `git status --porcelain images/` to detect changes
- Filter for untracked (`??`) or modified (`M`) files
- Add only those specific files
- Commit with message listing added images
- Push to GitHub

This ensures we never re-push unchanged images and only handle what's actually new.
