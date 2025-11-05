---
allowed-tools:
  - Bash
  - Read
  - Grep
description: "Push commits to GitHub with verification"
---

Push all local commits to GitHub (origin).

**Process:**

1. **Verify Git Status**
   - Check current branch
   - Show commits ahead of origin
   - Verify no uncommitted changes

2. **Pre-Push Summary**
   - Display commits that will be pushed
   - Show files changed in each commit
   - Confirm remote repository exists

3. **Push to Origin**
   - Execute `git push origin [branch]`
   - Handle any errors (authentication, conflicts, etc.)

4. **Post-Push Verification**
   - Confirm push succeeded
   - Display final git status
   - Show GitHub URL if available

**Safety Checks:**
- ⚠️ Never force push unless explicitly requested by user
- ⚠️ Warn if pushing to main/master branch
- ⚠️ Verify branch is tracking a remote
- ⚠️ Check for uncommitted changes before pushing

**If Push Fails:**
- Provide clear error message
- Suggest resolution steps
- Ask user how to proceed

**Output:**
- ✅ Success message with number of commits pushed
- 📊 Summary of what was pushed
- 🔗 GitHub repository link (if available)
