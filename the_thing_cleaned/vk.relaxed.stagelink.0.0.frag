uniform int uTDInstanceIDOffset;
uniform int uTDNumInstances;
uniform float uTDAlphaTestVal;
struct TDPhongResult
{
	vec3 diffuse;
	vec3 specular;
	vec3 specular2;
	float shadowStrength;
};
struct TDPBRResult
{
	vec3 diffuse;
	vec3 specular;
	float shadowStrength;
};
struct TDMatrix
{
	mat4 world;
	mat4 worldInverse;
	mat4 worldCam;
	mat4 worldCamInverse;
	mat4 cam;
	mat4 camInverse;
	mat4 camProj;
	mat4 camProjInverse;
	mat4 proj;
	mat4 projInverse;
	mat4 worldCamProj;
	mat4 worldCamProjInverse;
	mat4 quadReproject;
	mat3 worldForNormals;
	mat3 camForNormals;
	mat3 worldCamForNormals;
};
struct TDCameraInfo
{
	vec4 nearFar;
	vec4 fog;
	vec4 fogColor;
	int renderTOPCameraIndex;
};
struct TDGeneral
{
	vec4 ambientColor;
	vec4 nearFar;
	vec4 viewport;
	vec4 viewportRes;
	vec4 fog;
	vec4 fogColor;
};
void TDAlphaTest(float alpha);
vec4 TDDither(vec4 color);
vec4 TDOutputSwizzle(vec4 v);
uvec4 TDOutputSwizzle(uvec4 v);
void TDCheckOrderIndTrans();
void TDCheckDiscard();
uniform vec3 uConstant;
uniform float uShadowStrength;
uniform vec3 uShadowColor;
uniform vec4 uDiffuseColor;
uniform vec4 uAmbientColor;
uniform sampler2DArray sColorMap;
in Vertex
{
	vec4 color;
	vec3 worldSpacePos;
	vec3 texCoord0;
	flat int cameraIndex;
	flat int instance;
} iVert;
layout(location = 0) out vec4 oFragColor[TD_NUM_COLOR_BUFFERS];
void main()
{
	TDCheckDiscard();
	vec4 outcol = vec4(0.0, 0.0, 0.0, 0.0);
	vec3 texCoord0 = iVert.texCoord0.stp;
	float actualTexZ = mod(int(texCoord0.z),2048);
	float instanceLoop = floor(int(texCoord0.z)/2048);
	texCoord0.z = actualTexZ;
	vec4 colorMapColor = texture(sColorMap, texCoord0.stp);
	float red = colorMapColor[int(instanceLoop)];
	colorMapColor = vec4(red);
	outcol.rgb += uConstant * iVert.color.rgb;
	outcol *= colorMapColor;
	float alpha = iVert.color.a * colorMapColor.a ;
	outcol = TDDither(outcol);
	outcol.rgb *= alpha;
	TDAlphaTest(alpha);
	outcol.a = alpha;
	oFragColor[0] = TDOutputSwizzle(outcol);
	for (int i = 1; i < TD_NUM_COLOR_BUFFERS; i++)
	{
		oFragColor[i] = vec4(0.0);
	}
}
