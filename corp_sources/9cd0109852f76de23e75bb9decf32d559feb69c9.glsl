precision mediump float;
precision mediump int;

precision mediump float;
uniform vec4 color;
uniform ivec4 icolor;
uniform bool flag;
void main ()
{
	if(flag)
		gl_FragColor = vec4 (icolor[0], icolor[1], icolor[2], icolor[3]);
	else
		gl_FragColor = vec4 (color[0], color[1], color[2], color[3]);
}
