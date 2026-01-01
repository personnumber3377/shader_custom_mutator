precision mediump float;
precision mediump int;

precision mediump float;
void main()
{
	gl_FragColor = vec4(gl_DepthRange.near, gl_DepthRange.far, gl_DepthRange.diff, 1.0);
}
