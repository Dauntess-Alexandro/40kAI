#include <GLFW/glfw3.h>
#include <imgui.h>
#include <imgui_impl_glfw.h>
#include <imgui_impl_opengl2.h>

#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <string>
#include <vector>

#include "app_state.h"
#include "play_state.h"
#include "train_state.h"
#include "ui_panels.h"

namespace {
ImFont* LoadRussianFont(ImGuiIO& io) {
  const std::filesystem::path cwd = std::filesystem::current_path();
  std::vector<std::string> candidates;
  auto add_font_candidates = [&](const std::filesystem::path& base) {
    candidates.emplace_back((base / "fonts/Roboto-Regular.ttf").string());
    candidates.emplace_back((base / "fonts/NotoSans-Regular.ttf").string());
    candidates.emplace_back((base / "fonts/DejaVuSans.ttf").string());
    candidates.emplace_back((base / "gui_imgui/fonts/Roboto-Regular.ttf").string());
    candidates.emplace_back((base / "gui_imgui/fonts/NotoSans-Regular.ttf").string());
    candidates.emplace_back((base / "gui_imgui/fonts/DejaVuSans.ttf").string());
  };
  if (const char* env_path = std::getenv("IMGUI_FONT_PATH")) {
    candidates.emplace_back(env_path);
  }
  std::filesystem::path current = cwd;
  for (int depth = 0; depth < 5; ++depth) {
    add_font_candidates(current);
    if (!current.has_parent_path()) {
      break;
    }
    current = current.parent_path();
  }
  candidates.emplace_back("gui_imgui/fonts/Roboto-Regular.ttf");
  candidates.emplace_back("gui_imgui/fonts/NotoSans-Regular.ttf");
  candidates.emplace_back("gui_imgui/fonts/DejaVuSans.ttf");
  candidates.emplace_back("fonts/Roboto-Regular.ttf");
  candidates.emplace_back("fonts/NotoSans-Regular.ttf");
  candidates.emplace_back("fonts/DejaVuSans.ttf");

  for (const auto& path : candidates) {
    if (!path.empty() && std::filesystem::exists(path)) {
      ImFont* font = io.Fonts->AddFontFromFileTTF(path.c_str(), 18.0f, nullptr,
                                                  io.Fonts->GetGlyphRangesCyrillic());
      if (font) {
        return font;
      }
    }
  }

  std::fprintf(stderr,
               "Не удалось загрузить шрифт с кириллицей. "
               "Укажите путь через переменную IMGUI_FONT_PATH "
               "или положите файл в gui_imgui/fonts/. "
               "Текущая директория: %s\n",
               cwd.string().c_str());
  return nullptr;
}

void ApplyWarhammerStyle() {
  ImGuiStyle& style = ImGui::GetStyle();
  style.WindowRounding = 4.0f;
  style.FrameRounding = 3.0f;
  style.GrabRounding = 2.0f;
  style.ScrollbarRounding = 2.0f;
  style.FrameBorderSize = 1.0f;
  style.WindowBorderSize = 1.0f;

  ImVec4* colors = style.Colors;
  colors[ImGuiCol_Text] = ImVec4(0.92f, 0.88f, 0.78f, 1.00f);
  colors[ImGuiCol_WindowBg] = ImVec4(0.10f, 0.10f, 0.10f, 1.00f);
  colors[ImGuiCol_FrameBg] = ImVec4(0.18f, 0.18f, 0.18f, 1.00f);
  colors[ImGuiCol_FrameBgHovered] = ImVec4(0.28f, 0.25f, 0.20f, 1.00f);
  colors[ImGuiCol_FrameBgActive] = ImVec4(0.35f, 0.30f, 0.22f, 1.00f);
  colors[ImGuiCol_Button] = ImVec4(0.35f, 0.28f, 0.15f, 1.00f);
  colors[ImGuiCol_ButtonHovered] = ImVec4(0.50f, 0.40f, 0.20f, 1.00f);
  colors[ImGuiCol_ButtonActive] = ImVec4(0.65f, 0.50f, 0.25f, 1.00f);
  colors[ImGuiCol_Border] = ImVec4(0.55f, 0.45f, 0.25f, 1.00f);
  colors[ImGuiCol_TitleBg] = ImVec4(0.12f, 0.12f, 0.12f, 1.00f);
  colors[ImGuiCol_TitleBgActive] = ImVec4(0.22f, 0.18f, 0.12f, 1.00f);
  colors[ImGuiCol_CheckMark] = ImVec4(0.80f, 0.65f, 0.20f, 1.00f);
  colors[ImGuiCol_SliderGrab] = ImVec4(0.70f, 0.58f, 0.20f, 1.00f);
  colors[ImGuiCol_SliderGrabActive] = ImVec4(0.90f, 0.75f, 0.25f, 1.00f);
  colors[ImGuiCol_Header] = ImVec4(0.28f, 0.24f, 0.18f, 1.00f);
  colors[ImGuiCol_HeaderHovered] = ImVec4(0.38f, 0.32f, 0.22f, 1.00f);
  colors[ImGuiCol_HeaderActive] = ImVec4(0.50f, 0.40f, 0.25f, 1.00f);
}
}

int main() {
  if (!glfwInit()) {
    std::fprintf(stderr, "Не удалось инициализировать GLFW.\n");
    return 1;
  }

  GLFWwindow* window = glfwCreateWindow(1280, 720, "40kAI: ImGui минимальный GUI", nullptr, nullptr);
  if (!window) {
    std::fprintf(stderr, "Не удалось создать окно GLFW.\n");
    glfwTerminate();
    return 1;
  }

  glfwMakeContextCurrent(window);
  glfwSwapInterval(1);

  IMGUI_CHECKVERSION();
  ImGui::CreateContext();
  ImGuiIO& io = ImGui::GetIO();
  io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
  ImFont* russian_font = LoadRussianFont(io);
  if (russian_font) {
    io.FontDefault = russian_font;
  }

  ImGui::StyleColorsDark();
  ApplyWarhammerStyle();

  ImGui_ImplGlfw_InitForOpenGL(window, true);
  ImGui_ImplOpenGL2_Init();

  AppState state;
  PlayState play_state;
  TrainState train_state;

  while (!glfwWindowShouldClose(window)) {
    glfwPollEvents();

    ImGui_ImplOpenGL2_NewFrame();
    ImGui_ImplGlfw_NewFrame();
    ImGui::NewFrame();

    RenderCommandPanel(state);
    RenderSettingsPanel(state);
    RenderPlayPanel(play_state);
    RenderTrainPanel(train_state);

    bool show_demo = state.show_demo();
    if (show_demo) {
      ImGui::ShowDemoWindow(&show_demo);
      if (!show_demo) {
        state.set_show_demo(false);
      }
    }

    ImGui::Render();

    int display_w = 0;
    int display_h = 0;
    glfwGetFramebufferSize(window, &display_w, &display_h);
    glViewport(0, 0, display_w, display_h);
    glClearColor(0.08f, 0.08f, 0.08f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    ImGui_ImplOpenGL2_RenderDrawData(ImGui::GetDrawData());

    glfwSwapBuffers(window);
  }

  ImGui_ImplOpenGL2_Shutdown();
  ImGui_ImplGlfw_Shutdown();
  ImGui::DestroyContext();

  glfwDestroyWindow(window);
  glfwTerminate();
  return 0;
}
