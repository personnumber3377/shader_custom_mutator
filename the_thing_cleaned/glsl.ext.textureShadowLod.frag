uniform sampler2DArrayShadow s2da;
uniform samplerCubeArrayShadow sca;
uniform samplerCubeShadow sc;
out float c;
in vec4 tc;
void pass() {
    c = texture(s2da, tc, 0.0);
    c = texture(sca, tc, 0.0, 0.0);
    c = textureOffset(s2da, tc, ivec2(0.0), 0.0);
    c = textureLod(s2da, tc, 0.0);
    c = textureLod(sc, tc, 0.0);
    c = textureLod(sca, tc, 0.0, 0.0);
    c = textureLodOffset(s2da, tc, 0.0, ivec2(0.0));
}
void fail() {
    c = texture(s2da, tc, 0.0);
    c = texture(sca, tc, 0.0, 0.0);
    c = textureOffset(s2da, tc, ivec2(0.0), 0.0);
    c = textureLod(s2da, tc, 0.0);
    c = textureLod(sc, tc, 0.0);
    c = textureLod(sca, tc, 0.0, 0.0);
    c = textureLodOffset(s2da, tc, 0.0, ivec2(0.0));
}
