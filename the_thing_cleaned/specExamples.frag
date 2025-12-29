int  a = 0xffffffff;
int  b = 0xffffffffU;
uint c = 0xffffffff;
uint d = 0xffffffffU;
int  e = -1;
uint f = -1u;
int  g = 3000000000;
int  h = 0xA0000000;
int  i = 5000000000;
int  j = 0xFFFFFFFFF;
int  k = 0x80000000;
int  l = 2147483648;
float fa, fb = 1.5;
double fc, fd = 2.0LF;
vec2 texcoord1, texcoord2;
vec3 position;
vec4 myRGBA;
ivec2 textureLookup;
bvec3 less;
mat2 mat2D;
mat3 optMatrix;
mat4 view, projection;
mat4x4 view;
mat3x2 m;
dmat4 highPrecisionMVP;
dmat2x4 dm;
struct light {
    float intensity;
    vec3 position;
} lightVar;
struct S { float f; };
struct T {
	S s;
};
float frequencies[3];
uniform vec4 lightPosition[4];
light lights[];
const int numLights = 2;
light lights[numLights];
in vec3 normal;
centroid in vec2 TexCoord;
invariant centroid in vec4 Color;
noperspective in float temperature;
flat in vec3 myColor;
noperspective centroid in vec2 myTexCoord;
uniform vec4 lightPosition;
uniform vec3 color = vec3(0.7, 0.7, 0.2);
in Material {
    smooth in vec4 Color1;
    smooth vec4 Color2;
    vec2 TexCoordA;
    uniform float Atten;
};
in Light {
    vec4 LightPos;
    vec3 LightColor;
};
in ColoredTexture {
    vec4 Color;
    vec2 TexCoord;
} Materiala;
vec3 Color;
in vec4 gl_FragCoord;
layout(origin_upper_left) in vec4 gl_FragCoord;
layout(pixel_center_integer) in vec4 gl_FragCoord;
layout(origin_upper_left, pixel_center_integer) in vec4 gl_FragCoord;
layout(location = 3) out vec4 color;
layout(location = 3, index = 1) out vec4 factor;
layout(location = 2) out vec4 colors[3];
layout (depth_greater) out float gl_FragDepth;
out float gl_FragDepth;
layout (depth_any) out float gl_FragDepth;
layout (depth_greater) out float gl_FragDepth;
layout (depth_less) out float gl_FragDepth;
layout (depth_unchanged) out float gl_FragDepth;
in vec4 gl_Color;
flat  in vec4 gl_Color;
float[5] foo(float[5])
{
    return float[5](3.4, 4.2, 5.0, 5.2, 1.1);
}
precision highp float;
precision highp int;
precision mediump int;
precision highp float;
void main()
{
    {
		float a[5] = float[5](3.4, 4.2, 5.0, 5.2, 1.1);
	}
	{
		float a[5] = float[](3.4, 4.2, 5.0, 5.2, 1.1);
	}
    {
	    vec4 a[3][2];
		vec4[2] a1[3];
		vec4[3][2] a2;
		vec4 b[2] = vec4[2](vec4(0.0), vec4(0.1));
		vec4[3][2] a3 = vec4[3][2](b, b, b);
		void foo(vec4[3][2]);
		vec4 a4[3][2] = {vec4[2](vec4(0.0), vec4(1.0)),
						 vec4[2](vec4(0.0), vec4(1.0)),
						 vec4[2](vec4(0.0), vec4(1.0)) };
    }
	{
		float a[5];
		{
			float b[] = a;
		}
		{
			float b[5] = a;
		}
		{
			float b[] = float[](1,2,3,4,5);
		}
		a.length();
	}
    {
		vec4 a[3][2];
		a.length();
		a[x].length();
    }
	b[++x].a.length();
	s[x].a.length();
    struct {
        float a;
        int   b;
    } e = { 1.2, 2 };
    struct {
        float a;
        int   b;
    } e = { 1, 3 };
    {
        float a[] = float[](3.4, 4.2, 5.0, 5.2, 1.1);
        float b[] = { 3.4, 4.2, 5.0, 5.2, 1.1 };
        float c[] = a;
        float d[5] = b;
    }
    {
        const vec3 zAxis = vec3 (0.0, 0.0, 1.0);
        const float ceiling = a + b;
    }
    {
        in vec4 position;
        in vec3 normal;
        in vec2 texCoord[4];
    }
    {
        lowp float color;
        out mediump vec2 P;
        lowp ivec2 foo(lowp mat3);
        highp mat4 m;
    }
}
