precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
varying float dotClip[2];
void main ()
{
	if (dotClip[0] >= 0.0 || dotClip[1] >= 0.0)
		discard;
    gl_FragColor = color;
}
