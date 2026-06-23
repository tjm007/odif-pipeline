# PIM Asset Inspector

## Purpose

PIM Asset Inspector validates product assets before they are published to Product Information Management (PIM), Digital Asset Management (DAM), and ecommerce platforms.

The tool identifies asset-readiness issues such as invalid filenames, unsupported file types, incorrect image specifications, missing required product views, and other violations of configurable upload rules.

## Business Context

This project was inspired by real-world Product Information Management (PIM) workflows involving product launches, catalog governance, digital asset management, and product metadata quality.

In large catalogs, missing images, inconsistent naming conventions, incorrect file specifications, and incomplete product presentations can delay product launches and create customer-facing issues.

The PIM Asset Inspector was designed to identify these issues before assets are published to downstream systems.

## Quick Links

- [Example Workflow](#example-workflow)
- [Current Validation Capabilities](#current-validation-capabilities)
- [Current Status](#current-status)
- [Long-Term Vision](#long-term-vision)

## Example Workflow

### Input Assets

```text
SKU123_FRONT_01.jpg
SKU123_BACK_01.jpg
SKU123_SIDE_01.jpg

SKU456_FRONT_01.jpg
SKU456_BACK_01.jpg
```

### Validation Process

```text
Asset Files
     ↓
File Inventory
     ↓
Filename Validation
     ↓
Image Validation
     ↓
Required Asset Validation
     ↓
CSV Report
```

### Required Asset Validation Results

| SKU | Status | Missing Views |
|------|------|------|
| SKU123 | PASS | |
| SKU456 | FAIL | SIDE |

### Example Issues

```text
SKU456
Missing required view: SIDE
```

### Try It

Run the inspector against a sample asset folder:

```bash
python -m src.pim_asset_inspector
```

For a complete list of validations, see [Current Validation Capabilities](#current-validation-capabilities).

## Sample Outputs

### File-Level Validation Report

The detailed asset report captures validation status and extracted metadata for each file.

![File Validation Report](docs/images/pim_asset_file_report.png)

### Required Asset Validation Report

The required asset report evaluates product-level completeness and identifies missing product views.

![Required Asset Report](docs/images/required_asset_report.png)

This separation allows teams to review both individual asset quality and overall product launch readiness.

## Current Validation Capabilities

- File inventory
- Filename convention validation
- SKU, view, and sequence parsing
- Image format detection
- Image resolution validation
- File size validation
- Color mode validation
- Required product view validation
- Batch-level skipped file tracking
- CSV reporting

## Why This Matters

Product data teams frequently manage thousands of assets across multiple products, sales channels, and regions.

The PIM Asset Inspector helps improve:

- Asset naming consistency
- Image specification compliance
- Product presentation completeness
- Catalog governance
- Product launch readiness

By identifying issues earlier in the workflow, teams can reduce manual review effort and improve the quality of published product content.

## Technology Stack

- Python 3.12
- Pillow
- Pytest
- JSON Configuration
- CSV Reporting
- Rule-Based Validation Engine

## Quality Assurance

The project includes automated unit tests covering:

- Filename validation
- Image validation
- Color mode validation
- Required asset validation
- Batch-level validation behavior
- Report generation

Current test status: 25 passing tests.

## Current Status

Version: 0.2

### Implemented

- File inventory
- JSON rules loader
- Filename validation
- SKU, view, and sequence parsing
- Image format detection
- Image resolution validation
- File size validation
- Color mode validation
- Required asset validation
- CSV report generation
- Automated test coverage

### In Progress

- End-to-end reporting workflow
- Documentation improvements

### Planned

- Markdown summary report
- CSV-to-JSON rule conversion
- Document asset validation
- Video asset validation
- Multi-profile rule sets

## Inputs

- Asset folder
- JSON rules file

## Outputs

Current:

- CSV validation report
- Required asset validation report

Planned:

- Markdown summary report

## Design Direction

The validation engine receives normalized rules as a Python dictionary, allowing validation logic to remain independent of rule storage formats.

Future rule sources may include:

- CSV templates
- Excel workbooks
- Database tables
- PIM configuration exports

## Long-Term Vision

The PIM Asset Inspector is being developed as a reusable validation framework rather than a single-purpose script.

Future versions are intended to support:

- Additional asset types
- Multiple validation profiles
- PIM-specific rule sets
- DAM workflows
- Product launch readiness audits
- Catalog governance reporting

The goal is to create a flexible validation platform that can be adapted to a variety of product content and digital asset management workflows.