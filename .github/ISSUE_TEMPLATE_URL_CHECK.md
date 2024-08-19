---
title: "🚨 Broken URLs Detected: {{ env.TOTAL_ISSUES }} issues found"
labels: bug, documentation
---

## URL Check Results

### Issues Found: {{ env.TOTAL_ISSUES }}

| File | Line | URL | Status Code | Reason |
|------|------|-----|-------------|--------|
{{ env.ISSUE_TABLE }}
