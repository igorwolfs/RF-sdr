cmake_minimum_required(VERSION 3.10)

project(ad9361-test C)


if (CMAKE_COMPILER_IS_GNUCC)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DIIO_CHECK_RET")
endif ()

add_executable(
    ads9361_test ads9361_test.c ${GETOPT_C_FILE} ${LIBIIO_RC}
)

target_link_libraries(ads9361_test iio)

set(IIO_EXAMPLES_TARGETS ad9361-test)

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


set_target_properties(
    ${IIO_TESTS_TARGETS} PROPERTIES C_STANDARD 99 C_STANDARD_REQUIRED ON
                                    C_EXTENSIONS OFF
)

# We don't install any of these, they are examples, not tools. We build them to
# make sure they build/work, not to deploy them.
