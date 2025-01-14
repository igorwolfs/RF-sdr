cmake_minimum_required(VERSION 3.10)

project(ads9361_test C)


if (CMAKE_COMPILER_IS_GNUCC)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DIIO_CHECK_RET")
endif ()

include_directories(helper_lib/include)

add_executable(
    ads9361_test 
    src/main.c
    helper_lib/src/gnu_plot_lib.c 
    ${GETOPT_C_FILE} ${LIBIIO_RC}
)


target_link_libraries(ads9361_test iio)

set(IIO_EXAMPLES_TARGETS ads9361_test)


set_target_properties(
    ${IIO_TESTS_TARGETS} PROPERTIES C_STANDARD 99 C_STANDARD_REQUIRED ON
                                    C_EXTENSIONS OFF
)