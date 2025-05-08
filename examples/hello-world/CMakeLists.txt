cmake_minimum_required(VERSION 3.28)
project(HelloWorld)

add_executable(hello-world main.cpp message.cpp)
target_compile_features(hello-world PRIVATE cxx_std_23)
