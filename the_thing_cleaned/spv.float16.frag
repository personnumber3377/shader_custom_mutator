void main()
{
}
void literal()
{
    const float16_t f16c  = 0.000001hf;
    const f16vec2   f16cv = f16vec2(-0.25HF, 0.03HF);
    f16vec2 f16v;
    f16v.x  = f16c;
    f16v   += f16cv;
}
struct S
{
    float16_t  x;
    f16vec2    y;
    f16vec3    z;
};
layout(constant_id = 100) const float16_t sf16 = 0.125hf;
layout(constant_id = 101) const float     sf   = 0.25;
layout(constant_id = 102) const double    sd   = 0.5lf;
const float  f16_to_f = float(sf16);
const double f16_to_d = float(sf16);
const float16_t f_to_f16 = float16_t(sf);
const float16_t d_to_f16 = float16_t(sd);
void operators()
{
    float16_t f16;
    f16vec2   f16v;
    f16mat2x2 f16m;
    bool      b;
    f16v += f16v;
    f16v -= f16v;
    f16v *= f16v;
    f16v /= f16v;
    f16v++;
    f16v--;
    ++f16m;
    --f16m;
    f16v = -f16v;
    f16m = -f16m;
    f16 = f16v.x + f16v.y;
    f16 = f16v.x - f16v.y;
    f16 = f16v.x * f16v.y;
    f16 = f16v.x / f16v.y;
    b = (f16v.x != f16);
    b = (f16v.y == f16);
    b = (f16v.x >  f16);
    b = (f16v.y <  f16);
    b = (f16v.x >= f16);
    b = (f16v.y <= f16);
    f16v = f16v * f16;
    f16m = f16m * f16;
    f16v = f16m * f16v;
    f16v = f16v * f16m;
    f16m = f16m * f16m;
}
void typeCast()
{
    bvec3   bv;
    vec3    fv;
    dvec3   dv;
    ivec3   iv;
    uvec3   uv;
    i64vec3 i64v;
    u64vec3 u64v;
    f16vec3 f16v;
    f16v = f16vec3(bv);
    bv   = bvec3(f16v);
    f16v = f16vec3(fv);
    fv   = vec3(f16v);
    f16v = f16vec3(dv);
    dv   = dvec3(dv);
    f16v = f16vec3(iv);
    iv   = ivec3(f16v);
    f16v = f16vec3(uv);
    uv   = uvec3(f16v);
    f16v = f16vec3(i64v);
    i64v = i64vec3(f16v);
    f16v = f16vec3(u64v);
    u64v = u64vec3(f16v);
}
void builtinAngleTrigFuncs()
{
    f16vec4 f16v1, f16v2;
    f16v2 = radians(f16v1);
    f16v2 = degrees(f16v1);
    f16v2 = sin(f16v1);
    f16v2 = cos(f16v1);
    f16v2 = tan(f16v1);
    f16v2 = asin(f16v1);
    f16v2 = acos(f16v1);
    f16v2 = atan(f16v1, f16v2);
    f16v2 = atan(f16v1);
    f16v2 = sinh(f16v1);
    f16v2 = cosh(f16v1);
    f16v2 = tanh(f16v1);
    f16v2 = asinh(f16v1);
    f16v2 = acosh(f16v1);
    f16v2 = atanh(f16v1);
}
void builtinExpFuncs()
{
    f16vec2 f16v1, f16v2;
    f16v2 = pow(f16v1, f16v2);
    f16v2 = exp(f16v1);
    f16v2 = log(f16v1);
    f16v2 = exp2(f16v1);
    f16v2 = log2(f16v1);
    f16v2 = sqrt(f16v1);
    f16v2 = inversesqrt(f16v1);
}
void builtinCommonFuncs()
{
    f16vec3   f16v1, f16v2, f16v3;
    float16_t f16;
    bool  b;
    bvec3 bv;
    ivec3 iv;
    f16v2 = abs(f16v1);
    f16v2 = sign(f16v1);
    f16v2 = floor(f16v1);
    f16v2 = trunc(f16v1);
    f16v2 = round(f16v1);
    f16v2 = roundEven(f16v1);
    f16v2 = ceil(f16v1);
    f16v2 = fract(f16v1);
    f16v2 = mod(f16v1, f16v2);
    f16v2 = mod(f16v1, f16);
    f16v3 = modf(f16v1, f16v2);
    f16v3 = min(f16v1, f16v2);
    f16v3 = min(f16v1, f16);
    f16v3 = max(f16v1, f16v2);
    f16v3 = max(f16v1, f16);
    f16v3 = clamp(f16v1, f16, f16v2.x);
    f16v3 = clamp(f16v1, f16v2, f16vec3(f16));
    f16v3 = mix(f16v1, f16v2, f16);
    f16v3 = mix(f16v1, f16v2, f16v3);
    f16v3 = mix(f16v1, f16v2, bv);
    f16v3 = step(f16v1, f16v2);
    f16v3 = step(f16, f16v3);
    f16v3 = smoothstep(f16v1, f16v2, f16v3);
    f16v3 = smoothstep(f16, f16v1.x, f16v2);
    b     = isnan(f16);
    bv    = isinf(f16v1);
    f16v3 = fma(f16v1, f16v2, f16v3);
    f16v2 = frexp(f16v1, iv);
    f16v2 = ldexp(f16v1, iv);
}
void builtinPackUnpackFuncs()
{
    uint u;
    f16vec2 f16v;
    u    = packFloat2x16(f16v);
    f16v = unpackFloat2x16(u);
}
void builtinGeometryFuncs()
{
    float16_t f16;
    f16vec3   f16v1, f16v2, f16v3;
    f16   = length(f16v1);
    f16   = distance(f16v1, f16v2);
    f16   = dot(f16v1, f16v2);
    f16v3 = cross(f16v1, f16v2);
    f16v2 = normalize(f16v1);
    f16v3 = faceforward(f16v1, f16v2, f16v3);
    f16v3 = reflect(f16v1, f16v2);
    f16v3 = refract(f16v1, f16v2, f16);
}
void builtinMatrixFuncs()
{
    f16mat2x3 f16m1, f16m2, f16m3;
    f16mat3x2 f16m4;
    f16mat3   f16m5;
    f16mat4   f16m6, f16m7;
    f16vec3 f16v1;
    f16vec2 f16v2;
    float16_t f16;
    f16m3 = matrixCompMult(f16m1, f16m2);
    f16m1 = outerProduct(f16v1, f16v2);
    f16m4 = transpose(f16m1);
    f16   = determinant(f16m5);
    f16m6 = inverse(f16m7);
}
void builtinVecRelFuncs()
{
    f16vec3 f16v1, f16v2;
    bvec3   bv;
    bv = lessThan(f16v1, f16v2);
    bv = lessThanEqual(f16v1, f16v2);
    bv = greaterThan(f16v1, f16v2);
    bv = greaterThanEqual(f16v1, f16v2);
    bv = equal(f16v1, f16v2);
    bv = notEqual(f16v1, f16v2);
}
in f16vec3 if16v;
void builtinFragProcFuncs()
{
    f16vec3 f16v;
    f16v.x  = dFdx(if16v.x);
    f16v.y  = dFdy(if16v.y);
    f16v.xy = dFdxFine(if16v.xy);
    f16v.xy = dFdyFine(if16v.xy);
    f16v    = dFdxCoarse(if16v);
    f16v    = dFdxCoarse(if16v);
    f16v.x  = fwidth(if16v.x);
    f16v.xy = fwidthFine(if16v.xy);
    f16v    = fwidthCoarse(if16v);
    f16v.x  = interpolateAtCentroid(if16v.x);
    f16v.xy = interpolateAtSample(if16v.xy, 1);
    f16v    = interpolateAtOffset(if16v, f16vec2(0.5hf));
}
