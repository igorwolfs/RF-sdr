# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx

# Include any dependencies generated for this target.
include CMakeFiles/auto_rate_test.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/auto_rate_test.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/auto_rate_test.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/auto_rate_test.dir/flags.make

CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o: CMakeFiles/auto_rate_test.dir/flags.make
CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o: auto_rate_test_hw.c
CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o: CMakeFiles/auto_rate_test.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o -MF CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o.d -o CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o -c /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx/auto_rate_test_hw.c

CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx/auto_rate_test_hw.c > CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.i

CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx/auto_rate_test_hw.c -o CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.s

# Object files for target auto_rate_test
auto_rate_test_OBJECTS = \
"CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o"

# External object files for target auto_rate_test
auto_rate_test_EXTERNAL_OBJECTS =

auto_rate_test: CMakeFiles/auto_rate_test.dir/auto_rate_test_hw.c.o
auto_rate_test: CMakeFiles/auto_rate_test.dir/build.make
auto_rate_test: CMakeFiles/auto_rate_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable auto_rate_test"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/auto_rate_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/auto_rate_test.dir/build: auto_rate_test
.PHONY : CMakeFiles/auto_rate_test.dir/build

CMakeFiles/auto_rate_test.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/auto_rate_test.dir/cmake_clean.cmake
.PHONY : CMakeFiles/auto_rate_test.dir/clean

CMakeFiles/auto_rate_test.dir/depend:
	cd /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx /home/iwolfs/Work/Projects/rf_sdr_project/RF-sdr/snippets/raw/sine_txrx/CMakeFiles/auto_rate_test.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/auto_rate_test.dir/depend

