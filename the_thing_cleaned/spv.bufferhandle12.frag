bool compare_float    (highp float a, highp float b)  { return abs(a - b) < 0.05; }
bool compare_vec3     (highp vec3 a, highp vec3 b)    { return compare_float(a.x, b.x)&&compare_float(a.y, b.y)&&compare_float(a.z, b.z); }
bool compare_mat2x3   (highp mat2x3 a, highp mat2x3 b){ return compare_vec3(a[0], b[0])&&compare_vec3(a[1], b[1]); }
bool compare_ivec2    (highp ivec2 a, highp ivec2 b)  { return a == b; }
bool compare_uvec3    (highp uvec3 a, highp uvec3 b)  { return a == b; }
bool compare_float16_t(highp float a, highp float b)  { return abs(a - b) < 0.05; }
void main (void)
{
	bool allOk = true;
	allOk = allOk && compare_mat2x3(blockC.c, mat2x3(-5.0, 1.0, -7.0, 1.0, 2.0, 8.0));
	if (allOk)
		ac_numPassed++;
	blockD.d = (uvec3(8u, 1u, 5u));
}
