precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	vec4 tmp_Color = color + vec4(0.25);
	gl_FragColor = vec4(normalize(tmp_Color.rgb), 1.0);
}
