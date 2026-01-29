cmake_minimum_required(VERSION 3.20)
project(Application)

if (MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4250")
  set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /ENTRY:mainCRTStartup")
endif ()

file(GLOB CONFIG_FILES "${CMAKE_CURRENT_SOURCE_DIR}/img/*")

foreach(CONFIG_FILE ${CONFIG_FILES})
    get_filename_component(CONFIG_FILE_NAME ${CONFIG_FILE} NAME)
    configure_file(${CONFIG_FILE} "${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_FILE_NAME}" COPYONLY)
endforeach()

set(G_SLICE "always-malloc")
add_definitions(-DG_SLICE="${G_SLICE}")

set(G_DEBUG "fatal-criticals")
add_definitions(-DG_DEBUG="${G_DEBUG}")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(Application WIN32 main.cpp Application.cpp popup.cpp units.cpp warn.cpp help.cpp play.cpp RosterModel.cpp)

find_package(PkgConfig REQUIRED)

if (VCPKG_TOOLCHAIN)
  set(GTKMM_PKG_NAMES gtkmm-4.0 gtkmm-3.0)
else ()
  set(GTKMM_PKG_NAMES gtkmm-3.0)
endif ()

foreach(GTKMM_PKG ${GTKMM_PKG_NAMES})
  if (NOT GTKMM_FOUND)
    pkg_check_modules(GTKMM QUIET ${GTKMM_PKG})
  endif ()
endforeach()

if (NOT GTKMM_FOUND)
  message(FATAL_ERROR "Не найден pkg-config пакет gtkmm (пробовали: ${GTKMM_PKG_NAMES}). Проверьте, что gtkmm установлен.")
endif ()

target_include_directories(Application PRIVATE ${GTKMM_INCLUDE_DIRS})
target_link_directories(Application PRIVATE ${GTKMM_LIBRARY_DIRS})
target_link_libraries(Application PRIVATE ${GTKMM_LIBRARIES})

if (VCPKG_TOOLCHAIN)
  find_package(nlohmann_json CONFIG REQUIRED)
  target_link_libraries(Application PRIVATE nlohmann_json::nlohmann_json)
else ()
  find_package(nlohmann_json QUIET)
  if (nlohmann_json_FOUND)
    target_link_libraries(Application PRIVATE nlohmann_json::nlohmann_json)
  endif ()
endif ()
