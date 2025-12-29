void main()
{
    struct s {
        float y[5];
    } str;
    float t;
    int index = 5;
    str.y[4] = 2.0;
    t = ++str.y[--index];
    str.y[4] += t;
    t = str.y[4]--;
    str.y[index++] += t;
    --str.y[--index];
    float x = str.y[4];
	++x;
	--x;
	x++;
	x--;
	float y = x * ++x;
	float z = y * x--;
    vec4 v = vec4(1.0, 2.0, 3.0, 4.0);
    v.y = v.z--;
    v.x = --v.w;
    gl_FragColor = z * v;
}
