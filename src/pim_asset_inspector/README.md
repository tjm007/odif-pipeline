# PIM Asset Inspector

## Purpose

PIM Asset Inspector validates product asset files before they are loaded into a Product Information Management (PIM), Digital Asset Management (DAM), or ecommerce platform.

The tool helps identify asset-readiness issues such as invalid filenames, unsupported file types, incorrect image dimensions, and files that do not match configurable upload rules.

## Current Status

Version: 0.1

Implemented:
- Project structure
- JSON rules file
- JSON rules loader

In Progress:
- File inventory
- Filename validation

Planned:
- Image format detection
- Image dimension checks
- CSV inspection report
- Markdown summary report
- CSV-to-JSON rule conversion
- Multi-asset validation for images, documents, videos, and other file types

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