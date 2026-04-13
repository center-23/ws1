cmake_minimum_required(VERSION 3.5)
project(sim)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

install(
  DIRECTORY launch rviz config world maps urdf  
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
