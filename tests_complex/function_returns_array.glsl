HEADER: vert 3 6
#version 300 es

precision mediump float;

float[5] f() {
	return float[5](3.4, 4.2, 5.0, 5.2, 1.1);
}

void main() {
	f();
}