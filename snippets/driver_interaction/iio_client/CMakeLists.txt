cmake_minimum_required(VERSION 3.10)

set (CMAKE_C_COMPILER  "$ENV{PLUTOSDR_TOOLCHAIN}/arm-linux-gnueabihf-gcc")
set (CMAKE_CXX_COMPILER  "$ENV{PLUTOSDR_TOOLCHAIN}/arm-linux-gnueabihf-g++")
set (CMAKE_SYSROOT "$ENV{PLUTOSDR_SYSROOT}")
project(ads9361_test C)


if (CMAKE_COMPILER_IS_GNUCC)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DIIO_CHECK_RET")
endif ()

include_directories(helper_lib/include)

set(SOURCES
    src/main.c
    helper_lib/src/csv_writer.c
)

add_executable(
    ads9361_libiio_txrx.bin
    ${SOURCES}
    ${GETOPT_C_FILE} ${LIBIIO_RC}
)


target_link_libraries(ads9361_libiio_txrx.bin 
    m
    iio)

find_library(PTHREAD_LIBRARIES pthread)
find_library(CURSES_LIBRARY curses)
find_library(CDK_LIBRARY cdk)

include(CheckSymbolExists)

if (PTHREAD_LIBRARIES
    AND CURSES_LIBRARY
    AND CDK_LIBRARY
)
    find_path(LIBCKD_INCLUDE_DIR cdk.h PATH_SUFFIXES cdk)

    set(TEMP ${CMAKE_REQUIRED_LIBRARIES})
    set(TEMP1 ${CMAKE_REQUIRED_INCLUDES})
    list(APPEND CMAKE_REQUIRED_LIBRARIES ${CURSES_LIBRARY} ${CDK_LIBRARY})
    list(APPEND CMAKE_REQUIRED_INCLUDES ${LIBCKD_INCLUDE_DIR})
    set(TMP_FLAGS "${CMAKE_C_FLAGS}")
    set(CMAKE_C_FLAGS "")
    check_symbol_exists(CDK_CSTRING2 "cdk.h" HAS_CDK_CSTRING2)
    set(CMAKE_C_FLAGS "${TMP_FLAGS}")
    set(CMAKE_REQUIRED_LIBRARIES ${TEMP})
    set(CMAKE_REQUIRED_INCLUDES ${TEMP1})
endif()

if(HAS_CDK_CSTRING2)
    include_directories(${LIBCKD_INCLUDE_DIR})
    project(iio-monitor C)
    add_executable(iio-monitor iio-monitor.c)
    target_link_libraries(
        iio-monitor iio ${PTHREAD_LIBRARIES} ${CURSES_LIBRARY} ${CDK_LIBRARY}
    )
    set(IIO_TESTS_TARGETS ${IIO_TESTS_TARGETS} iio-monitor)
else()
    message(STATUS "Curses Development Kit (CDK) missing or too old, skipping iio-monitor")
endif ()



set_target_properties(ads9361_libiio_txrx.bin
     PROPERTIES C_STANDARD 99 C_STANDARD_REQUIRED ON
                                    C_EXTENSIONS OFF
)
