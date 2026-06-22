# PIM Asset Inspector

## Purpose

PIM Asset Inspector validates product asset files before they are loaded into a Product Information Management (PIM), Digital Asset Management (DAM), or ecommerce platform.

The tool helps identify asset-readiness issues such as invalid filenames, unsupported file types, incorrect image dimensions, and files that do not match configurable upload rules.

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

| SKU    | Status | Missing Views |
| ------ | ------ | ------------- |
| SKU123 | PASS   |               |
| SKU456 | FAIL   | SIDE          |

### Example Issues

```text
SKU456
Missing required view: SIDE
```

### Current Validation Capabilities

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

Product Information Management (PIM) teams frequently manage thousands of product assets across multiple sales channels. Missing images, inconsistent naming conventions, incorrect file specifications, and incomplete product presentations can delay product launches and create a poor customer experience.

The PIM Asset Inspector helps identify asset quality and completeness issues before publication by validating:

- Asset naming standards
- Image specifications
- Product view requirements
- Catalog completeness

This allows product data teams to identify issues earlier, improve data governance, and support more consistent product launches.

## Technology Stack

- Python 3.12
- Pytest
- Pillow
- CSV Reporting
- JSON Configuration
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

Implemented:

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

In Progress:

- End-to-end reporting workflow
- Documentation improvements

Planned:

- Markdown summary report
- CSV-to-JSON rule conversion
- Document asset validation
- Video asset validation
- Multi-profile rule sets

## Inputs

- Asset folder
- JSON rules file

## Outputs

- CSV validation report
- Markdown summary report

## Design Direction

The validation engine should receive normalized rules as a Python dictionary.

Future rule sources may include:

- CSV template
- Excel workbook
- Database table
- PIM configuration export