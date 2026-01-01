precision mediump float;
precision mediump int;

precision mediump float;
uniform sampler2D gtf_Texture0;
varying vec4 color;
varying vec4 gtf_TexCoord[1];
void main ()
{
	gl_FragColor = texture2D(gtf_Texture0, gtf_TexCoord[0].st, 1.0) * color;
}
