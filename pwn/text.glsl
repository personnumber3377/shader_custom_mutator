HEADER: frag 3 6
#version 100
#extension GL_EXT_shader_framebuffer_fetch : require

precision mediump float;
precision mediump int;

vec4 color = vec4(+(false ? -2.0 : (true ? 2.0 : 1.0)), 2.0, 2.0, -1.0);

uniform sampler2D u;

struct S {
  bool b;
  sampler2D samplerMember;
};

struct T {
  bool b;
  S nest;
};

uniform T uStruct;

vec2 uTexCoord = vec2(2.0);

int g = -14;

uniform float loopMax;

vec4 sampleConstSampler(const in sampler2D s)
{
  return texture2D(s, vec2(0));
}

vec4 foo2(S structVar)
{
  if (structVar.b)
    return texture2D(structVar.samplerMember, uTexCoord);
  else
    return vec4(1, 0, 0, 1);
}

vec4 foo(T structVar)
{
  if (structVar.b)
    return foo2(structVar.nest);
  else
    return vec4(1, 0, 0, 1);
}

void F()
{
  ((true ? true : false) ? g : 1);
  ivec2((false ? (false ? (9 + g) : (9 + 8)) : 0), 9);
}

void G()
{
  (-++g + 5);
  foo2(S(!false, u));
}

void main()
{
  gl_FragColor = foo(uStruct);
  for (float l = 0.0; (l < loopMax); l++)
  {
    if ((loopMax > 3.0))
    {
      (gl_FragColor.a += 0.1);
    }
  }
  G();
  G();
  if (false)
  {
    +1.0;
  }
  else
  {
    (-1.0 + 1.0);
  }
  gl_FragColor = sampleConstSampler(u);
  gl_FragColor = (length(color.xy) * gl_LastFragData[0]);
  gl_FragColor = (length(color.xy) * gl_LastFragData[0]);
}
