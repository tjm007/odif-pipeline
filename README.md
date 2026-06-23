# Operational Decision Intelligence Framework (ODIF)

**Finding and fixing the gaps between data, systems, and business processes.**

## Overview

The Operational Decision Intelligence Framework (ODIF) is a modular data analysis and decision-support framework designed to mirror how real business problems are investigated and solved.

Most organizations do not suffer from a lack of data. They suffer from uncertainty about whether the data is accurate, complete, trusted, and relevant to the decision being made.

ODIF was created to address that problem.

Rather than starting with dashboards or visualizations, ODIF starts with a simple question:

> Can we trust the information being used to make a decision?

## Design Philosophy

ODIF is influenced by my professional experience working with product information management, catalog operations, reporting, pricing analysis, and business systems.

Throughout my career, I have frequently investigated situations where:

- Data from multiple systems did not agree
- Product information was incomplete or inconsistent
- Reports produced unexpected results
- Business processes were failing
- Teams lacked confidence in the information available to them

In many cases, the technical issue was only part of the problem. The larger challenge was understanding how data, systems, and business processes interacted.

ODIF follows that same investigative approach:

```text
Understand
→ Validate
→ Analyze
→ Explain
→ Decide
```
## Current Modules

### PIM Asset Inspector

A validation tool for product information management workflows that verifies:

- Required assets
- File naming conventions
- Image dimensions
- File formats
- Launch readiness requirements

See:
src/pim_asset_inspector/README.md
