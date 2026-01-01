precision mediump float;
precision mediump int;

precision mediump float;
varying vec3  Position;
varying float lightIntensity;
uniform sampler2D sampler2d;
varying vec4 gtf_TexCoord[1];
void main ()
{
    vec3 lightColor = vec3(texture2D(sampler2d,  vec2(gtf_TexCoord[0]))) * lightIntensity;
    vec3 ct = clamp(lightColor, 0.0, 1.0);
    gl_FragColor = vec4 (ct, 1.0);
}
