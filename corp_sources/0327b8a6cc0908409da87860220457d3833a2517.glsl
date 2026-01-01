precision mediump float;
precision mediump int;

struct FuzzStruct1698 {
  bvec4 f_3478;
  mat2 f_3411[1];
};

vec4 gtf_Vertex = vec4((false ? (true ? 0.0 : 2.0) : 0.5), 2.0, 0.5, +(true ? (false ? 0.0 : 1.0) : 0.0));

vec4 gtf_Color = vec4(1.0, -0.5, -1.0, 2.0);

uniform mat4 gtf_ModelViewProjectionMatrix;

varying vec4 color;

void main()
{
  vec2 c = (2.0 * (gtf_Color.rg - 0.5));
  if (false)
  {
    0.5;
  }
  else
  {
    vec4(0.5, -1.0, +-1.0, 0.5);
  }
  if ((c[1] < 0.0))
    (c[1] *= -1.0);
  color = vec4(c, 0.0, 1.0);
  gl_Position = (gtf_ModelViewProjectionMatrix * gtf_Vertex);
  ivec2((9 - +6), -3);
}

