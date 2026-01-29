#include <GLFW/glfw3.h>
#include <imgui.h>
#include <imgui_impl_glfw.h>
#include <imgui_impl_opengl2.h>

#include <cstdio>

namespace {
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
    std::fprintf(stderr, "Не удалось инициализировать GLFW.\\n");
    return 1;
  }

  GLFWwindow* window = glfwCreateWindow(1280, 720, "40kAI: ImGui минимальный GUI", nullptr, nullptr);
  if (!window) {
    std::fprintf(stderr, "Не удалось создать окно GLFW.\\n");
    glfwTerminate();
    return 1;
  }

  glfwMakeContextCurrent(window);
  glfwSwapInterval(1);

  IMGUI_CHECKVERSION();
  ImGui::CreateContext();
  ImGuiIO& io = ImGui::GetIO();
  io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;

  ImGui::StyleColorsDark();
  ApplyWarhammerStyle();

  ImGui_ImplGlfw_InitForOpenGL(window, true);
  ImGui_ImplOpenGL2_Init();

  bool show_demo = false;
  int clicks = 0;

  while (!glfwWindowShouldClose(window)) {
    glfwPollEvents();

    ImGui_ImplOpenGL2_NewFrame();
    ImGui_ImplGlfw_NewFrame();
    ImGui::NewFrame();

    ImGui::Begin("Командный пункт");
    ImGui::Text("Минимальный ImGui GUI. Дальше будем переносить окна.");
    if (ImGui::Button("Боевой клич")) {
      ++clicks;
    }
    ImGui::SameLine();
    ImGui::Text("Нажатий: %d", clicks);
    ImGui::Checkbox("Показать демо-окно", &show_demo);
    ImGui::End();

    if (show_demo) {
      ImGui::ShowDemoWindow(&show_demo);
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
