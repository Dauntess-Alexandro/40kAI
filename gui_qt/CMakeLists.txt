cmake_minimum_required(VERSION 3.16)
project(40kAI_QtGui LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

set(SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/tabs/TrainTab.cpp
    src/tabs/MetricsTab.cpp
    src/tabs/PlayTab.cpp
    src/tabs/SettingsTab.cpp
    src/tabs/EvalTab.cpp
    src/dialogs/ArmyViewerDialog.cpp
    src/util/ProcessRunner.cpp
    src/util/SettingsStore.cpp
    src/util/RosterStore.cpp
)

set(HEADERS
    src/MainWindow.h
    src/tabs/TrainTab.h
    src/tabs/MetricsTab.h
    src/tabs/PlayTab.h
    src/tabs/SettingsTab.h
    src/tabs/EvalTab.h
    src/dialogs/ArmyViewerDialog.h
    src/util/ProcessRunner.h
    src/util/SettingsStore.h
    src/util/RosterStore.h
    src/util/Types.h
)

add_executable(40kAI_QtGui ${SOURCES} ${HEADERS})

target_include_directories(40kAI_QtGui PRIVATE src)

target_link_libraries(40kAI_QtGui PRIVATE Qt6::Widgets)

if (WIN32)
    set_target_properties(40kAI_QtGui PROPERTIES WIN32_EXECUTABLE TRUE)
endif()
