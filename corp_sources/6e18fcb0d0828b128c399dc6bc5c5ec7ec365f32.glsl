precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	gl_FragColor = vec4(float(gl_MaxCombinedTextureImageUnits) / 8.0);
}
