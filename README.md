# Multi-Agent AI System for Document Processing

This repository contains a modular multi-agent AI system designed to process various document types such as emails, JSON invoices, and PDFs. The system uses zero-shot classification to detect the intent of the document (e.g., invoice, complaint, RFQ) and routes the content to specialized agents for processing. Processed data and metadata are logged into a SQLite shared memory database for persistence and analysis.

## Features

- Zero-shot classification of document intents using Hugging Face transformer models.
- Dedicated agents for handling emails, JSON files, and PDFs.
- Extraction of structured data like sender, urgency, invoice fields, etc.
- Shared memory implemented with SQLite for logging processed documents and metadata.
- Support for multiple input formats: `.txt`, `.json`, `.pdf`.
- Log viewing and export capability with duplicate removal and CSV output.

