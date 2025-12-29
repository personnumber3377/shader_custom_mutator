    int64_t i64 = i64Const[index];
    const uint64_t u64Const[] =
    {
        0xFFFFFFFFFFFFFFFFul,
        4294967296UL,
        077777777777ul,
    };
    uint64_t u64 = u64Const[index];
}
void typeCast()
{
    bvec2 bv;
    ivec2 iv;
    uvec2 uv;
    vec2  fv;
    dvec2 dv;
    i64vec2 i64v;
    u64vec2 u64v;
    i64v = i64vec2(bv);
    u64v = u64vec2(bv);
    i64v = iv;
    iv = ivec2(i64v);
    u64v = uv;
    uv = uvec2(u64v);
    fv = vec2(i64v);
    dv = i64v;
    fv = vec2(u64v);
    dv = u64v;
    i64v = i64vec2(fv);
    i64v = i64vec2(dv);
    u64v = u64vec2(fv);
    u64v = u64vec2(dv);
    bv = bvec2(i64v);
    bv = bvec2(u64v);
    u64v = i64v;
    i64v = i64vec2(u64v);
    uv = uvec2(i64v);
    i64v = i64vec2(uv);
    iv = ivec2(u64v);
    u64v = iv;
}
void operators()
{
    u64vec3 u64v;
    int64_t i64;
    uvec3   uv;
    int     i;
    bool    b;
    u64v++;
    i64--;
    ++i64;
    --u64v;
    u64v = ~u64v;
    i64 = +i64;
    u64v = -u64v;
    i64  += i64;
    u64v -= u64v;
    i64  *= i;
    u64v /= uv;
    u64v %= i;
    u64v = u64v + uv;
    i64  = i64 - i;
    u64v = u64v * uv;
    i64  = i64 * i;
    i64  = i64 % i;
    u64v = u64v << i;
    i64 = i64 >> uv.y;
    u64v <<= i;
    i64  >>= uv.y;
    i64  = i64 << u64v.z;
    u64v = u64v << i64;
    b = (u64v.x != i64);
    b = (i64 == u64v.x);
    b = (u64v.x > uv.y);
    b = (i64 < i);
    b = (u64v.y >= uv.x);
    b = (i64 <= i);
    u64v |= i;
    i64  = i64 | i;
    i64  &= i;
    u64v = u64v & uv;
    u64v ^= i64;
    u64v = u64v ^ i64;
}
void builtinFuncs()
{
    i64vec2  i64v;
    u64vec3  u64v;
    dvec3    dv;
    bvec3    bv;
    int64_t  i64;
    uint64_t u64;
    i64v = abs(i64v);
    i64  = sign(i64);
    i64v = min(i64v, i64);
    i64v = min(i64v, i64vec2(-1));
    u64v = min(u64v, u64);
    u64v = min(u64v, u64vec3(0));
    i64v = max(i64v, i64);
    i64v = max(i64v, i64vec2(-1));
    u64v = max(u64v, u64);
    u64v = max(u64v, u64vec3(0));
    i64v = clamp(i64v, -i64, i64);
    i64v = clamp(i64v, -i64v, i64v);
    u64v = clamp(u64v, -u64, u64);
    u64v = clamp(u64v, -u64v, u64v);
    i64  = mix(i64v.x, i64v.y, true);
    i64v = mix(i64vec2(i64), i64vec2(-i64), bvec2(false));
    u64  = mix(u64v.x, u64v.y, true);
    u64v = mix(u64vec3(u64), u64vec3(-u64), bvec3(false));
    i64v = doubleBitsToInt64(dv.xy);
    u64v.x = doubleBitsToUint64(dv.z);
    dv.xy = int64BitsToDouble(i64v);
    dv = uint64BitsToDouble(u64v);
    i64 = packInt2x32(ivec2(1, 2));
    ivec2 iv = unpackInt2x32(i64);
    u64 = packUint2x32(uvec2(2, 3));
    uvec2 uv = unpackUint2x32(u64);
    bv    = lessThan(u64v, u64vec3(u64));
    bv.xy = lessThan(i64v, i64vec2(i64));
    bv    = lessThanEqual(u64v, u64vec3(u64));
    bv.xy = lessThanEqual(i64v, i64vec2(i64));
    bv    = greaterThan(u64v, u64vec3(u64));
    bv.xy = greaterThan(i64v, i64vec2(i64));
    bv    = greaterThanEqual(u64v, u64vec3(u64));
    bv.xy = greaterThanEqual(i64v, i64vec2(i64));
    bv    = equal(u64v, u64vec3(u64));
    bv.xy = equal(i64v, i64vec2(i64));
    bv    = notEqual(u64v, u64vec3(u64));
    bv.xy = notEqual(i64v, i64vec2(i64));
    i64   = findLSB(u64);
    i64v  = findLSB(u64vec2(u64));
    i64   = bitCount(u64);
    i64v  = bitCount(u64vec2(u64));
}
layout(constant_id = 100) const int64_t  si64 = -10L;
layout(constant_id = 101) const uint64_t su64 = 20UL;
layout(constant_id = 102) const int  si = -5;
layout(constant_id = 103) const uint su = 4;
layout(constant_id = 104) const bool sb = true;
layout(constant_id = 105) const uint64_t su64inc = su64 + 1UL;
const bool i64_to_b = bool(si64);
const bool u64_to_b = bool(su64);
const int64_t  b_to_i64 = int64_t(sb);
const uint64_t b_to_u64 = uint64_t(sb);
const int     i64_to_i = int(si64);
const int64_t i_to_i64 = int64_t(si);
const uint     u64_to_u = uint(su64);
const uint64_t u_to_u64 = uint64_t(su);
const int64_t  u64_to_i64 = int64_t(su64);
const uint64_t i64_to_u64 = uint64_t(si64);
const int      u64_to_i = int(su64);
const uint64_t i_to_u64 = uint64_t(si);
const uint    i64_to_u = uint(si64);
const int64_t u_to_i64 = int64_t(su);
uint64_t u64Max = UINT64_MAX;
