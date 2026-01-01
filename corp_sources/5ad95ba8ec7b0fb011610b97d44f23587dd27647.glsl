precision mediump float;
precision mediump int;

attribute vec4 gtf_Vertex;
uniform mat4 gtf_ModelViewProjectionMatrix;
varying vec4 color;
void main ()
{
	int count=0;
	int val=0;
    	for(int i=0;i<10;i++)
	{
	  count++;
	  if(count == 5)
            continue;
	  else
	    val += count;
	}
	float gray;
	if( val == 50)
	gray=1.0;
	else gray=0.0;
	color = vec4(gray, gray, gray, 1.0);
	gl_Position = gtf_ModelViewProjectionMatrix * gtf_Vertex;
}
