# ReaBank Files

Includes .reabank files for several midi keyboards, allowing their instruments to be selected from within a daw using the Reaper ReaControlMIDI vst:

* **Roland FP-90** (should also work with other keyboards in the FP- series)
* **Yamaha PSR-E323**

Several .reabank files are included per keyboard, one containing all the instruments, and smaller ones split by category.

The .reabank files can be downloaded from the [releases](https://github.com/smaldragon/ReaBank/releases/) page.

---

## Technical

The files are generated with the python `rea-parse.py` script, based on copy-pasted tables taken from the keyboard's official manuals. 

When run the script looks for folders within its directory that contain a `pdfdata.txt`file. This file contains a simple short header in the first line describing the layout of the data table (ie. `i_no name msb lsb pc`) followed by the data itself, as copied from the pdf manual.
