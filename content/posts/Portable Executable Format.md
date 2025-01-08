---
title: Portable Executable Format
date: 2025-01-07
tags:
  - Windows
Description: Contains the structure of Windows executable file format and some introduction about the function of each part in the structure.
---
### PE File Extensions

The following is the list of PE file extensions:
- `.exe` - run directly by the user, contains the main entry point.
- `.dll` - dynamic-link library that can be used by multiple programs
- `.sys` - device drivers or low-level system components
- `.scr` - screen saver files, run by the system when the screen saver is activated.

### PE Structure

The structure contains the following sections
- [[#DOS Header]]
- [[#DOS Stub]]
- [[#NT Headers]]
	- NT Signature
	- File Header
	- Optional Header
- [[#Data Directories]]
- [[#Sections]]

### DOS Header

At the start of PE files, always prefixed with two bytes, `0x4D` and `0x5A`, or `MZ` in ASCII.

The data structure of DOS Header (_IMAGE_DOS_HEADER) is listed as below:

The important members of the structure are `e_magic` and `e_lfanew`, the former is used to store the magic number `MZ` to file format recognition, the latter is a 4-byte value that store the offset to the start of the NT Header.

`e_lfanew` is always located at an offset of `0x3C`

```c
typedef struct _IMAGE_DOS_HEADER {      // DOS .EXE header
    WORD   e_magic;                     // Magic number
    WORD   e_cblp;                      // Bytes on last page of file
    WORD   e_cp;                        // Pages in file
    WORD   e_crlc;                      // Relocations
    WORD   e_cparhdr;                   // Size of header in paragraphs
    WORD   e_minalloc;                  // Minimum extra paragraphs needed
    WORD   e_maxalloc;                  // Maximum extra paragraphs needed
    WORD   e_ss;                        // Initial (relative) SS value
    WORD   e_sp;                        // Initial SP value
    WORD   e_csum;                      // Checksum
    WORD   e_ip;                        // Initial IP value
    WORD   e_cs;                        // Initial (relative) CS value
    WORD   e_lfarlc;                    // File address of relocation table
    WORD   e_ovno;                      // Overlay number
    WORD   e_res[4];                    // Reserved words
    WORD   e_oemid;                     // OEM identifier (for e_oeminfo)
    WORD   e_oeminfo;                   // OEM information; e_oemid specific
    WORD   e_res2[10];                  // Reserved words
    LONG   e_lfanew;                    // Offset to the NT header
  } IMAGE_DOS_HEADER, *PIMAGE_DOS_HEADER;
```


### DOS Stub

This section is created for back compatibility, when executing the program in DOS mode, the error message `This program cannot be run in DOS mode` is printed. 

```ad-tip
The error message can be changed by the programmer at compile time.
```


### NT Header

The section starts with a signature, `PE` is usually the string value of the signature.

The data structure of NT Header varies with the machine's architecture. The `OptionalHeader` is the only difference between the two versions.

```c
/// 32-bit
typedef struct _IMAGE_NT_HEADERS {
  DWORD                   Signature;
  IMAGE_FILE_HEADER       FileHeader;
  IMAGE_OPTIONAL_HEADER32 OptionalHeader;
} IMAGE_NT_HEADERS32, *PIMAGE_NT_HEADERS32;
```
```c
/// 64-bit
typedef struct _IMAGE_NT_HEADERS64 {
    DWORD                   Signature;
    IMAGE_FILE_HEADER       FileHeader;
    IMAGE_OPTIONAL_HEADER64 OptionalHeader;
} IMAGE_NT_HEADERS64, *PIMAGE_NT_HEADERS64;
```

There are two headers that reside in NT Header
`FileHeader` and `OptionalHeader`, both of which include a large amount of information about the file.

##### File Header 

Contains the following important information
- `NumberOfSections` - number of sections in the file
- `Characteristics` - specify whether the file is a library of a console program
- `SizeOfOptionalHeader` - the size of the following optional header
##### Optional Header

The size of optional header varies with the machine's architecture

Some members that use `DWORD` as their data type on a 32-bit machine will use `ULONGLONG` on a 64-bit machine instead.

Contains the following critical members:
- `Magic` - describes whether the image is 32-bit or 64-bit 
- `MajorOperatingSystemVersion` - Required major operating system version (eg. 10, 11)
- `MinorOperatingSystemVersion` - Required minor operating system version (eg. 1511, 1507)
- `SizeOfCode` - size of the `.text` section
- `AddressOfEntryPoint` - offset to the entry point of the file (eg. main)
- `BaseOfCode` - offset to the `.text` section
- `SizeOfImage` -  size of the image in bytes
- `ImageBase` - the preferred address of how the application is to be loaded into memory. Due to ASLR, it is rarely realized.
- `DataDirectory` - an array of IMAGE_DATA_DIRECTORY, contains the directories in a PE file.

### Data Directories

An important member in the optional header, an array of size 16 (IMAGE_NUMBEROF_DIRECTORY_ENTRIES)

```c
typedef struct _IMAGE_DATA_DIRECTORY {
	DWORD VirtualAddress;
	DWORD Size;
} IMAGE_DATA_DIRECTORY, *PIMAGE_DATA_DIRECTORY;
```

Each entry includes some data about a PE section of a data table, the following is the corresponding information of each index

```c
IMAGE_DIRECTORY_ENTRY_EXPORT          0   // Export Directory
IMAGE_DIRECTORY_ENTRY_IMPORT          1   // Import Directory
IMAGE_DIRECTORY_ENTRY_RESOURCE        2   // Resource Directory
IMAGE_DIRECTORY_ENTRY_EXCEPTION       3   // Exception Directory
IMAGE_DIRECTORY_ENTRY_SECURITY        4   // Security Directory
IMAGE_DIRECTORY_ENTRY_BASERELOC       5   // Base Relocation Table
IMAGE_DIRECTORY_ENTRY_DEBUG           6   // Debug Directory
IMAGE_DIRECTORY_ENTRY_ARCHITECTURE    7   // Architecture Specific Data
IMAGE_DIRECTORY_ENTRY_GLOBALPTR       8   // RVA of GP
IMAGE_DIRECTORY_ENTRY_TLS             9   // TLS Directory
IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG    10   // Load Configuration Directory
IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT   11   // Bound Import Directory in headers
IMAGE_DIRECTORY_ENTRY_IAT            12   // Import Address Table
IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT   13   // Delay Load Import Descriptors
IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR 14   // COM Runtime descriptor
```

`Export Directory` and `Import Address Table` are two interesting directories.

`Export Directory` - contains information about functions and variables that are exported from the executable. This directory is generally found in DLLs that export functions (eg. `kernel32.dll` exporting `CreateFileA`)
`Image Address Table` - contains information about the addresses of functions that are imported from other executables. (eg. `app.exe` importing `CreateFileA` from `kernel32.dll`)

```ad-note
Hierarchy of the members

- NT Headers
	- Optional Header
		- Data Directories
```
### Sections

The number of sections in a PE file is dynamic, since the section can be added be a compiler or manually added later on. `IMAGE_FILE_HEADER.NumberOfSections` helps determine the number.

Common sections are listed as below:
- `.text` - contains executable codes
- `.data` - contains initialized data
- `.rdata` - contains read only data
- `.idata` - contains the import tables, used by PE loader to determine which DLL files need to be loaded to the process, along with the functions that are being used from each DLL.
- `.reloc` - contains information on how to fix up memory addresses.
- `.rsrc` - contains resources such as icons, bitmaps.

Each PE section has an `IMAGE_SECTION_HEADER` data structure. These sections are saved under the NT headers, and are stacked up together.

Each structure represents a section

```c
typedef struct _IMAGE_SECTION_HEADER {
  BYTE  Name[IMAGE_SIZEOF_SHORT_NAME];
  union {
    DWORD PhysicalAddress;
    DWORD VirtualSize;
  } Misc;
  DWORD VirtualAddress;
  DWORD SizeOfRawData;
  DWORD PointerToRawData;
  DWORD PointerToRelocations;
  DWORD PointerToLinenumbers;
  WORD  NumberOfRelocations;
  WORD  NumberOfLinenumbers;
  DWORD Characteristics;
} IMAGE_SECTION_HEADER, *PIMAGE_SECTION_HEADER;
```

- `Name` - the name of the section
- `PhysicalAddress` / `VirtualSize` - the size of the section when it's in memory.
- `VirtualAddress` - offset of the start of the section in memory.