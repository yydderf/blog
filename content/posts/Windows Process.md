Tag### Description

Contains information about the resources used by a process on windows, and the characteristics a process can have.

### Memory Types

A process can have 3 different types of memory

- `Private memory` - dedicated to a single process, not shared by other processes.
- `Mapped memory` - can be shared between multiple processes, examples: shared libraries, shared memory segments, and shared files. 
- `Image memory` - contains code and data of an executable file. used to store the code and data that is used by the process. often related to ==DLL files== loaded into a process's address space.

### Process Environment Block (PEB)

Contains information about a process, such as its
- Parameters
- Startup information
- Allocated heap
- Loaded DLLs
- Process ID
- Path to the executable

Used by the operating system to store information about the process, and by the Windows loader to launch applications. 

##### PEB Structure

Important members are:
- [[#BeingDebugged]]
- [[#Ldr]]
- [[#ProcessParameters]]
- [[#AtlThunkSListPtr & AtlThunkSListPtr32]]
- [[#PostProcessInitRoutine]]
- [[#SessionId]]

```c
typedef struct _PEB {
  BYTE                          Reserved1[2];
  BYTE                          BeingDebugged;
  BYTE                          Reserved2[1];
  PVOID                         Reserved3[2];
  PPEB_LDR_DATA                 Ldr;
  PRTL_USER_PROCESS_PARAMETERS  ProcessParameters;
  PVOID                         Reserved4[3];
  PVOID                         AtlThunkSListPtr;
  PVOID                         Reserved5;
  ULONG                         Reserved6;
  PVOID                         Reserved7;
  ULONG                         Reserved8;
  ULONG                         AtlThunkSListPtr32;
  PVOID                         Reserved9[45];
  BYTE                          Reserved10[96];
  PPS_POST_PROCESS_INIT_ROUTINE PostProcessInitRoutine;
  BYTE                          Reserved11[128];
  PVOID                         Reserved12[1];
  ULONG                         SessionId;
} PEB, *PPEB;
```

##### BeingDebugged

Set to 1 if the process is being debugged.

Used by the Windows loader to determine whether to launch the application with a debugger attached or not.

##### Ldr

A pointer to a `PEB_LDR_DATA` structure in the `PEB`
The structure contains information about the process's loaded dynamic link library modules.

It includes a list of DLLs loaded in the process, which is used by the Windows loader to keep track of DLLs loaded in the process.

```c
typedef struct _PEB_LDR_DATA {
  BYTE       Reserved1[8];
  PVOID      Reserved2[3];
  LIST_ENTRY InMemoryOrderModuleList;
} PEB_LDR_DATA, *PPEB_LDR_DATA;
```

```ad-tip
`Ldr` can be leveraged to find the base address of a particular DLL, which can be used to build a ==custom version of GetModuleHandleA/W== to stay stealthy
```
##### ProcessParameters

A pointer to the `PTL_USER_PROCESS_PARAMETERS` structure.

```c
typedef struct _RTL_USER_PROCESS_PARAMETERS {
  BYTE           Reserved1[16];
  PVOID          Reserved2[10];
  UNICODE_STRING ImagePathName;
  UNICODE_STRING CommandLine;
} RTL_USER_PROCESS_PARAMETERS, *PRTL_USER_PROCESS_PARAMETERS;
```

Contains command lines parameters passed to the process when created.

The parameters are added to the PEB by the Windows loader.

```ad-tip
`ProcessParameters` can be leveraged to perform ==command line spoofing==
```

##### AtlThunkSListPtr & AtlThunkSListPtr32

Used by the ATL (Active Template Library) to store a pointer to a linked list of thunking functions.

Thunking functions are used to call functions that are implemented in a different address space, often represent functions exported from a DLL

##### PostProcessInitRoutine

Used to store a pointer to a function called by the operating system after TLS (Thread Local Storage) initialization has been completed for all threads in the process.

This function can also be used to perform additional initialization tasks required by the process.

##### SessionId

A identifier of a single session used for tracking the activity of the user during the session.

### TEB Structure

The import members in TEB
- [[#Process Environment Block (PEB)]]
- [[#TlsSlots]]
- [[#TlsExpansionSlots]]

```c
typedef struct _TEB {
  PVOID Reserved1[12];
  PPEB  ProcessEnvironmentBlock;
  PVOID Reserved2[399];
  BYTE  Reserved3[1952];
  PVOID TlsSlots[64];
  BYTE  Reserved4[8];
  PVOID Reserved5[26];
  PVOID ReservedForOle;
  PVOID Reserved6[4];
  PVOID TlsExpansionSlots;
} TEB, *PTEB;
```

##### ProcessEnvironmentBlock

PEB as described above, stores information about the currently running process.

```ad-note
Processes stands at a higher level in the hierarchy than threads.  
```

##### TlsSlots

Thread local storage is used to store thread-specific data. Each thread has its own TEB with a set of TLS slots.

Thread-specific variables, thread-specific handles, and thread-specific states may be stored in the TLS slot.

##### TlsExpansionSlots

The expansion slots are a set of pointers used to store thread-local storage data for a thread. often reserved for use by system DLLs.

### Process / Thread Handles

Each process / thread has its own unique identifier. One can use these identifiers to get the handle of a process or a thread by `OpenProcess` or `OpenThread`

```ad-note
To avoid handle-leaking, every opened handle should be closed by `CloseHandle` once their use is no longer required.
```