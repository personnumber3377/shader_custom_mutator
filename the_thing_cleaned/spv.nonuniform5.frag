layout(location = 0) flat in int Index;
layout(location = 0) out vec4 FragColor;
layout(set = 0, binding = 0) uniform UBO
{
	vec4 v;
} ubos[];
void main()
{
	FragColor = ubos[nonuniformEXT(Index)].v;
}
