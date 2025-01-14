cmake_minimum_required(VERSION 3.10)

project(gnuplot_test C)


if (CMAKE_COMPILER_IS_GNUCC)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DIIO_CHECK_RET")
endif ()

include_directories(include)

add_executable(
    gnuplot_test 
    src/main.c
    src/gnu_plot_lib.c 
    ${GETOPT_C_FILE} ${LIBIIO_RC}
)

target_link_libraries(gnuplot_test iio)

set(IIO_EXAMPLES_TARGETS ad9361-test)


set_target_properties(
    ${IIO_TESTS_TARGETS} PROPERTIES C_STANDARD 99 C_STANDARD_REQUIRED ON
                                    C_EXTENSIONS OFF
)