    const uint16_t u16c[] =
    {
        0xFFFFus,
        65535US,
        0177777us,
    };
    uint16_t u16 = i16c[i] + u16c[i];
}
void operators()
{
    u16vec3  u16v;
    int16_t  i16;
    uint16_t u16;
    int      i;
    uint     u;
    bool     b;
    u16v++;
    i16--;
    ++i16;
    --u16v;
    u16v = ~u16v;
    i16 = +i16;
    u16v = -u16v;
    u16  += i16;
    u16v -= u16v;
    i16  *= i16;
    u16v /= u16v;
    u16v %= i16;
    u16v = u16v + u16v;
    u16  = i16 - u16;
    u16v = u16v * i16;
    i16  = i16 * i16;
    i16  = i16 % i16;
    u16v <<= i16;
    i16  >>= u16v.y;
    i16  = i16 << u16v.z;
    u16v = u16v << i16;
    b = (u16v.x != i16);
    b = (i16 == u16v.x);
    b = (u16v.x > u16v.y);
    b = (i16 < u);
    b = (u16v.y >= u16v.x);
    b = (i16 <= i);
    u16v |= i16;
    u16  = i16 | u16;
    i16  &= i16;
    u16v = u16v & u16v;
    u16v ^= i16;
    u16v = u16v ^ i16;
}
void typeCast()
{
    bvec2 bv;
    ivec2 iv;
    uvec2 uv;
    vec2  fv;
    dvec2 dv;
    f16vec2 f16v;
    i64vec2 i64v;
    u64vec2 u64v;
    i16vec2 i16v;
    u16vec2 u16v;
    i16v = i16vec2(bv);
    u16v = u16vec2(bv);
    bv   = bvec2(i16v);
    bv   = bvec2(u16v);
    i16v = i16vec2(iv);
    u16v = u16vec2(iv);
    iv   = i16v;
    iv   = ivec2(u16v);
    i16v = i16vec2(uv);
    u16v = u16vec2(uv);
    uv   = i16v;
    uv   = u16v;
    i16v = i16vec2(fv);
    u16v = u16vec2(fv);
    fv   = i16v;
    fv   = u16v;
    i16v = i16vec2(dv);
    u16v = u16vec2(dv);
    dv   = i16v;
    dv   = u16v;
    i16v = i16vec2(f16v);
    u16v = u16vec2(f16v);
    f16v = i16v;
    f16v = u16v;
    i16v = i16vec2(i64v);
    u16v = u16vec2(i64v);
    i64v = i16v;
    i64v = i64vec2(u16v);
    i16v = i16vec2(u64v);
    u16v = u16vec2(u64v);
    u64v = i16v;
    u64v = u16v;
    i16v = i16vec2(u16v);
    u16v = i16v;
}
void builtinFuncs()
{
    i16vec2  i16v;
    u16vec3  u16v;
    f16vec3  f16v;
    bvec3    bv;
    int16_t  i16;
    uint16_t u16;
    i16v = abs(i16v);
    i16v  = sign(i16v);
    i16v = min(i16v, i16);
    i16v = min(i16v, i16vec2(-1s));
    u16v = min(u16v, u16);
    u16v = min(u16v, u16vec3(0us));
    i16v = max(i16v, i16);
    i16v = max(i16v, i16vec2(-1s));
    u16v = max(u16v, u16);
    u16v = max(u16v, u16vec3(0us));
    i16v = clamp(i16v, -i16, i16);
    i16v = clamp(i16v, -i16v, i16v);
    u16v = clamp(u16v, -u16, u16);
    u16v = clamp(u16v, -u16v, u16v);
    i16  = mix(i16v.x, i16v.y, true);
    i16v = mix(i16vec2(i16), i16vec2(-i16), bvec2(false));
    u16  = mix(u16v.x, u16v.y, true);
    u16v = mix(u16vec3(u16), u16vec3(-u16), bvec3(false));
    i16vec3 exp;
    f16v = frexp(f16v, exp);
    f16v = ldexp(f16v, exp);
    i16v = float16BitsToInt16(f16v.xy);
    u16v.x = float16BitsToUint16(f16v.z);
    f16v.xy = int16BitsToFloat16(i16v);
    f16v = uint16BitsToFloat16(u16v);
    int packi = packInt2x16(i16v);
    i16v = unpackInt2x16(packi);
    uint packu = packUint2x16(u16v.xy);
    u16v.xy = unpackUint2x16(packu);
    int64_t packi64 = packInt4x16(i16vec4(i16));
    i16v = unpackInt4x16(packi64).xy;
    uint64_t packu64 = packUint4x16(u16vec4(u16));
    u16v = unpackUint4x16(packu64).xyz;
    bv    = lessThan(u16v, u16vec3(u16));
    bv.xy = lessThan(i16v, i16vec2(i16));
    bv    = lessThanEqual(u16v, u16vec3(u16));
    bv.xy = lessThanEqual(i16v, i16vec2(i16));
    bv    = greaterThan(u16v, u16vec3(u16));
    bv.xy = greaterThan(i16v, i16vec2(i16));
    bv    = greaterThanEqual(u16v, u16vec3(u16));
    bv.xy = greaterThanEqual(i16v, i16vec2(i16));
    bv    = equal(u16v, u16vec3(u16));
    bv.xy = equal(i16v, i16vec2(i16));
    bv    = notEqual(u16v, u16vec3(u16));
    bv.xy = notEqual(i16v, i16vec2(i16));
}
layout(constant_id = 100) const int64_t  si64 = -10L;
layout(constant_id = 101) const uint64_t su64 = 20UL;
layout(constant_id = 102) const int  si = -5;
layout(constant_id = 103) const uint su = 4;
layout(constant_id = 104) const bool sb = true;
layout(constant_id = 105) const int16_t si16 = -5S;
layout(constant_id = 106) const uint16_t su16 = 4US;
const bool i16_to_b = bool(si16);
const bool u16_to_b = bool(su16);
const int16_t  b_to_i16 = int16_t(sb);
const uint16_t b_to_u16 = uint16_t(sb);
const int i16_to_i = int(si16);
const int u16_to_i = int(su16);
const int16_t  i_to_i16 = int16_t(si);
const uint16_t i_to_u16 = uint16_t(si);
const uint i16_to_u = uint(si16);
const uint u16_to_u = uint(su16);
const int16_t  u_to_i16 = int16_t(su);
const uint16_t u_to_u16 = uint16_t(su);
const int64_t i16_to_i64 = int64_t(si16);
const int64_t u16_to_i64 = int64_t(su16);
const int16_t  i64_to_i16 = int16_t(si64);
const uint16_t i64_to_u16 = uint16_t(si64);
const uint64_t i16_to_u64 = uint64_t(si16);
const uint64_t u16_to_u64 = uint64_t(su16);
const int16_t  u64_to_i16 = int16_t(su64);
const uint16_t u64_to_u16 = uint16_t(su64);
const uint16_t i16_to_u16 = uint16_t(si16);
const int16_t  u16_to_i16 = int16_t(su16);
void main()
{
    literal();
    operators();
    typeCast();
    builtinFuncs();
}
