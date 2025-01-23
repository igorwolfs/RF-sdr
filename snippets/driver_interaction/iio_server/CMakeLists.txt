cmake_minimum_required(VERSION 3.10)

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

# set(IIO_EXAMPLES_TARGETS ads9361_test)


# set_target_properties(
#     ${IIO_TESTS_TARGETS} PROPERTIES
# )