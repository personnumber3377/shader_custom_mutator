precision mediump float;
precision mediump int;

precision mediump float;
uniform vec3 lightPosition[2];
varying vec4  color;
void main()
{
     int i;
     gl_FragColor = vec4(0.0);
	 gl_FragColor += vec4(lightPosition[0], 0.0);
	 gl_FragColor += vec4(lightPosition[1], 0.0);
     gl_FragColor /= 2.0;
}
