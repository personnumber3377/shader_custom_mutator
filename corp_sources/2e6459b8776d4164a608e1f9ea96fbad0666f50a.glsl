precision mediump float;
precision mediump int;

precision mediump float;
varying vec4 color;
void main ()
{
	bool toDiscard = false;
	if(color.r > 0.75) toDiscard = true;
	else if(color.g > 0.75) toDiscard = true;
	else if(color.b > 0.75) toDiscard = true;
	if (toDiscard) discard;
	gl_FragColor = color;
}
