layout(location = 0) out vec4 outColor;
layout(binding = 1, set = 0) uniform accelerationStructureEXT topLevelAS;
void main() {
  outColor = vec4(0.0);
}
