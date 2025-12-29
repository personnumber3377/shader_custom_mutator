precision highp float;
in vec2 vUV;
out vec4 color;
uniform highp sampler2DShadow sampler;
uniform int funct;
void main (void)
{
    switch (funct)
    {
    case 0:
        ivec2 iv2 = textureSize(sampler, 0);
        vec2 fv2 = textureQueryLOD(sampler, vec2(0.0, 0.0));
		color = vec4(iv2,fv2);
        break;
    default:
        color = vec4(1.0, 1.0, 1.0, 1.0);
        break;
    }
}
