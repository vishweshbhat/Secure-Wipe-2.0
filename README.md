# ByteShift - Secure Data Wiping Tool

## Overview

ByteShift is a cross-platform secure data wiping tool that supports wiping files, partitions, and full disks (including hidden areas like HPA/DCO, SSD sectors). It generates digitally signed tamper-proof wipe certificates (PDF/JSON) and aims to enable trustworthy IT asset recycling aligned with NIST SP 800-88 standards.

---

## Features

- Multi-pass overwrite compliant with NIST for HDDs.
- Firmware Secure Erase support for SSDs.
- One-click user-friendly interface.
- Cross-platform support (Windows, Linux, Android).
- Verification via cryptographically signed reports.
- Planned offline use with bootable USB/ISO media.

---

## Project Specification

### Objective

To design and implement a tool that securely wipes data from drives/partitions/files and generates a digitally signed verification report that proves the data is unrecoverable.

### Features

**Core Features**

- Selective Wiping  
  Wipe specific files/folders, selected partitions, or entire drives (including OS if chosen).

- Multiple Wiping Methods  
  Single-pass overwrite (quick) and multi-pass overwrite (secure, e.g., DoD/Gutmann).

- Dry Run Mode  
  Simulates wiping without touching actual data (for demo and testing).

- Verification  
  Verify wiped regions contain only chosen patterns/random data and generate detailed reports.

- Report Generation  
  JSON/PDF format containing: Target (file/partition/drive), Wiping method used, Timestamp, Verification result (Success/Failure).

- Digital Signing  
  Report signed with tool’s private key; verification possible using public key.

**Optional / Advanced Features**

- Bootable USB ISO option (for wiping without OS interference).  
- Enterprise log export (send reports to central server).  
- Simple GUI (to replace CLI).

### Constraints / Safety

- Must never wipe system disk by accident.  
- Require explicit confirmation before destructive actions.  
- Must support dry run for testing and demo.  
- Testing must be done only on virtual disks/dummy files.

### Deliverables

- Working wipe engine.  
- Verification module.  
- Report generator with digital signatures.  
- Documentation (design, how-to-use, safety notes).  
- Demo (safe run on test disk with dry run + real wipe on dummy image).

### Done Criteria

- Selective wipe: User can choose target (file, partition, or disk).  
- Wiping method: At least 2 overwrite methods available.  
- Dry run: Produces simulated output + report without touching data.  
- Verification: Tool scans wiped target and confirms overwrite.  
- Report: JSON file generated with all required details.  
- Digital signing: Report can be verified with a public key.

---

## Design and Architecture

### High-Level Architecture

- `main.py`: Orchestrates wiping, verification, report generation.  
- `src/wipe_utils.py`: Implements wiping logic for HDD and SSD.  
- `src/verify.py`: Verifies deletion; HDD binary checks/SSD warnings.  
- `src/report.py`: Generates reports (JSON/HTML/PDF) with SHA256 hash and optional signature.

### Workflow

1. User provides path of file/partition.  
2. `main.py` detects drive type.  
3. File/partition is wiped using `wipe_utils.wipe()`:
   - HDD: multi-pass overwrite.  
   - SSD: overwrite + encrypt + delete.  
4. Verification:
   - HDD: samples binary data at random offsets.  
   - SSD: existence check and warning about wear-leveling.  
5. `report.py` generates a report:
   - Includes file hash, verification status, wipe method, drive type.  
   - Saves report in `/reports`.  
   - Signs report with unique private key.

### Decision Points

- HDD vs SSD determines wipe and verification method.  
- File vs Partition determines whether bootable media is required.  
- Verification method: Multi-pass for HDD; existence/encryption for SSD.

### Notes

- SSD verification cannot fully guarantee unrecoverability due to wear-leveling.  
- Future work: integrate online verification portal.

---

## Workflow Summary

User selects mode →  
- File Wipe → Overwrite + Delete + Verify + Report  
- Partition Wipe →  
  - Is OS? →  
    - Yes → Bootable Media  
    - No → Wipe directly  
- Full Device → Bootable Media required

---

## Report Format

Each report contains:  
1. Wipe mode  
2. Target (file/partition/device)  
3. Method used (passes, overwrite type)  
4. Verification status  
5. Timestamp  
6. Signature/hash

---

## Changelog

### v1.0 – Current

- Added SSD wipe logic: overwrite + encrypt + delete.  
- Updated HDD verification: multi-pass binary sampling.  
- Updated `main.py` to integrate new `verify.py`.  
- Reports now include:  
  - Verification notes (HDD/SSD)  
  - SHA256 hash of file  
  - Verification code  
- Removed `mode` argument from `verify_wipe()`.  
- Added `detect_drive_type()` helper for drive detection.  
- Updated frontend integration planned.

---

## Installation

Requires Python 3.x. Install dependencies:

pip install -r requirements.txt


---

## Usage

Run the main application:

python main.py


---

## Future Scope

- Bootable ISO/live USB integration for full OS disk wiping.  
- Extended hidden area wiping support (HPA/DCO).  
- Enhanced SSD compatibility and detection.  
- Online verification portal to validate wipe reports.

---

## License

MIT License. See LICENSE file.


